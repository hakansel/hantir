## Client Implemented APIs

1. [Domain Search](https://hunter.io/api-documentation/v2#domain-search)
2. [Email Verifier](https://hunter.io/api-documentation/v2#email-verifier)

## Structure

```
.
├── README.md
├── requirements.txt
├── setup.cfg
├── src
│ ├── __init__.py
│ └── facade
│     ├── __init__.py
│     ├── hunter_io_helper.py
│     ├── hunterio_facade_models.py
│     └── hunterio_facade.py
└── tests
    ├── __init__.py
    └── e2e
        ├── __init__.py
        └── test_hunter_io_e2e.py
```

`hunterio_facade.py` contains clients
</br>
`test_hunter_io_e2e.py` contains tests these clients

## Setup Environement

PS. ensure python linked to the python version 3.11

```
cd <PATH-TO>/hantir
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## RUN Tests

PS. do first Setup Environement

```
cd <PATH-TO>/hantir
PYTHONPATH=./ python tests/e2e/test_hunter_io_e2e.py
```
