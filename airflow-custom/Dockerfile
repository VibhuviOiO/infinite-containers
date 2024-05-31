FROM apache/airflow:2.8.1

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         gcc \
         heimdal-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt
