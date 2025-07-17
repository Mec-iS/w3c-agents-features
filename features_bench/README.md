# Data Bench

Translating BSPL protocols to and from Natural Language.

Anything needed for payloads pre-processing and feature engineerings.

## Install local
```
$ cd features_bench
$ pip install -e .[dev]
```


### Install BSPL Python
```
$ git clone https://gitlab.com/masr/bspl.git
$ pip install -e ./bspl
```

## Run tests
```
$ python -m features_bench.core.base.test_01_parse
$ python -m features_bench.core.base.test_02_ast
```

## Run translations for samples
Training data and samples are available in the `data/` directory.

To run tests against this data, for example:
```
$ python -m features_bench.core.bspl_to_nl.translate_one_shot --model smollm2
```