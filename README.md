# Thesis Evaluation Dataset & Results

**Context-Aware Document-Level Location Selection for Finnish News Articles: A Hybrid Rule-Based and LLM Approach**

Master's Thesis — Irum Shehryar  
Metropolia University of Applied Sciences, May 2026  
Grade: 5/5

📄 **Full thesis:** [URN:NBN:fi:amk-2026051311846](https://urn.fi/URN:NBN:fi:amk-2026051311846)

---

## Overview

This repository contains the evaluation dataset and results for a master's thesis that built and evaluated a four-configuration NLP pipeline for extracting and ranking geographic locations at postal level from Finnish news articles.

The pipeline was developed in collaboration with **Superhood Oy** — a Finnish neighbourhood-level news platform.

---

## Repository Contents

| File/Folder                | Description                                                       |
|----------------------------|-------------------------------------------------------------------|
| `evaluation/`              | Contains all evaluation data files and scripts                    |
| `evaluation/article_meta_data.json` | Ground truth annotations for 60 Finnish news articles      |
| `evaluation/ranking_experiment_static_baseline.csv` | Config 1 results — Static resolver + Baseline ranking |
| `evaluation/ranking_experiment_static_postal_first.csv` | Config 2 results — Static resolver + Postal-first ranking |
| `evaluation/ranking_experiment_geoapi_postal_first.csv` | Config 3 results — GeoAPI resolver + Postal-first ranking |
| `evaluation/19_MCP_ranking_experiment_geoapi_postal_first.csv` | Config 4 partial — MCP applied to 19 incorrect GeoAPI predictions |
| `evaluation/41_MCP_articles-ranking_experiment_geoapi_postal_first.csv` | Config 4 partial — MCP applied to 41 correct GeoAPI predictions |
| `evaluation/compute_metrics.py`      | Script to reproduce all evaluation metrics                 |
| `diagram/`                  | Diagrams related to the pipeline architecture or results         |

---

## Dataset

The dataset consists of 60 publicly available Finnish news articles collected from Yle, Finnish police (poliisi.fi), and Finnish municipal websites. Article categories include Traffic and Street Works, Crime, Weather, and Local News.

Each article is annotated with:
- **human_correct** — the primary location name representing the geographic scope of the article
- **human_level** — geographic level: POSTAL, CITY, PROVINCE, or COUNTRY
- **human_city** — parent city for postal-level articles

---

## Four Pipeline Configurations

| Configuration | Resolver         | Ranking           | Description |
|---------------|-----------------|-------------------|-------------|
| Config 1      | Static dictionary | Baseline         | Rule-based, no geographic hierarchy |
| Config 2      | Static dictionary | Postal-first     | Hierarchical ranking — postal > city > province |
| Config 3      | Geoapify API      | Postal-first     | Dynamic geocoding replaces static dictionary |
| Config 4      | Geoapify API      | Postal-first + MCP| LLM contextual reasoning layer added on top   |

---

## Results

![Postal-Level Location Extraction Results](diagram/results-graph.PNG)

| Configuration                | Exact Match         | Level Match         | City Match              |
|------------------------------|---------------------|---------------------|-------------------------|
| Config 1 — Static Baseline   | 40/60 = 66.67%      | 43/60 = 71.67%      | 22/29 = 75.86%          |
| Config 2 — Static + Postal-First | 48/60 = 80.00%  | 51/60 = 85.00%      | 24/29 = 82.76%          |
| Config 3 — GeoAPI + Postal-First | 41/60 = 68.33%  | 47/60 = 78.33%      | 22/29 = 75.86%          |
| Config 4 — Full Hybrid + MCP     | 50/60 = 83.33%  | 47/60 = 78.33%      | 20/29 = 68.97%          |

**Key findings:**
- Postal-first ranking produced the largest gain (+13.33 percentage points over baseline).
- GeoAPI reduced accuracy despite broader coverage due to noisy candidate locations.
- MCP corrected 11 of 19 GeoAPI errors, including one case with an inferred location not in the candidate list.
- MCP introduced 2 regressions from contextually plausible but incorrect selections.
- The main bottleneck is coverage in Finnish NER corpora, not the tool architecture.

---

## Evaluation Metrics

Three binary metrics were used:

- **Exact match** — System location name matches human annotation exactly.
- **Level match** — System geographic level matches human annotation.
- **City match** — System city matches human annotation (postal-level articles only).

*Note: Exact string matching penalized geographically correct answers with language variants (e.g., "Finland" vs "Suomi").*

---

## Reproducing Results

**Step 1 — Clone the repository:**

```bash
git clone https://github.com/IrumShehryar/thesis-nlp-evaluation
cd thesis-nlp-evaluation
```

**Step 2 — Install dependencies:**

```bash
pip install pandas
```

**Step 3 — Run the evaluation script:**

```bash
python evaluation/compute_metrics.py
```

This will print the exact match, level match, and city match accuracy for all four pipeline configurations.

---

## Citation

If you use this dataset or evaluation results in your research, please cite:

```
Shehryar, I. (2026). Context-Aware Document-Level Location Selection for 
Finnish News Articles: A Hybrid Rule-Based and LLM Approach. 
Master's Thesis, Metropolia University of Applied Sciences.
URN:NBN:fi:amk-2026051311846
```

---

## License

The evaluation dataset and scripts are released under the MIT License.

The article texts are not included in this repository. All articles are publicly accessible via the URLs provided in `evaluation/article_meta_data.json`.
