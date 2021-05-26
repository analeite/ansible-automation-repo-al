FROM python:3.9.5-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo

COPY . .

RUN pip install -r requirements.txt

RUN pip3 install "ansible-lint[community,yamllint]"
