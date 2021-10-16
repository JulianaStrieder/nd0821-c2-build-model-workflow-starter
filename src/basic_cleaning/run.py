#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    Get the input artifact, do some fixes and save as an output artifact.
    Args:
        pbf_args: necessary arguments
    """

    logger.info("Initiating NYC Airbnb Project")
    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading input artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df_original = pd.read_csv(artifact_local_path)

    logger.info("Drop outliers")
    min_price = 10
    max_price = 350
    idx = df_original["price"].between(min_price, max_price)
    df_original = df_original[idx].copy()

    logger.info("Convert last_review to datetime")
    df_original["last_review"] = pd.to_datetime(df_original["last_review"])

    df_original.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")

    logger.info("Logging artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Specifies the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Specifies the output artifact, name and format",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Specifies the file name for output",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of final artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Min Price Value",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Max Price Value",
        required=True
    )

    args = parser.parse_args()

    go(args)
