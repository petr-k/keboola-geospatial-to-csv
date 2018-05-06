FROM python:3.6-alpine

RUN apk add \
	gdal git \
	--no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /code

COPY requirements*.txt ./
RUN pip install \
    --no-cache-dir \
    -r ${REQUIREMENTS_FILE}

COPY . .

# Run the application
CMD python3 -u ./src/main.py
