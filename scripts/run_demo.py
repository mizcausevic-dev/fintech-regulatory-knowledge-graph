from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.graph_service import graph_service


def main() -> None:
    print("== Summary ==")
    print(json.dumps(graph_service.summary().model_dump(), indent=2))
    print("\n== Lead path ==")
    print(json.dumps(graph_service.path_between("stablecoin-sweep", "custody-control").model_dump(), indent=2))
    print("\n== JSON-LD keys ==")
    exported = graph_service.jsonld_export().data
    print(json.dumps({"type": exported["@type"], "graph_entries": len(exported["@graph"])}, indent=2))


if __name__ == "__main__":
    main()
