# features

## mission
An operational framework for controlled generation to keep developing the standard, writing validation tests, testing hypothesis.

The main idea is to provide a set of adaptors for all the calls that are bound outside the boundary of a system
 towards the system that has to be make interoperable.

## this repo
Create a workbench for features engineering to model inputs and outputs from publicly available LLMs.

## Running the examples

This repo uses openly available models running locally using `ollama`. Same workflows can apply to any provider in a relatively straighforward way thanks to the `langchain` API.

### install ollama

```
$ curl -fsSL https://ollama.com/install.sh | sh
```
Check `localhost:11434` in your browser.

### models selection

```
$ ollama pull <MODEL>
$ ollama serve
$ ollama run <MODEL>
```
Models available: [link](https://ollama.com/library).

## install package

```
$ conda create -n features python=3.12
$ conda activate features
$ cd features_bench && pip install -e .[dev]
$ git clone https://gitlab.com/masr/bspl.git
$ pip install -e ./bspl
```

## run visualisation
It is possible to run a visualisation of the results using `streamlit`:
```
$ streamlit run features_bench/app/__init__.py
```

## Objectives

To demonstrate a process for the definition of (standard-assuring) Web agents programmed for different tasks required
to achieve the mission statement of the group. Main points tackled:
1. Layout for directories and files involved in context architecture
2. Content, format and language for the files defining the context for the "specialised agents" (agents tasked with carrying on the operations needed for the interoperability to be possbile, "interop agents" or any appropriate naming to be defined)
3. Code (for now LangChain) and workflows (for now LangGraph and LlamaIndex) for the "specialised agents". Miminal Viable Implementation to nudge best practices and provide a test bed for "specialised agents"
4. Evaluation and Testing

## Working hypothesis

### **General** assumptions:
* use interaction-oriented programming (BSPL)
* define input payloads that allow repeatable experiments
* READMEs are for human operators (so to not mingle documentation with inputs)
