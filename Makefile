.PHONY: dist publish

dist:
	python setup.py sdist
	python setup.py bdist_wheel

publish:
	python setup.py sdist bdist_wheel upload -r https://testpypi.python.org/pypi
