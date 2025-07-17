import json
import tempfile
from pathlib import Path

from bspl.generators.asl import generate_asl
from features_bench.__init__ import logger


def test_ASL():
    """
    AgentSpeak Language - a logical programming language used for implementing intelligent
    agents in multi-agent systems. AgentSpeak is based on the Belief-Desire-Intention (BDI) model
    and uses a logic programming syntax similar to Prolog
    """
    target_dir = Path(__file__).resolve().parent.parent.parent

    with open(target_dir / "data" / "training_pairs.json", "r") as f:
        data_pairs = json.load(f)

    for pair in data_pairs:
        payload = pair["bspl"].replace("\n", " ")
        try:
            with tempfile.NamedTemporaryFile(mode="w+", suffix=".bspl", delete=True) as tmpfile:
                tmpfile.write(payload)
                tmpfile.flush()  # Ensure data is written to disk

                asl = generate_asl(tmpfile.name)
                logger.info(
                    "ASL ->",
                    extra={"component": f"{'/'.join(Path(__file__).parts[-2:])}", "asl": asl},
                )
        except Exception as e:
            logger.error("Error", extra={"not_generated": payload, "exception": str(e)})
            raise


if __name__ == "__main__":
    test_ASL()
