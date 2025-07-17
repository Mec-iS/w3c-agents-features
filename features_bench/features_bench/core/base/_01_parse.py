import json
from pathlib import Path

from bspl.parsers.bspl import parse
from features_bench.__init__ import logger


def load_parse():
    """
    Load and parse all the text-payload pairs in the training pairs.
    """
    target_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
    data_file = target_dir / "data" / "training_pairs.json"

    logger.info("Loading data from a JSON file", file=data_file)
    with open(data_file, "r") as f:
        data_pairs = json.load(f)

    for pair in data_pairs:
        payload = pair["bspl"].replace("\n\n", " ").replace("\n", "")
        try:
            parsed = parse(payload)
            logger.info(
                "payload parsed",
                component=f"{'/'.join(Path(__file__).parts[-2:])}",
                parsed=f"{parsed}",
            )
            yield payload, pair["natural_language"]
        except:
            logger.error("Error", not_parsed=payload)
            raise


if __name__ == "__main__":
    load_parse()
