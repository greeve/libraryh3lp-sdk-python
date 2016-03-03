.PHONY: dist publish

dist:
	python setup.py sdist
	python setup.py bdist_wheel

publish:
	twine upload dist/*
