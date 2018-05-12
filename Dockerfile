FROM petkr/gdal-python-alpine:python3.6-gdal2.2.4-v1

LABEL org.label-schema.name = "keboola-geospatial-to-csv"
LABEL org.label-schema.description = "A Keboola Connection processor component that can produce CSV tables from various geospatial formats."
LABEL org.label-schema.vcs-url = "https://github.com/petr-k/keboola-geospatial-to-csv"
LABEL org.label-schema.vendor = "Petr Krebs"

RUN apk add git --no-cache

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /code

COPY requirements*.txt ./
RUN pip install \
    --no-cache-dir \
    -r ${REQUIREMENTS_FILE}

COPY . .

CMD python3 -u ./src/main.py
