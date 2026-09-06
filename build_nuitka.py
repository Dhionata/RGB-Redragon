"""Build standalone native Windows executable using Nuitka (C++ compilation).

Complies with SOLID & DRY principles, delegating build steps and process termination
to dedicated build_tools modules.
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is in sys.path for build_tools import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_tools.nuitka_builder import NuitkaBuilder


def main() -> int:
    parser = argparse.ArgumentParser(description="Nuitka C++ Native Builder")
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Build standalone directory instead of single compressed onefile (0 Static ML flags)",
    )
    args = parser.parse_args()
    builder = NuitkaBuilder(onefile=not args.standalone)
    return builder.run()


if __name__ == "__main__":
    sys.exit(main())
