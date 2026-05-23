"""
Compute inter-annotator agreement between Rituparno's annotations
and the BLP-2023 gold standard labels.

Author: Rituparno Majumdar
"""

import csv
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table

console = Console()


def load_csv(path: Path, label_col: str) -> dict:
    data = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["id"]] = row[label_col].strip()
    return data


def cohen_kappa(gold: list, pred: list, labels: list) -> float:
    n = len(gold)
    if n == 0:
        return 0.0

    # Observed agreement
    p_o = sum(g == p for g, p in zip(gold, pred)) / n

    # Expected agreement
    p_e = sum(
        (gold.count(label) / n) * (pred.count(label) / n)
        for label in labels
    )

    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def accuracy(gold: list, pred: list) -> float:
    if not gold:
        return 0.0
    return sum(g == p for g, p in zip(gold, pred)) / len(gold)


@click.command()
@click.option("--gold", default="data/gold_sample.csv", show_default=True,
              help="Path to gold labels CSV")
@click.option("--annotations", default="data/my_annotations.csv", show_default=True,
              help="Path to your annotations CSV")
@click.option("--output", default="data/results_summary.csv", show_default=True,
              help="Path to save merged results CSV")
def main(gold, annotations, output):
    """Compute Cohen's Kappa and accuracy against the BLP-2023 gold standard."""

    gold_path = Path(gold)
    ann_path = Path(annotations)

    if not gold_path.exists():
        console.print(f"[red]Gold file not found: {gold_path}[/red]")
        raise SystemExit(1)
    if not ann_path.exists():
        console.print(f"[red]Annotations file not found: {ann_path}[/red]")
        raise SystemExit(1)

    gold_data = load_csv(gold_path, "gold_label")
    ann_data = load_csv(ann_path, "your_label")

    # Match on id
    common_ids = sorted(set(gold_data) & set(ann_data))
    missing_annotations = [i for i in common_ids if not ann_data[i]]

    if missing_annotations:
        console.print(
            f"[yellow]Warning: {len(missing_annotations)} items have empty annotations "
            f"(ids: {missing_annotations[:5]}{'...' if len(missing_annotations) > 5 else ''})[/yellow]"
        )
        common_ids = [i for i in common_ids if ann_data[i]]

    gold_labels = [gold_data[i] for i in common_ids]
    pred_labels = [ann_data[i] for i in common_ids]
    label_set = ["Positive", "Negative", "Neutral"]

    kappa = cohen_kappa(gold_labels, pred_labels, label_set)
    acc = accuracy(gold_labels, pred_labels)

    # Per-class breakdown
    table = Table(title="Results: Your Annotations vs. BLP-2023 Gold Standard")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Items compared", str(len(common_ids)))
    table.add_row("Accuracy", f"{acc:.1%}")
    table.add_row(
        "Cohen's Kappa",
        f"{kappa:.3f}  {'✅ above threshold (≥0.70)' if kappa >= 0.70 else '⚠️ below threshold (<0.70)'}",
    )

    # Per-label stats
    table.add_section()
    for label in label_set:
        gold_count = gold_labels.count(label)
        pred_count = pred_labels.count(label)
        correct = sum(g == p == label for g, p in zip(gold_labels, pred_labels))
        table.add_row(
            f"{label} — correct / gold / predicted",
            f"{correct} / {gold_count} / {pred_count}",
        )

    console.print(table)

    # Save merged results
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "gold_label", "your_label", "match"])
        with open(gold_path, encoding="utf-8") as gf:
            gold_rows = {r["id"]: r for r in csv.DictReader(gf)}
        for i in common_ids:
            match = "✓" if gold_data[i] == ann_data[i] else "✗"
            writer.writerow([i, gold_rows[i]["text"], gold_data[i], ann_data[i], match])

    console.print(f"\n[green]Merged results saved to {output_path}[/green]")
    console.print(
        "\n[dim]Disagreements to analyse: "
        f"{sum(g != p for g, p in zip(gold_labels, pred_labels))} items[/dim]"
    )


if __name__ == "__main__":
    main()
