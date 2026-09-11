<!--
SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>

SPDX-License-Identifier: MIT
-->

> [!CAUTION]
> **This is the repository’s development branch and contains untested code**.
> Tested changes will be merged into the `main` branch over time.
> The code is provided for reproducibility, but use it at your own risk.

<h1>
  <img src="assets/banner.png" alt="Banner" style="width: 100%; display: block; margin: 0 auto;">

[![HuggingFace](https://img.shields.io/badge/Hugging_Face-stemauro/multimodal--lucas-FFD21E?logo=huggingface)](https://huggingface.co/datasets/stemauro/multimodal-lucas)

</h1>

This repository provides code to assemble and curate a vision-language dataset from **LUCAS survey data** and **in-situ field photos**. [LUCAS](https://esdac.jrc.ec.europa.eu/projects/lucas) (Land Use/Cover Area Frame statistical Survey) is a land-monitoring exercise conducted by [EUROSTAT](https://ec.europa.eu/eurostat/web/main/home) in close cooperation with the Directorate-General responsible for Agriculture, with technical support from the Joint Research Centre ([JRC](https://commission.europa.eu/about/departments-and-executive-agencies/joint-research-centre_en)). The survey has been repeated every three years since 2006, and each time it has been conducted in the EU member states in place at that point in time. The latest iteration was run in 2022 across all EU-27 member states.

## Installation

Requires Python3.12+.

```shell
git clone --branch develop git@github.com:stemauro/multimodal-lucas.git &&
cd multimodal-lucas && 
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
│   │   └── {{survey_year}}
│   │       ├── data-00000-of-00001.arrow
│   │       ├── dataset_info.json
│   │       ├── manifest.jsonl
│   │       └── state.json
│   └── raw
│       └── EU_LUCAS_{{survey_year}}.csv
├── pyproject.toml
├── scripts
├── src
│   └── multimodal_lucas
├── tests
└── uv.lock
```

## License

The LUCAS data and field photos are available from EUROSTAT under its free-reuse policy and may be reused with appropriate attribution. The data-curation code in this repository is released under a permissive [MIT License](LICENSES/MIT.txt).
