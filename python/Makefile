NAME := muman/bookshelf
TAG := $$(git log -1 --pretty=%h)
IMG := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build:
	echo "Hello"
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}

login:
	@docker login ${DOCKER_USER} -p {DOCKER_PASS}


