REGISTRY ?=
IMAGE_NAME ?= e2e_rag_app
TAG ?= latest

ifdef REGISTRY
IMAGE_REPOSITORY = ${REGISTRY}/${IMAGE_NAME}:${TAG}
else
IMAGE_REPOSITORY = ${IMAGE_NAME}:${TAG}
endif


docker-build:
	@docker build \
		--platform=linux/x86_64 \
		-t ${IMAGE_REPOSITORY} \
		-f Dockerfile .


docker-push:
	@docker push ${IMAGE_REPOSITORY}