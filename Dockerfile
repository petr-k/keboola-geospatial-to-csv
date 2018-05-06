FROM python:3.6-alpine

RUN apk update && \
    apk add git && \
    apk add build-base musl-dev --virtual build-dependencies && \
    apk add gdal-dev --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted && \
    pip install gdal &&\
    apk del build-dependencies && \
    rm -rf /var/cache/apk/*

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /code

COPY requirements*.txt ./
RUN pip install \
    --no-cache-dir \
    -r ${REQUIREMENTS_FILE}

COPY . .

CMD python3 -u ./src/main.py

