NAME := muman/bookshelf
ARCH=$$(uname -m)
TAG := ${ARCH}-$$(git log -1 --pretty=%h)
IMG := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build:
	echo "Building docker images for ${ARCH}"
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}

login:
	@docker login ${DOCKER_USER} -p {DOCKER_PASS}


