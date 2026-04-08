from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

from auto_poc.core import generate_report
from auto_poc.generator import DEFAULT_BACKEND, DEFAULT_MODEL, DEFAULT_PROVIDER


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Auto-PoC: HackerOne bug bounty report generator"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Path to input JSON file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Path to write output JSON (prints to stdout if omitted)",
    )
    parser.add_argument(
        "--backend", "-b",
        type=str,
        default=DEFAULT_BACKEND,
        choices=["cli", "api"],
        help=f"LLM backend: cli or api (default: {DEFAULT_BACKEND})",
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        default=DEFAULT_PROVIDER,
        help=f"CLI provider: claude or codex (default: {DEFAULT_PROVIDER})",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=DEFAULT_MODEL,
        help=f"API model for --backend api (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save report to projects directory",
    )

    args = parser.parse_args()

    # 입력 읽기
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            input_data = json.load(f)
    else:
        input_data = json.load(sys.stdin)

    # 보고서 생성
    report = generate_report(
        input_data=input_data,
        backend=args.backend,
        provider=args.provider,
        model=args.model,
        save=not args.no_save,
    )

    # 출력
    output_json = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output_json)
