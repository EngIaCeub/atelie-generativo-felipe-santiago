from __future__ import annotations

import argparse
import csv
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DATASET_LICENSE_PREFIXES = (
    "Public domain",
    "CC0",
    "CC-BY ",
    "CC-BY-SA ",
)
REQUIRED_TEAM_ASSIGNMENTS = [
    "dados_e_licencas",
    "treinamento_lora",
    "avaliacao",
    "aplicacao_e_publicacao",
    "documentacao",
]
REQUIRED_BOOTSTRAP = [
    "AGENTS.md",
    "PLANS.md",
    "PROJECT_STATE.md",
    "config/project.json",
    "dados/fontes.csv",
    "dados/legendas.txt",
    "notebooks/01_dataset.ipynb",
    "notebooks/02_treino_lora.ipynb",
    "notebooks/03_avaliacao.ipynb",
    "app/app.py",
    "relatorio/relatorio_final.md",
]


@dataclass
class Check:
    key: str
    ok: bool
    message: str
    evidence: str = ""


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def noncomment_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def assignment_people(value: object) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [person.strip() for person in value if isinstance(person, str) and person.strip()]
    return []


def bootstrap_checks(root: Path, config: dict) -> list[Check]:
    checks = [
        Check("structure", all((root / p).exists() for p in REQUIRED_BOOTSTRAP),
              "Estrutura mínima presente." if all((root / p).exists() for p in REQUIRED_BOOTSTRAP)
              else "Há arquivos obrigatórios ausentes."),
        Check("legacy_noteboks", not (root / "noteboks").exists(),
              "Nome notebooks correto." if not (root / "noteboks").exists()
              else "A pasta legada noteboks/ ainda existe."),
    ]
    team = config.get("team", {})
    members = [
        member.strip()
        for member in team.get("members", [])
        if isinstance(member, str) and member.strip()
    ]
    assignments = team.get("assignments")
    valid_assignments = assignments if isinstance(assignments, dict) else {}
    missing_roles = [
        role
        for role in REQUIRED_TEAM_ASSIGNMENTS
        if not assignment_people(valid_assignments.get(role))
    ]
    assigned_people = [
        person
        for role in REQUIRED_TEAM_ASSIGNMENTS
        for person in assignment_people(valid_assignments.get(role))
    ]
    unknown_people = sorted({person for person in assigned_people if person not in members})
    style = config.get("style", {})
    hf = config.get("hugging_face", {})
    checks.extend([
        Check("team_roles_confirmed", team.get("roles_confirmed") is True,
              "Papéis da equipe confirmados." if team.get("roles_confirmed") is True
              else "Confirme team.roles_confirmed como true em config/project.json."),
        Check("team_members", bool(members),
              f"{len(members)} integrante(s) registrado(s)." if members
              else "Inclua pelo menos um integrante em team.members."),
        Check("team_assignments", isinstance(assignments, dict),
              "team.assignments definido." if isinstance(assignments, dict)
              else "Defina team.assignments em config/project.json."),
        Check("team_required_roles", not missing_roles,
              "Papéis obrigatórios preenchidos." if not missing_roles
              else "Preencha os papéis obrigatórios: " + ", ".join(missing_roles) + "."),
        Check("team_assignment_members", not unknown_people,
              "Todas as pessoas atribuídas existem em team.members." if not unknown_people
              else "Pessoas atribuídas fora de team.members: " + ", ".join(unknown_people) + "."),
        Check("style_defined", bool(style.get("name") and style.get("trigger_token")),
              "Estilo e token definidos." if style.get("name") and style.get("trigger_token")
              else "Defina estilo e trigger_token em config/project.json."),
        Check("style_approved", style.get("approval_status") == "approved",
              "Estilo aprovado." if style.get("approval_status") == "approved"
              else "Aprovação humana/professor pendente."),
        Check("hf_namespace", bool(hf.get("namespace")),
              "Namespace Hugging Face definido." if hf.get("namespace")
              else "Namespace Hugging Face pendente."),
        Check("token_policy", hf.get("token_status") == "available_not_versioned",
              "Token registrado apenas como status, sem valor."),
    ])
    return checks


def dataset_checks(root: Path, config: dict) -> list[Check]:
    images = [p for p in (root / "dados/imagens").glob("*") if p.suffix.lower() in IMAGE_EXTENSIONS]
    sources = read_csv(root / "dados/fontes.csv")
    captions = noncomment_lines(root / "dados/legendas.txt")
    source_files = {row.get("arquivo", "").strip() for row in sources if row.get("arquivo")}
    reviewed_files: set[str] = set()
    malformed = 0
    token = config.get("style", {}).get("trigger_token", "")
    for line in captions:
        parts = line.split("\t")
        if len(parts) < 3:
            malformed += 1
            continue
        filename, caption, status = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if status == "revisada" and (not token or caption.startswith(token + ",")):
            reviewed_files.add(filename)
    image_files = {p.name for p in images}
    required_source_fields = {
        "arquivo",
        "url",
        "autor",
        "licenca",
        "data_coleta",
        "fonte",
        "observacoes",
    }
    rows_with_required_fields = [
        row
        for row in sources
        if all(row.get(field, "").strip() for field in required_source_fields)
    ]
    allowed_license_rows = [
        row
        for row in sources
        if row.get("licenca", "").strip().startswith(ALLOWED_DATASET_LICENSE_PREFIXES)
    ]
    image_sizes: dict[str, tuple[int, int]] = {}
    unreadable_images: list[str] = []
    for image_path in images:
        try:
            with Image.open(image_path) as image:
                image_sizes[image_path.name] = image.size
        except (OSError, UnidentifiedImageError):
            unreadable_images.append(image_path.name)
    small_images = [
        filename
        for filename, size in image_sizes.items()
        if min(size) < 512
    ]
    return [
        Check("image_count", 20 <= len(images) <= 40, f"{len(images)} imagens encontradas; esperado 20–40."),
        Check("provenance_count", image_files == source_files and bool(image_files),
              "Proveniência cobre todas as imagens." if image_files == source_files and image_files
              else f"Diferenças imagem/fonte: imagens sem fonte={sorted(image_files-source_files)}, fontes sem imagem={sorted(source_files-image_files)}."),
        Check("provenance_fields", len(rows_with_required_fields) == len(sources) and bool(sources),
              "Campos obrigatÃ³rios de proveniÃªncia preenchidos." if len(rows_with_required_fields) == len(sources) and sources
              else f"Linhas com proveniÃªncia completa: {len(rows_with_required_fields)}/{len(sources)}."),
        Check("allowed_licenses", len(allowed_license_rows) == len(sources) and bool(sources),
              "Todas as licenÃ§as do dataset sÃ£o permitidas." if len(allowed_license_rows) == len(sources) and sources
              else f"Linhas com licenÃ§a permitida: {len(allowed_license_rows)}/{len(sources)}."),
        Check("image_resolution", not unreadable_images and not small_images and len(image_sizes) == len(images) and bool(images),
              "Todas as imagens tÃªm pelo menos 512 x 512." if not unreadable_images and not small_images and image_sizes
              else f"Imagens ilegÃ­veis={unreadable_images}; abaixo de 512={small_images}."),
        Check("captions_reviewed", image_files == reviewed_files and bool(image_files) and malformed == 0,
              "Todas as captions estão revisadas." if image_files == reviewed_files and image_files and malformed == 0
              else f"Captions revisadas {len(reviewed_files)}/{len(image_files)}; linhas malformadas={malformed}."),
        Check("metadata", (root / "dados/metadata.jsonl").exists() and bool(noncomment_lines(root / "dados/metadata.jsonl")),
              "metadata.jsonl gerado." if noncomment_lines(root / "dados/metadata.jsonl") else "metadata.jsonl vazio/ausente."),
    ]


def training_checks(root: Path, config: dict) -> list[Check]:
    rows = read_csv(root / "resultados/treino/experimentos.csv")
    completed = [r for r in rows if r.get("status", "").lower() in {"completed", "concluido", "concluído"}]
    hf = config.get("hugging_face", {})
    model_card_candidates = [root / "MODEL_CARD.md", root / "docs/templates/MODEL_CARD.md"]
    return [
        Check("two_training_runs", len(completed) >= 2,
              f"{len(completed)} experimentos concluídos registrados; mínimo 2."),
        Check("lora_repo", bool(hf.get("lora_repo_id")),
              "ID do LoRA no Hub registrado." if hf.get("lora_repo_id") else "lora_repo_id pendente."),
        Check("model_card", any(p.exists() and p.stat().st_size > 200 for p in model_card_candidates),
              "Model card local encontrado."),
    ]


def evaluation_checks(root: Path, config: dict) -> list[Check]:
    prompts = noncomment_lines(root / "dados/prompts_avaliacao.txt")
    clip_rows = read_csv(root / "resultados/avaliacao/clipscore.csv")
    memory_rows = read_csv(root / "resultados/avaliacao/memorizacao.csv")
    human_rows = read_csv(root / "resultados/avaliacao/avaliacao_humana.csv")
    raters = {r.get("id_avaliador", "").strip() for r in human_rows if r.get("id_avaliador")}
    grade_exists = any((root / "resultados/avaliacao").glob("grade_comparativa.*"))
    min_raters = int(config.get("evaluation", {}).get("minimum_external_raters", 5))
    return [
        Check("six_prompts", len(prompts) == 6, f"{len(prompts)} prompts fixos; esperado 6."),
        Check("comparison_grid", grade_exists, "Grade comparativa encontrada." if grade_exists else "Grade comparativa ausente."),
        Check("clipscore", len(clip_rows) >= 12, f"{len(clip_rows)} linhas de CLIPScore; esperado ao menos 12."),
        Check("memorization", len(memory_rows) >= 10, f"{len(memory_rows)} casos de memorização; esperado 10."),
        Check("human_evaluation", len(raters) >= min_raters,
              f"{len(raters)} avaliadores únicos; mínimo {min_raters}."),
    ]


def publication_checks(root: Path, config: dict) -> list[Check]:
    hf = config.get("hugging_face", {})
    app_text = (root / "app/app.py").read_text(encoding="utf-8") if (root / "app/app.py").exists() else ""
    pending = "PendingPromptExpander" in app_text or "PendingImageGenerator" in app_text
    return [
        Check("space_repo", bool(hf.get("space_repo_id")),
              "ID do Space registrado." if hf.get("space_repo_id") else "space_repo_id pendente."),
        Check("production_backends", not pending and bool(app_text),
              "Backends de produção configurados." if not pending and app_text else "App ainda contém backends Pending."),
        Check("requirements", (root / "app/requirements.txt").exists() and (root / "app/requirements.txt").stat().st_size > 0,
              "requirements do app presente."),
    ]


def final_checks(root: Path) -> list[Check]:
    pdf = root / "relatorio/relatorio_final.pdf"
    return [
        Check("report_pdf", pdf.exists() and pdf.stat().st_size > 1000,
              "Relatório PDF encontrado." if pdf.exists() else "Relatório PDF ausente."),
    ]


def collect(root: Path) -> dict[str, list[Check]]:
    config = load_json(root / "config/project.json")
    return {
        "bootstrap": bootstrap_checks(root, config),
        "dataset": dataset_checks(root, config),
        "training": training_checks(root, config),
        "evaluation": evaluation_checks(root, config),
        "publication": publication_checks(root, config),
        "final": final_checks(root),
    }


def stage_ok(checks: Iterable[Check]) -> bool:
    return all(check.ok for check in checks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mostra o estado verificável do projeto.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = collect(args.root.resolve())
    if args.json:
        print(json.dumps({k: [asdict(c) for c in v] for k, v in result.items()}, ensure_ascii=False, indent=2))
        return 0
    for stage, checks in result.items():
        mark = "OK" if stage_ok(checks) else "PENDENTE"
        print(f"\n[{mark}] {stage}")
        for check in checks:
            symbol = "✓" if check.ok else "✗"
            print(f"  {symbol} {check.key}: {check.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
