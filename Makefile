build:
	python3 setup.py install

test:
	  python3 -m pytest .

isort:
	  isort .

flake8:
	  python3 -m flake8 .

clean-build:
	  rm -rf *.egg-info dist build

clean-pyc:
	  find . -name '*.pyc' -delete
	  find . -name '*.pyo' -delete

trim:
	  trim .

unify:
	   unify -r -i --quote '"' .

trail-comma:
	  find . -name '*.py' -exec add-trailing-comma {} +
