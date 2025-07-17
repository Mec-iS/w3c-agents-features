import json
from pathlib import Path

from bspl.parsers.bspl.bspl_parser import BsplParser
from features_bench.__init__ import logger

model = BsplParser()


def generate_ast():
    target_dir = Path(__file__).resolve().parent.parent.parent

    with open(target_dir / "data" / "training_pairs.json", "r") as f:
        data_pairs = json.load(f)

    for pair in data_pairs:
        payload = pair["bspl"].replace("\n", "").replace("\n", " ")
        try:
            ast = model.parse(payload, rule_name="document")
            logger.info(
                "payload to AST", component=f"{'/'.join(Path(__file__).parts[-2:])}", ast=f"{ast}"
            )
        except:
            logger.error("Error", not_parsed=payload)
            raise


if __name__ == "__main__":
    generate_ast()
