<!--
SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>

SPDX-License-Identifier: MIT
-->

<div style="text-align: center;">
  <img src="assets/banner.png" alt="Banner" style="display: block; margin: 0 auto;">
</div>

# Multimodal LUCAS

This repository provides code to assemble and curate a vision-language dataset from **LUCAS survey data** and **in-situ field photos**. [LUCAS](https://esdac.jrc.ec.europa.eu/projects/lucas) (Land Use/Cover Area Frame statistical Survey) is a land-monitoring exercise conducted by [EUROSTAT](https://ec.europa.eu/eurostat/web/main/home) in close cooperation with the Directorate-General responsible for Agriculture, with technical support from the Joint Research Centre ([JRC](https://commission.europa.eu/about/departments-and-executive-agencies/joint-research-centre_en)). The survey has been repeated every three years since 2006, and each time it has been conducted in the EU member states in place at that point in time. The latest iteration was run in 2022 across all EU-27 member states.

## Installation

Requires Python3.12+.

```shell
git clone git@github.com:stemauro/multimodal-lucas.git && cd multimodal-lucas
uv sync --all-groups --extra dev
```

## Repository structure

```shell
multimodal-lucas/
├── LICENSES
│   └── MIT.txt
├── README.md
├── assets
├── data
│   ├── processed
│   │   └── 2022
│   │       ├── data-00000-of-00001.arrow
│   │       ├── dataset_info.json
│   │       ├── manifest.jsonl
│   │       └── state.json
│   └── raw
│       └── EU_LUCAS_2022.csv
├── pyproject.toml
├── scripts
│   └── preprocess.py
├── src
│   └── multimodal_lucas
└── uv.lock
```
