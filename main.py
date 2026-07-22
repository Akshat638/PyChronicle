"""
PyChronicle - CLI Entry Point (Week 1 + Week 2 deliverables)

Usage:
    python main.py sample/test.py --show-ast
    python main.py sample/test.py
    python ui/app.py                (launch the Week 2 TUI scaffold)
"""

import argparse

from parser.ast_parser import parse_python_file
from tracer.execution_tracer import run_and_trace


def main():
    arg_parser = argparse.ArgumentParser(
        description="PyChronicle - AST-Powered Time-Travel Debugger"
    )
    arg_parser.add_argument("file", help="Path to the Python script to trace")
    arg_parser.add_argument(
        "--show-ast",
        action="store_true",
        help="Show variable assignments detected via static AST parsing",
    )
    args = arg_parser.parse_args()

    if args.show_ast:
        variables = parse_python_file(args.file)
        print("Detected variable assignments (static AST scan):")
        for v in variables:
            print(f"  Line {v['line']}: {v['variable']} = {v['value']}")
        print()

    print(f"Tracing execution of {args.file} ...\n")
    history = run_and_trace(args.file)
    print(f"\nCaptured {len(history)} variable state snapshots into pychronicle.db")


if __name__ == "__main__":
    main()
