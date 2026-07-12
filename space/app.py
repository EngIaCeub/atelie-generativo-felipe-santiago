from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

package_dir = Path(__file__).resolve().parent / "app"
spec = importlib.util.spec_from_file_location(
    "app",
    package_dir / "__init__.py",
    submodule_search_locations=[str(package_dir)],
)
if spec is None or spec.loader is None:
    raise RuntimeError("Pacote da aplicacao ausente.")
package = importlib.util.module_from_spec(spec)
sys.modules["app"] = package
spec.loader.exec_module(package)

from app.app import demo

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=1).launch()
