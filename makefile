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
	python setup.py sdist upload
	# python2.7 setup.py bdist_egg upload
	# python3.5 setup.py bdist_egg upload

test27:
	python2.7 -m unittest discover tests || true

test35:
	python3.5 -m unittest discover tests || true

vtest:
	python3.5 tests/test_default_beeprint.py || true
	python2.7 tests/test_default_beeprint.py || true

clean:
	rm -rf beeprint.egg-info/ build/ dist/
