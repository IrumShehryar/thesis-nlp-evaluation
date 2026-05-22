# Thesis Evaluation Dataset & Results

**Context-Aware Document-Level Location Selection for Finnish News Articles: A Hybrid Rule-Based and LLM Approach**

Master's Thesis — Irum Shehryar
Metropolia University of Applied Sciences, May 2026
Grade: 5/5

📄 **Full thesis:** [URN:NBN:fi:amk-2026051311846](https://urn.fi/URN:NBN:fi:amk-2026051311846)

---

## Overview

This repository contains the evaluation dataset and results for a master's thesis that built and evaluated a four-configuration NLP pipeline for extracting and ranking geographic locations at postal-code granularity from Finnish news articles.

The pipeline was developed in collaboration with **Superhood Oy** — a Finnish neighbourhood-level news platform that processes around 80 Finnish news articles per day requiring manual postal-area location tagging.

---

## Repository Contents

| File | Description |
|---|---|
| `article_meta_data.json` | Ground truth annotations for 60 Finnish news articles |
| `ranking_experiment_static_baseline.csv` | Config 1 results — Static resolver + Baseline ranking |
| `ranking_experiment_static_postal_first.csv` | Config 2 results — Static resolver + Postal-first ranking |
| `ranking_experiment_geoapi_postal_first.csv` | Config 3 results — GeoAPI resolver + Postal-first ranking |
| `19_MCP_ranking_experiment_geoapi_postal_first.csv` | Config 4 partial — MCP applied to 19 incorrect GeoAPI predictions |
| `41_MCP_articles-ranking_experiment_geoapi_postal_first.csv` | Config 4 partial — MCP applied to 41 correct GeoAPI predictions |
| `compute_metrics.py` | Script to reproduce all evaluation metrics |

---

## Dataset

The dataset consists of 60 publicly available Finnish news articles collected from Yle, Finnish police (poliisi.fi), and Finnish municipal websites. Articles cover seven categories:

- Traffic and Street Work
- Local News
- Authority Info
- Culture and Music
- Sports and Fitness
- City or Municipality
- Authority Alerts

Each article is annotated with:
- **human_correct** — the primary location name representing the geographic scope of the article
- **human_level** — geographic level: POSTAL, CITY, PROVINCE, or COUNTRY
- **human_city** — parent city for postal-level articles

---

## Four Pipeline Configurations

| Configuration | Resolver | Ranking | Description |
|---|---|---|---|
| Config 1 | Static dictionary | Baseline | Rule-based, no geographic hierarchy |
| Config 2 | Static dictionary | Postal-first | Hierarchical ranking — postal > city > province |
| Config 3 | Geoapify API | Postal-first | Dynamic geocoding replaces static dictionary |
| Config 4 | Geoapify API | Postal-first + MCP | LLM contextual reasoning layer added on top |

The static dictionary contained 42 manually compiled Finnish postal area entries. The postal-first ranking strategy promotes the most specific geographic level when strong signals are present — title mention, frequency ≥ 2, or position ≤ 3. Configuration 4 used Llama 3.3 70B via Groq through Model Context Protocol (MCP) for document-level contextual disambiguation.

---

## Results

| Configuration | Exact Match | Level Match | City Match |
|---|---|---|---|
| Config 1 — Static Baseline | 40/60 = 66.67% | 43/60 = 71.67% | 22/29 = 75.86% |
| Config 2 — Static + Postal-First | 48/60 = 80.00% | 51/60 = 85.00% | 24/29 = 82.76% |
| Config 3 — GeoAPI + Postal-First | 41/60 = 68.33% | 47/60 = 78.33% | 22/29 = 75.86% |
| Config 4 — Full Hybrid + MCP | 50/60 = 83.33% | 47/60 = 78.33% | 20/29 = 68.97% |

**Key findings:**
- Postal-first ranking produced the single largest gain — +13.33 percentage points over baseline
- GeoAPI reduced accuracy despite broader coverage due to noisy candidates (POIs, street addresses)
- MCP corrected 11 of 19 GeoAPI errors including one case where it inferred a location absent from the candidate list
- MCP introduced 2 regressions — overriding correct ranking decisions with contextually plausible but incorrect selections
- The data coverage gap in Finnish NER training corpora — not tool architecture — is the primary bottleneck for postal-level location extraction

---

## Evaluation Metrics

Three binary metrics were used:

- **Exact match** — system location name matches human annotation exactly (string comparison)
- **Level match** — system geographic level matches human annotation
- **City match** — system city matches human annotation (postal-level articles only)

Note: exact string matching penalised geographically correct answers where the system returned an equivalent name in a different language — e.g. Finland vs Suomi, Hedenäset vs Hietaniemi. Fuzzy matching would yield higher effective accuracy.

---

## Reproducing Results
**Step 1 — Clone the repository:**
git clone https://github.com/IrumShehryar/thesis-nlp-evaluation
cd thesis-nlp-evaluation
**Step 2 — Install dependencies:**
pip install pandas
**Step 3 — Run the evaluation script:**
python compute_metrics.py

This will print exact match, level match, and city match accuracy for all four pipeline configurations.

---

## Citation

If you use this dataset or evaluation results in your research please cite:

```
Shehryar, I. (2026). Context-Aware Document-Level Location Selection for 
Finnish News Articles: A Hybrid Rule-Based and LLM Approach. 
Master's Thesis, Metropolia University of Applied Sciences.
URN:NBN:fi:amk-2026051311846
```

---

## License

The evaluation dataset (article_meta_data.json) and evaluation scripts are released under the MIT License.

The article texts are not included in this repository. All articles are publicly accessible via the URLs provided in article_meta_data.json.
