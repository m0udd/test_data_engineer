#!/usr/bin/python
# -*- coding: utf-8 -*-

"""`run_fill_data_pipeline.py` is an ELT Dataflow pipeline.
This script should be executed as an entry point.
"""

import logging
import os
from tools.tools import clean_folder
from extract.extract_data import extract_from_test
from load.load_data import load_drug, load_clinical_trials, load_pubmed
from transform.transform_data import transform_published_dugs

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == "__main__":

    # clean everything from previous run
    if os.getenv('ENV', 'DEV') == 'DEV':
        logger.info(
            " ---> STEP 0 : Clean the Data pipeline from previous run (should not be in prod!)")
        clean_folder(os.getenv('RAW_PATH'))
        clean_folder(os.getenv('MINING_PATH'))
        clean_folder(os.getenv('GOLD_PATH'))

    logger.info(" ---> STEP 1 : Extraction in progress...")
    if extract_from_test():
        logger.info(" > STEP 1 : OK")

    logger.info(" ---> STEP 2 : Loading in progress...")
    if load_drug()\
            and load_clinical_trials()\
            and load_pubmed():
        logger.info(" > STEP 2 : OK")

    logger.info(" ---> STEP 3 : Transformation in progress...")
    if transform_published_dugs():
        logger.info(" > STEP 3 : OK")

    # @TODO add some unit test

# exit
