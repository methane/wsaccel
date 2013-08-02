all:
	@echo "Targets:"
	@echo ""
	@echo "   install          Local install"
	@echo "   clean            Cleanup"
	@echo "   build            Clean build"
	@echo "   publish          Clean build and publish to PyPi"
	@echo ""

install:
	python setup.py install

clean:
	rm -rf ./wsaccel.egg-info
	rm -rf ./build
	rm -rf ./dist
	find . -name "*.pyc" -exec rm -f {} \;

build:
	python setup.py sdist
	python setup.py bdist_egg
	python setup.py bdist_wininst

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_egg upload
	python setup.py bdist_wininst upload
