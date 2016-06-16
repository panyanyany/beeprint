sdist:
	python setup.py sdist || true

edist:
	python setup.py bdist_egg || true

dist:
	python setup.py sdist bdist_egg || true

register:
	python setup.py register -r pypi || true
	python setup.py register -r pypitest || true

full:
	python setup.py sdist bdist_egg upload

test27:
	python2.7 -m unittest discover tests || true

test35:
	python3.5 -m unittest discover tests || true
