"""
compute_metrics.py
------------------
Computes evaluation metrics for all four pipeline configurations from the
thesis: "Context-Aware Document-Level Location Selection for Finnish News Articles"

Metrics computed:
- Exact match accuracy  : system location name == human annotation
- Level match accuracy  : system geographic level == human level
- City match accuracy   : system city == human city (postal-level articles only)

Usage:
    python compute_metrics.py

Requirements:
    pip install pandas
"""

import pandas as pd
import os

# ── Configuration files ──────────────────────────────────────────────────────

CONFIGS = [
    {
        "name": "Config 1 — Static Baseline",
        "file": "ranking_experiment_static_baseline.csv",
    },
    {
        "name": "Config 2 — Static + Postal-First",
        "file": "ranking_experiment_static_postal_first.csv",
    },
    {
        "name": "Config 3 — GeoAPI + Postal-First",
        "file": "ranking_experiment_geoapi_postal_first.csv",
    },
    {
        "name": "Config 4 — Full Hybrid (GeoAPI + Postal-First + MCP)",
        "files": [
            "19_MCP_ranking_experiment_geoapi_postal_first.csv",
            "41_MCP_articles-ranking_experiment_geoapi_postal_first.csv",
        ],
    },
]

# ── Helper functions ─────────────────────────────────────────────────────────

def load_config(config):
    """Load a single or combined CSV for a configuration."""
    if "file" in config:
        path = config["file"]
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found — skipping")
            return None
        return pd.read_csv(path)
    else:
        parts = []
        for f in config["files"]:
            if not os.path.exists(f):
                print(f"  WARNING: {f} not found — skipping")
                continue
            parts.append(pd.read_csv(f))
        if not parts:
            return None
        combined = pd.concat(parts, ignore_index=True)
        # Drop empty rows and duplicate article IDs
        combined = combined.dropna(subset=["article_id"])
        combined = combined.drop_duplicates(subset=["article_id"])
        return combined


def compute_metrics(df):
    """Compute exact match, level match, and city match from a results dataframe."""
    total = len(df)
    if total == 0:
        return None

    exact = df["match"].sum()
    level = df["level_match"].sum()

    # City match — only articles where human_city is provided
    city_rows = df[df["human_city"].notna() & (df["human_city"].astype(str).str.strip() != "")]
    city_total = len(city_rows)
    city_correct = city_rows["city_match"].sum() if city_total > 0 else 0

    return {
        "total": total,
        "exact_correct": int(exact),
        "exact_pct": round(exact / total * 100, 2),
        "level_correct": int(level),
        "level_pct": round(level / total * 100, 2),
        "city_total": city_total,
        "city_correct": int(city_correct),
        "city_pct": round(city_correct / city_total * 100, 2) if city_total > 0 else None,
    }


def print_results(name, metrics):
    """Print formatted results for one configuration."""
    if metrics is None:
        print(f"\n{name}")
        print("  Could not compute metrics — missing files")
        return

    print(f"\n{name}")
    print(f"  Articles evaluated : {metrics['total']}")
    print(f"  Exact match        : {metrics['exact_correct']}/{metrics['total']} = {metrics['exact_pct']}%")
    print(f"  Level match        : {metrics['level_correct']}/{metrics['total']} = {metrics['level_pct']}%")
    if metrics["city_pct"] is not None:
        print(f"  City match         : {metrics['city_correct']}/{metrics['city_total']} = {metrics['city_pct']}%")
    else:
        print(f"  City match         : N/A")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Thesis Evaluation Results")
    print("Context-Aware Location Selection for Finnish News Articles")
    print("=" * 60)

    for config in CONFIGS:
        df = load_config(config)
        if df is not None:
            metrics = compute_metrics(df)
            print_results(config["name"], metrics)
        else:
            print(f"\n{config['name']}: skipped — missing files")

    print("\n" + "=" * 60)
    print("Notes:")
    print("  - Exact match: string comparison of system vs human location name")
    print("  - Level match: geographic level (POSTAL/CITY/PROVINCE/COUNTRY)")
    print("  - City match:  city component for postal-level articles only")
    print("  - Config 4 combines two partial MCP run files (19 + 41 articles)")
    print("=" * 60)
