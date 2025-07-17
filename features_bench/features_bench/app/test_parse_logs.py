from features_bench.app.__init__ import parse_log_file


def test_parse_log_file():
    test_log = """
2025-07-17 10:52:34.944240 [info     ] One shot Question:        component=bspl_to_nl/translate_one_shot.py model=smollm2 question='Offer { roles Buyer, Seller parameters in ID key , out item , out price Buyer → Seller: rfq [ in ID , out item ] Seller → Buyer : quote [ in ID , in item , out price ]}' question_n=1
2025-07-17 10:53:17.377744 [info     ] One shot Response:        component=bspl_to_nl/translate_one_shot.py model=smollm2 question_n=1 response='Here is a natural language translation of the given BSPL Payload: The task requires translating a protocol from a simple BSPL language to a more human-readable format.'"""

    df = parse_log_file(test_log)
    breakpoint()

    assert len(df) == 1  # only the question is spotted
    assert not df.empty, "Parsed dataframe is empty"
    assert "question_n" in df.columns, "Missing 'question_n' column"
    assert "model" in df.columns, "Missing 'model' column"
    assert "question" in df.columns, "Missing 'question' column"
    assert "response" in df.columns, "Missing 'response' column"
    assert df["question_n"].iloc[0] == 1, "Unexpected question number"
    assert df["model"].iloc[0] == "smollm2", "Unexpected model"
    assert df["question"].iloc[0].startswith("Offer { roles Buyer"), "Unexpected question content"
    assert df["response"].iloc[0].startswith("Here is a natural language"), (
        "Unexpected response content"
    )

    print("Test passed: parse_log_file correctly handles variable whitespace in log format.")
