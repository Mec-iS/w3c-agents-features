import json
from pathlib import Path

from bspl.parsers import bspl
from features_bench.__init__ import logger


def test_load_bspl_strings():
    target_dir = Path(__file__).resolve().parent.parent.parent

    with open(target_dir / "data" / "training_pairs.json", "r") as f:
        data_pairs = json.load(f)

    for pair in data_pairs:
        payload = pair["bspl"].replace("\n", "").replace("\n", " ")
        try:
            loaded = bspl.load(payload)
            logger.info(
                "payload loaded", component=f"{'/'.join(Path(__file__).parts[-2:])}", loaded=loaded
            )
        except:
            logger.error("Error", not_parsed=payload)
            raise


if __name__ == "__main__":
    test_load_bspl_strings()
