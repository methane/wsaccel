all:
	@echo "Targets:"
	@echo ""
	@echo "   install          Local install"
	@echo "   clean            Cleanup"
	@echo "   build            Clean build"
	@echo "   publish          Clean build and publish to PyPi"
	@echo ""

install:
	python3 setup.py install

clean:
	rm -rf ./wsaccel.egg-info
	rm -rf ./build
	rm -rf ./dist
	find . -name "*.pyc" -exec rm -f {} \;

build:
	python3 -m pip install Cython==0.29.32
	python3 setup.py sdist

publish:
	python3 setup.py register
	python3 setup.py sdist upload
