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
	# TypeError: Retry.__init__() got an unexpected keyword argument 'method_whitelist'
	# solved: pip install 'urllib3<2'
	python setup.py sdist
	twine upload dist/*
	# python2.7 setup.py bdist_egg upload
	# python3.5 setup.py bdist_egg upload

test:
	python tests/main.py || true

clean:
	rm -rf beeprint.egg-info/ build/ dist/
