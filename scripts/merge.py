# SPDX-FileCopyrightText: 2026 Stefano Maurogiovanni <s.maurogiovanni@gmx.de>
#
# SPDX-License-Identifier: MIT

"""Merge LUCAS datasets from multiple years and push to hub."""

import os

from datasets import concatenate_datasets, load_from_disk
from dotenv import load_dotenv

from multimodal_lucas import project_root
from multimodal_lucas.config import LUCAS_YEARS


def main() -> None:
    load_dotenv()

    data_dir = project_root / "data" / "processed"

    dataset_paths = filter(lambda path: path.stem in LUCAS_YEARS, data_dir.iterdir())
    dataset = concatenate_datasets([load_from_disk(path) for path in dataset_paths])  # ty: ignore[invalid-argument-type]

    # Re-index merged datasets
    index_name = "index"
    index_type = dataset.features[index_name]
    dataset = dataset.remove_columns(index_name).add_column(
        name=index_name, column=list(range(len(dataset))), feature=index_type
    )

    dataset = dataset.select_columns(
        [index_name] + [name for name in dataset.column_names if name != index_name]
    )

    dataset.push_to_hub(
        repo_id="stemauro/multimodal-lucas",
        token=os.getenv("HF_WRITE_TOKEN"),
        commit_message="feat(data): merge yearly datasets",
        commit_description="Merge year-specific datasets and reindex rows accordingly.",
    )


if __name__ == "__main__":
    main()
