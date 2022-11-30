
"""
This script should be scheduled to load/prepare the  
the data from raw to something meaningful for the
business. The files should contain all the information 
we need in the future. I called it the mining process.
"""
import os
import pandas as pd
import json5
import csv
from tools.tools import try_parsing_date

from dotenv import load_dotenv
load_dotenv()

# @TODO read directory and load/merge files automatically


def load_drug(raw_path=os.getenv('RAW_PATH'), mining_path=os.getenv('MINING_PATH')):
    """
    Load file to mining zone
    """
    #path_load = task.xcom_pull(task_ids='load_drugs_publication', key='load')
    file_name = 'drugs.csv'
    df_drugs_csv = pd.read_csv(
        os.path.join(raw_path, file_name))

    df_drugs_csv.to_csv(
        os.path.join(mining_path, file_name), index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
    return True


def load_pubmed(raw_path=os.getenv('RAW_PATH'), mining_path=os.getenv('MINING_PATH')):
    """
    Load file to mining zone
    """
    df_pubmed_csv = pd.read_csv(
        os.path.join(raw_path, 'pubmed.csv'))

    with open(os.path.join(raw_path, 'pubmed.json')) as f:
        df_pubmed_json = pd.DataFrame(json5.load(f))

    # concat both csv and json and reset index
    df_pubmed_csv = pd.concat(
        [df_pubmed_csv, df_pubmed_json]).reset_index(drop=True)
    df_pubmed_csv['id'] = df_pubmed_csv.index+1

    # make the date great again! ;)
    df_pubmed_csv['date'] = df_pubmed_csv['date'].map(
        lambda dte: try_parsing_date(dte))

    df_pubmed_csv.to_csv(
        os.path.join(mining_path, 'pubmed.csv'), index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
    return True


def load_clinical_trials(raw_path=os.getenv('RAW_PATH'), mining_path=os.getenv('MINING_PATH')):
    """
    Load file to mining zone
    """
    file_name = 'clinical_trials.csv'
    df_clinical_trials_csv = pd.read_csv(
        os.path.join(raw_path, file_name), parse_dates=['date'], date_parser=try_parsing_date)
    
    # clean/remove some special byte-char
    df_clinical_trials_csv['scientific_title'] = df_clinical_trials_csv['scientific_title'].apply(lambda x: x.replace('\\xc3', ''). replace('\\xb1', ''))
    df_clinical_trials_csv['journal'] = df_clinical_trials_csv['journal'].astype(str).apply(lambda x: x.replace('\\xc3', ''). replace('\\x28', ''))

    df_clinical_trials_csv.to_csv(
        os.path.join(mining_path, file_name), index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
    return True
