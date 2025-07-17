from functools import lru_cache
from string import Template
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from features_bench.core.base._01_parse import load_parse

from features_bench.__init__ import logger


@lru_cache()
def load_examples():
    examples = """\n\nHere some examples of translations with input a BSPL payload 
    and expected output a Natural Language definition of the input. Please use these as reference
    expected output:"""
    for proto, nl in load_parse():
        examples += "\nINPUT: " + proto
        examples += "\nOUTPUT: " + nl
    return examples


@lru_cache()
def create_prompt_template(node_title: str, context_content: str) -> str:
    """ Safely handles content with curly braces by using $ placeholders.
    """
    logger.info("Building template once")
    # Use Template class for safer string substitution
    template_builder = Template(open(Path(__file__).parent / "_prompt.txt", mode="r").read())

    # Substitute the known values, leaving question as a LangChain placeholder
    partial_template = template_builder.substitute(
        node_name=node_title,
        context_content=context_content,
        examples="{examples}",
        payload="{payload}",  # This becomes the LangChain placeholder
    )

    return PromptTemplate.from_template(partial_template)


def query_context(
    node_title: str, context_content: str, payload: str, model="smollm2"
) -> str:
    """ Build the query context for the given payload and invoke the LLM API. """
    logger.info("Building prompt")

    examples = load_examples()
    prompt_template = create_prompt_template(node_title, context_content)
    prompt = (
        prompt_template.format(payload=payload, examples=examples)
        .replace("\n\n", " ")
        .replace("\n", " ")
    )

    try:
        response = OllamaLLM(model=model).invoke(prompt)
        return response
    except Exception as e:
        return f"Error querying LLM: {e}"
