#!/usr/bin/env python3
"""CLI: Run all structural and consistency checks on the vault.

Usage:
    python scripts/validate_vault.py --vault ./vault --output ./outputs/validation_report.md
"""

import sys
from pathlib import Path

import click


@click.command()
@click.option("--vault", default="./vault", help="Path to the vault directory.")
@click.option("--output", default="./outputs/validation_report.md", help="Path for the validation report.")
def main(vault: str, output: str) -> None:
    """Run all structural and consistency validation checks."""
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from engine.parser import parse_vault
    from engine.validator import run_full_validation, generate_validation_report

    vault_path = Path(vault).resolve()
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    click.echo(f"Parsing vault at: {vault_path}")
    parsed_data = parse_vault(str(vault_path))

    click.echo("Running validation checks...")
    results = run_full_validation(
        parsed_data["graph"],
        parsed_data["holon_hierarchy"],
        parsed_data,
        str(vault_path),
    )

    # Print summary
    summary = results.get("summary", {})
    click.echo(f"\nValidation Results:")
    click.echo(f"  Total checks: {summary.get('total_checks', 0)}")
    click.echo(f"  Passed: {summary.get('passed', 0)}")
    click.echo(f"  Failed: {summary.get('failed', 0)}")
    click.echo(f"  Pass rate: {summary.get('pass_rate', 0):.0%}")

    # Print individual check results
    click.echo("\nDetailed Results:")
    for check_name, check_result in results.items():
        if check_name == "summary":
            continue
        status = "PASS" if check_result.get("passed", False) else "FAIL"
        message = check_result.get("message", "")
        click.echo(f"  [{status}] {check_name}: {message}")

    # Generate and save report
    report = generate_validation_report(results)
    output_path.write_text(report, encoding="utf-8")
    click.echo(f"\nFull report saved to: {output_path}")


if __name__ == "__main__":
    main()
