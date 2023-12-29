#
# devcontainer-python Makefile: set up a basic Python environment
#

REPO=damonreed
IMAGE=devcontainer-python
TAG=latest

requirements: requirements.txt
	pip install --no-cache-dir -r ./requirements.txt
