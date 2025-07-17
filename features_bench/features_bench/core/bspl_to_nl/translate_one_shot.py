import argparse
from pathlib import Path
import logging

from features_bench.__init__ import logger
from features_bench.core.base._01_parse import load_parse
from features_bench.core.bspl_to_nl.__init__ import query_context


def main(model: str):
    """
    Run one-shot translations on `training_pairs.json` data
    """
    logger_with_model = logger.bind(model=model)

    component = f"{'/'.join(Path(__file__).parts[-2:])}"
    context_content = open(Path(__file__).parent / "_context.txt", mode="r").read()

    # One-shot test
    for i, (p, _) in enumerate(load_parse()):
        logger_with_model.info(f"------------- {model} ({i}) ----------------")
        logger_with_model.info(
            "One shot Question:", question_n=i, question=p, model=model, component=component
        )
        response = query_context(
            node_title="BSPL Protocol to Natural Language",
            context_content=context_content,
            payload=p,
            model=model,
        )
        logger_with_model.info(
            "One shot Response:", question_n=i, response=response, model=model, component=component
        )
        logger_with_model.info("------------- -------------- ----------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run BSPL to language agent processing with specified model"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name to use for processing (e.g., 'llama3.1', 'smolllm2', etc.)",
    )

    args = parser.parse_args()

    logger.info("Starting processing with model:", model=args.model)
    main(args.model)
