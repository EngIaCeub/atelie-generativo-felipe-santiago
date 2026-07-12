import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = path.join(ROOT, "relatorio");
const QA_DIR = path.join(ROOT, "resultados", "demoday_huggingface", "_deck_preview");
const FINAL_PPTX = path.join(OUT_DIR, "entrega_recomendada_demoday.pptx");
const evidenceImage = path.join(
  ROOT,
  "resultados",
  "demoday_huggingface",
  "prints_imagens_tempos.png",
);
const comparisonGrid = path.join(ROOT, "resultados", "avaliacao", "grade_comparativa.png");
const evidenceJson = JSON.parse(
  await fs.readFile(
    path.join(ROOT, "resultados", "demoday_huggingface", "evidencias_geracao_huggingface.json"),
    "utf8",
  ),
);

const links = {
  repo: "https://github.com/EngIaCeub/atelie-generativo-felipe-santiago/tree/agent/finalizar-entrega-academica",
  space: "https://huggingface.co/spaces/RalphError/atelie-xilogravura-cerrado",
  app: "https://ralpherror-atelie-xilogravura-cerrado.hf.space",
  lora: "https://huggingface.co/RalphError/flpxilobr-lora",
};

const deck = Presentation.create({
  slideSize: { width: 1280, height: 720 },
});

const colors = {
  canvas: "#FFFFFF",
  ink: "#111111",
  muted: "#525252",
  panel: "#EFEFEF",
  rule: "#B8BCC4",
  accent: "#3D8DFF",
  pale: "#F7F7F7",
};

function addText(slide, text, left, top, width, height, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: opts.fontSize ?? 22,
    bold: opts.bold ?? false,
    color: opts.color ?? colors.ink,
    alignment: opts.alignment ?? "left",
  };
  return shape;
}

function addPanel(slide, left, top, width, height, fill = colors.panel) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height },
    fill,
    line: { style: "solid", fill: colors.rule, width: 1 },
  });
}

function addHeader(slide, title, eyebrow = "Atelie Generativo") {
  addText(slide, eyebrow, 56, 34, 400, 30, {
    fontSize: 16,
    bold: true,
    color: colors.muted,
  });
  addText(slide, title, 56, 72, 1080, 92, {
    fontSize: 42,
    bold: true,
  });
  slide.shapes.add({
    geometry: "rect",
    position: { left: 56, top: 158, width: 1168, height: 1.5 },
    fill: colors.rule,
    line: { style: "solid", fill: colors.rule, width: 0 },
  });
}

function addFooter(slide, index) {
  addText(slide, String(index), 1190, 666, 44, 24, {
    fontSize: 14,
    color: colors.muted,
    alignment: "right",
  });
}

async function addImage(slide, file, left, top, width, height, alt, fit = "contain") {
  const bytes = await fs.readFile(file);
  slide.images.add({
    blob: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    contentType: "image/png",
    alt,
    fit,
    position: { left, top, width, height },
  });
}

function bulletLines(items) {
  return items.map((item) => `- ${item}`).join("\n");
}

// Slide 1
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addText(slide, "Entrega academica consolidada", 56, 82, 900, 80, {
    fontSize: 58,
    bold: true,
  });
  addText(
    slide,
    "Atelie Generativo - Felipe Santiago\nLoRA Stable Diffusion v1.5 para xilogravura digital do Cerrado",
    56,
    190,
    760,
    92,
    { fontSize: 25, color: colors.muted },
  );
  addPanel(slide, 56, 370, 340, 126, colors.pale);
  addText(slide, "Repositorio final", 80, 395, 280, 30, { fontSize: 24, bold: true });
  addText(slide, "Branch final no GitHub", 80, 435, 290, 52, {
    fontSize: 20,
    color: colors.muted,
  });
  addPanel(slide, 440, 370, 340, 126, colors.pale);
  addText(slide, "App publicado", 464, 395, 280, 30, { fontSize: 24, bold: true });
  addText(slide, "Hugging Face Space publico", 464, 435, 290, 52, {
    fontSize: 20,
    color: colors.muted,
  });
  addPanel(slide, 824, 370, 340, 126, colors.pale);
  addText(slide, "Evidencias", 848, 395, 280, 30, { fontSize: 24, bold: true });
  addText(slide, "Relatorio, notebooks, metricas e prints", 848, 435, 290, 52, {
    fontSize: 20,
    color: colors.muted,
  });
  addText(slide, "Para envio no portal academico", 56, 616, 500, 26, {
    fontSize: 18,
    color: colors.muted,
  });
  addFooter(slide, 1);
}

// Slide 2
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addHeader(slide, "O projeto atende aos marcos esperados para avaliacao");
  const items = [
    ["Dataset", "24 imagens com proveniencia, licencas permitidas e captions revisadas."],
    ["Treino", "Duas configuracoes LoRA concluidas; config_b selecionada e publicada."],
    ["Avaliacao", "Grade base x LoRA, CLIPScore, memorizacao e avaliacao humana cega."],
    ["Aplicacao", "Pipeline texto -> imagem -> audio em Gradio no Hugging Face Space."],
  ];
  items.forEach(([label, body], idx) => {
    const x = 56 + (idx % 2) * 584;
    const y = 210 + Math.floor(idx / 2) * 176;
    addPanel(slide, x, y, 520, 130, colors.pale);
    addText(slide, label, x + 24, y + 20, 460, 34, { fontSize: 26, bold: true });
    addText(slide, body, x + 24, y + 62, 454, 48, { fontSize: 20, color: colors.muted });
  });
  addFooter(slide, 2);
}

// Slide 3
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addHeader(slide, "Links publicos e arquivos para colar no portal");
  const rows = [
    ["Repositorio GitHub", links.repo],
    ["Space Hugging Face", links.space],
    ["App do Space", links.app],
    ["Modelo LoRA", links.lora],
    ["Relatorio PDF", "relatorio/relatorio_final.pdf"],
    ["Notebooks", "notebooks/01_dataset.ipynb, 02_treino_lora.ipynb, 03_avaliacao.ipynb"],
  ];
  addPanel(slide, 56, 190, 1168, 420, "#FFFFFF");
  rows.forEach(([label, value], idx) => {
    const y = 210 + idx * 62;
    if (idx > 0) {
      slide.shapes.add({
        geometry: "rect",
        position: { left: 76, top: y - 14, width: 1128, height: 1 },
        fill: colors.rule,
        line: { style: "solid", fill: colors.rule, width: 0 },
      });
    }
    addText(slide, label, 86, y, 260, 30, { fontSize: 22, bold: true });
    addText(slide, value, 370, y, 790, 36, { fontSize: 17, color: colors.muted });
  });
  addFooter(slide, 3);
}

// Slide 4
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addHeader(slide, "Geracoes remotas no Hugging Face foram registradas");
  await addImage(
    slide,
    evidenceImage,
    56,
    188,
    760,
    456,
    "Painel com duas imagens geradas no Hugging Face Space e seus tempos de processamento",
    "contain",
  );
  addPanel(slide, 850, 188, 374, 456, colors.pale);
  addText(slide, "Chamadas registradas", 878, 216, 300, 32, { fontSize: 25, bold: true });
  addText(
    slide,
    bulletLines([
      `${evidenceJson[0].theme}: ${evidenceJson[0].latency_seconds} s`,
      `${evidenceJson[1].theme}: ${evidenceJson[1].latency_seconds} s`,
      "Endpoint: /gerar",
      "Status: Concluido nas duas chamadas",
      "Arquivos: PNG, WAV, JSON e painel visual",
    ]),
    878,
    274,
    306,
    248,
    { fontSize: 19, color: colors.ink },
  );
  addText(slide, "Pasta: resultados/demoday_huggingface", 878, 572, 310, 34, {
    fontSize: 17,
    color: colors.muted,
  });
  addFooter(slide, 4);
}

// Slide 5
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addHeader(slide, "Avaliacao e contingencia sustentam a demonstracao");
  await addImage(
    slide,
    comparisonGrid,
    56,
    188,
    620,
    410,
    "Grade comparativa base versus LoRA",
    "contain",
  );
  addPanel(slide, 720, 188, 504, 410, colors.pale);
  addText(slide, "Como apresentar", 748, 216, 380, 32, { fontSize: 25, bold: true });
  addText(
    slide,
    bulletLines([
      "Abrir o Space antes da fala e usar 2 prompts curtos.",
      "Avisar que CPU Basic tem latencia alta.",
      "Se o Space demorar, mostrar as evidencias offline como contingencia.",
      "Nao apresentar prints ou audios como execucao ao vivo.",
    ]),
    748,
    276,
    420,
    210,
    { fontSize: 20, color: colors.ink },
  );
  addText(slide, "Evidencia adicional: resultados/avaliacao/grade_comparativa.png", 748, 548, 420, 36, {
    fontSize: 16,
    color: colors.muted,
  });
  addFooter(slide, 5);
}

// Slide 6
{
  const slide = deck.slides.add();
  slide.background.fill = colors.canvas;
  addHeader(slide, "Checklist final para submissao");
  const checklist = [
    "Anexar este PPTX como apresentacao da entrega.",
    "Informar o link da branch final do GitHub.",
    "Informar Space, App e modelo LoRA no Hugging Face.",
    "Anexar ou apontar o relatorio_final.pdf.",
    "Manter a pasta demoday_huggingface como evidencia de demonstracao.",
    "Confirmar com o professor se a entrega deve estar na branch main.",
  ];
  addText(slide, bulletLines(checklist), 84, 210, 860, 330, {
    fontSize: 25,
    color: colors.ink,
  });
  addPanel(slide, 984, 210, 240, 240, colors.pale);
  addText(slide, "Validado", 1012, 250, 180, 36, { fontSize: 28, bold: true });
  addText(slide, "project_status.py\ncheck_secrets.py\nvalidate final", 1012, 310, 180, 104, {
    fontSize: 22,
    color: colors.muted,
  });
  addText(slide, "Entrega individual: Felipe Santiago", 84, 604, 500, 30, {
    fontSize: 22,
    bold: true,
  });
  addFooter(slide, 6);
}

await fs.mkdir(OUT_DIR, { recursive: true });
await fs.mkdir(QA_DIR, { recursive: true });

for (const [idx, slide] of deck.slides.items.entries()) {
  const stem = `slide-${String(idx + 1).padStart(2, "0")}`;
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(QA_DIR, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(QA_DIR, `${stem}.layout.json`), await layout.text());
}

const montage = await deck.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(QA_DIR, "montage.webp"), new Uint8Array(await montage.arrayBuffer()));

const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(FINAL_PPTX);
console.log(FINAL_PPTX);
