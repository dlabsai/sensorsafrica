SHELL := /bin/bash

IMAGE_NAME=sensorsafrica-backend
REGION=eu-central-1
ACCOUNT_ID=177616166430
REPOSITORY=sensorsafrica/backend

build-image:
	docker build --platform linux/amd64 -t "${IMAGE_NAME}" .

aws-auth:
	aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com" 

tag-image: 
	docker tag "${IMAGE_NAME}" ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:latest

push-image:
	docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:latest
