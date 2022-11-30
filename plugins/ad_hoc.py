#!/usr/bin/python
# -*- coding: utf-8 -*-

"""`ad_hoc.py`
This script will take the gold data and print each journal 
and his corresponding number of different unique drug mention,
order by the highest mention.
"""

import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":

    df = pd.read_json(
        os.path.join(os.getenv('GOLD_PATH'), 'published_drugs.json')
    )

    # get drugA/releaseA, drugA/releaseB...
    df = df.explode('release')

    # get drugA/journalA, drugA/journalB... but unique!
    df = df.join(pd.DataFrame([*df.pop('release')],
                 index=df.index)).reset_index(drop=True)
    df.drop(columns='quote', inplace=True)
    df = df.drop_duplicates(['drug', 'journal'])

    # group by journal and count occurrence
    df = df.groupby(['journal'], axis=0, as_index=False).size()
    df = df.rename({'size': 'nb_drugs_mention'}, axis=1)

    # sort and print
    df = df.sort_values('nb_drugs_mention', ascending=False)

    for i, row in df.iterrows():
        print(
            f"-> ('{row['journal']}') has mentioned {row['nb_drugs_mention']} different drugs.")
