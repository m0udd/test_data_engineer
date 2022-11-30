
"""
This script should be scheduled to transform the  
the data from mining to gold. The gold zone should 
contain a transformed data that is as close as possible 
to the business usage. Gold data is consumed from 
other app for analytics or dashboarding for example.
"""

import os
import pandas as pd
from tools.tools import match_title_drug

from dotenv import load_dotenv
load_dotenv()


def transform_published_dugs(mining_path=os.getenv('MINING_PATH'), gold_path=os.getenv('GOLD_PATH')):
    df_pmd = pd.read_csv(os.path.join(mining_path, 'pubmed.csv'))
    df_pmd['type'] = 'pubmed'

    df_clt = pd.read_csv(os.path.join(mining_path, 'clinical_trials.csv'))
    df_clt.rename(columns={'scientific_title': 'title'}, inplace=True)
    df_clt['type'] = 'clinical_trials'

    df = pd.concat([df_pmd, df_clt], ignore_index=True)
    df['title_up'] = df['title'].str.upper()

    drugs_list = pd.read_csv(os.path.join(mining_path, 'drugs.csv'))
    drugs_list = drugs_list['drug'].values.tolist()

    # find all occurence of drug in title
    df['drug'] = df['title_up'].map(
        lambda title: match_title_drug(title, drugs_list))
    df = df.explode('drug')
    df = df[df['drug'].notna()]
    df = df.drop('title_up', axis=1)

    # organize the data as drug -> release -> [journal -> [quote]]
    df['pub_tmp'] = df.apply(lambda row: {
                             'date': row['date'], 'type': row['type'],
                             'id': row['id'], 'title': row['title']}, axis=1)
    df.drop(columns=['date', 'title', 'id', 'type'], inplace=True)

    df = df.groupby(['drug', 'journal']).agg(list).reset_index()

    df['release'] = df.apply(
        lambda row: {'journal': row['journal'], 'quote': row['pub_tmp']}, axis=1)
    df.drop(columns=['journal', 'pub_tmp'], inplace=True)

    df = df.groupby(['drug']).agg(list).reset_index()

    df.to_json(os.path.join(gold_path, 'published_drugs.json'),
               orient='records', indent=4, force_ascii=False)
    return True
