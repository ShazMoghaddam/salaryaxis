"""
SalaryAxis — main.py
---------------------
Phase 1 CLI entry point. Fetches ONS data and runs the data pipeline.

Falls back to bundled ONS ASHE 2023 data automatically if NOMIS is unreachable.

Author:  Shaz Moghaddam · https://github.com/ShazMoghaddam/salaryaxis
Copyright (c) 2026 Shaz Moghaddam. Licensed under MIT.

Run:
    python3 main.py
"""

import logging
import sys

from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from utils.logger  import setup_logging, console
from config import DEFAULT_YEAR

setup_logging("INFO")
logger = logging.getLogger(__name__)


def display_occupation_summary(df) -> None:
    table = Table(
        title=f"[bold]UK Median Annual Salary by Occupation — {DEFAULT_YEAR}[/bold]",
        show_header=True, header_style="bold cyan", border_style="dim",
    )
    table.add_column("SOC",      style="dim",  width=5)
    table.add_column("Occupation",              min_width=40)
    table.add_column("Median (£)",  justify="right", style="green")
    table.add_column("P25 (£)",     justify="right", style="yellow")
    table.add_column("P75 (£)",     justify="right", style="yellow")

    for _, row in df.iterrows():
        table.add_row(
            str(row.get("occupation_code", "—")),
            str(row.get("occupation_label", "—"))[:48],
            f"{int(row['median_salary']):,}",
            f"{int(row['p25_salary']):,}",
            f"{int(row['p75_salary']):,}",
        )
    console.print(table)


def display_region_summary(df) -> None:
    table = Table(
        title=f"[bold]UK Median Salary by Region — {DEFAULT_YEAR}[/bold]",
        show_header=True, header_style="bold magenta", border_style="dim",
    )
    table.add_column("Region",       min_width=20)
    table.add_column("Median (£)",   justify="right", style="green")
    table.add_column("Mean (£)",     justify="right", style="yellow")

    for _, row in df.iterrows():
        table.add_row(
            str(row.get("geography", "—")),
            f"{int(row['median_salary']):,}",
            f"{int(row['mean_salary']):,}",
        )
    console.print(table)


def main() -> int:
    console.rule("[bold cyan]SalaryAxis — Data Pipeline")

    # ── Step 1: Try live NOMIS fetch ─────────────────────────────────────────
    console.print("\n[bold]Step 1 of 3:[/bold] Fetching ONS/NOMIS data...\n")

    occ_df = None
    reg_df = None
    source = "nomis_live"

    try:
        from data.ons_fetcher import ONSFetcher
        fetcher = ONSFetcher()
        occ_df  = fetcher.fetch_ashe_time_series(geography="UK", sex="all")
        if occ_df.empty:
            raise RuntimeError("NOMIS returned 0 rows.")
        reg_df  = fetcher.fetch_ashe_by_region(year=DEFAULT_YEAR, sex="all")
        logger.info("Live data: %d occupation rows, %d region rows", len(occ_df), len(reg_df))
    except Exception as exc:
        logger.warning("NOMIS unavailable (%s) — using bundled ONS ASHE 2023 data.", exc)
        source = "bundled_ons_2023"

    # ── Step 1b: Bundled fallback ────────────────────────────────────────────
    if source == "bundled_ons_2023":
        console.print(
            "[yellow]  NOMIS API unreachable — loading bundled ONS ASHE 2023 data.[/yellow]\n"
            "  [dim]This is real published ONS data, not estimates.[/dim]\n"
        )
        from data.bundled_data import (
            get_occupation_summary, get_region_summary,
            get_trends, get_clean_combined,
        )
        import pathlib, pandas as pd
        out = pathlib.Path("output")
        out.mkdir(exist_ok=True)

        occ_summary = get_occupation_summary()
        reg_summary = get_region_summary()
        trends      = get_trends()
        clean       = get_clean_combined()

        occ_summary.to_csv(out / "occupation_summary.csv", index=False)
        reg_summary.to_csv(out / "region_summary.csv",     index=False)
        trends.to_csv(out      / "salary_trends.csv",      index=False)
        clean.to_csv(out       / "clean_combined.csv",     index=False)

        logger.info("Bundled data written to output/")

        console.print()
        console.print("[bold]Step 2 of 3:[/bold] Pipeline (bundled data — skipping)\n")
        console.print("[bold]Step 3 of 3:[/bold] Results\n")
        display_occupation_summary(occ_summary)
        console.print()
        display_region_summary(reg_summary)
        console.print()
        console.print(Panel(
            f"[green]✓[/green] Pipeline complete.\n"
            f"  Source: [bold]ONS ASHE 2023 (bundled)[/bold]\n"
            f"  Occupation groups: [bold]{len(occ_summary)}[/bold]\n"
            f"  Regions: [bold]{len(reg_summary)}[/bold]\n"
            f"  Output files: [bold]output/[/bold] (CSV)",
            title="[bold cyan]SalaryAxis — Pipeline Summary",
            border_style="cyan",
        ))
        return 0

    # ── Step 2: Run pipeline on live data ────────────────────────────────────
    console.print("\n[bold]Step 2 of 3:[/bold] Running data pipeline...\n")

    from pipeline.processor import SalaryPipeline
    pipeline = SalaryPipeline()
    results  = pipeline.run(occupation_df=occ_df, region_df=reg_df)

    # ── Step 3: Display ───────────────────────────────────────────────────────
    console.print("\n[bold]Step 3 of 3:[/bold] Results\n")

    occ_summary = results["occupation_summary"]
    reg_summary = results["region_summary"]
    trends      = results["trends"]

    if not occ_summary.empty:
        display_occupation_summary(occ_summary)
    if not reg_summary.empty:
        console.print(); display_region_summary(reg_summary)

    console.print()
    console.print(Panel(
        f"[green]✓[/green] Pipeline complete.\n"
        f"  Source: [bold]NOMIS live API[/bold]\n"
        f"  Clean records:     [bold]{len(results['clean']):,}[/bold]\n"
        f"  Occupation groups: [bold]{len(occ_summary)}[/bold]\n"
        f"  Regions:           [bold]{len(reg_summary)}[/bold]\n"
        f"  Years covered:     [bold]{trends['year'].nunique() if not trends.empty else 0}[/bold]\n"
        f"  Output files: [bold]output/[/bold] (CSV + Parquet)",
        title="[bold cyan]SalaryAxis — Pipeline Summary",
        border_style="cyan",
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
