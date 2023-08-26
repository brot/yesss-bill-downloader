pip install -U pip setuptools wheel

pip-compile --upgrade --generate-hashes --output-file=requirements/requirements.txt requirements/requirements.in

pip install -r requirements/requirements.txt
