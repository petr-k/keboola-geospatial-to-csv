FROM petkr/gdal-python-alpine:python3.6-gdal2.2.4-v1

RUN apk add git --no-cache

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /code

COPY requirements*.txt ./
RUN pip install \
    --no-cache-dir \
    -r ${REQUIREMENTS_FILE}

COPY . .

CMD python3 -u ./src/main.py

