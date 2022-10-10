#!/bin/bash

# docker
.api-container-name := gistapi

.docker-compose-path := environment
.docker-compose-filename := dockercompose.yml
.docker-image-lookup := docker image ls | grep
.docker-rm-image := docker image rm -f $(.docker-compose-path)-$(.api-container-name)
.docker-rm-container := docker container rm -f $(.docker-compose-path)-$(.api-container-name)

# linters & tests
.run-black := python -m black -l 79 gistapi
.run-flake8 := python -m flake8 --extend-ignore F401,F403 gistapi
.run-tests := python -m pytest -vv .

# application cli
.run-dev := docker-compose -f $(.docker-compose-path)/$(.docker-compose-filename) up --build


lint:
	@$(.run-black)
	@$(.run-flake8)

test:
	@$(.run-tests)

clean-images:
	if $(.docker-image-lookup) $(.api-container-name);\
		then $(.docker-rm-image) && $(.docker-rm-container);\
	fi

run: clean-images lint test
	$(.run-dev)

