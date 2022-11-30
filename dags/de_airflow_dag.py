"""
This will be the Airflow DAG to manage our data pipeline.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract.extract_data import extract_from_test
from load.load_data import load_drug, load_clinical_trials, load_pubmed
from transform.transform_data import transform_published_dugs

TEST_PATH = '/opt/airflow/plugins/data/test'
RAW_PATH = '/opt/airflow/plugins/data/raw'
MINING_PATH = '/opt/airflow/plugins/data/mining'
GOLD_PATH = '/opt/airflow/plugins/data/gold'

with DAG(
    dag_id="test_de_dag",
    start_date=datetime(2022, 11, 25),
    schedule='@daily',
    template_searchpath='./include',
    catchup=False
) as dag:

    # extracting data

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=extract_from_test,
        op_kwargs={'test_path': TEST_PATH, 'raw_path': RAW_PATH},
        dag=dag
    )

    # loading data

    load_drug = PythonOperator(
        task_id="load_drug",
        python_callable=load_drug,
        op_kwargs={'raw_path': RAW_PATH, 'mining_path': MINING_PATH},
        dag=dag
    )

    load_clinical_trials = PythonOperator(
        task_id="load_clinical_trials",
        python_callable=load_clinical_trials,
        op_kwargs={'raw_path': RAW_PATH, 'mining_path': MINING_PATH},
        dag=dag
    )

    load_pubmed = PythonOperator(
        task_id="load_pubmed",
        python_callable=load_pubmed,
        op_kwargs={'raw_path': RAW_PATH, 'mining_path': MINING_PATH},
        dag=dag
    )

    # transforming data

    transform_published_dugs = PythonOperator(
        task_id="transform_published_dugs",
        python_callable=transform_published_dugs,                
        op_kwargs={'mining_path': MINING_PATH, 'gold_path': GOLD_PATH},
        dag=dag
    )

# task hierarchy
extract_data >> [load_drug, load_clinical_trials,
                 load_pubmed] >> transform_published_dugs
