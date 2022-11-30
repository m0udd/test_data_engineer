# this custom docker file just update and install 
# requirement before running Airflow
FROM apache/airflow:2.4.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt
#COPY ./requirements.txt ./
#RUN pip install --no-cache-dir --user ./requirement.txt