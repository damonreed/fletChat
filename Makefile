#
# devcontainer-python Makefile: set up a basic Python environment
#

install: requirements.txt
	apt update
	apt install -y iputils-ping
	pip install --upgrade pip
	pip install --no-cache-dir --upgrade -r ./requirements.txt
