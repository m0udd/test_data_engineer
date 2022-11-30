"""
Logger for this data pipeline
"""
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

"""
Store environement for this data pipeline
"""
ENV = 'debug'  # should be read from env var

def totooo():
    print('toto')

def clean_folder(folder: str):
    """
    Safely clean a specific folder
    """
    import os
    import shutil
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error('Failed to delete %s. Reason: %s' % (file_path, e))


def try_parsing_date(text_date):
    """
    Try parsing date with different format
    """
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d %B %Y'):
        try:
            return datetime.strptime(text_date, fmt)
        except ValueError:
            pass
    logger.error('no valid date format found for '+text_date)
    return text_date


def match_title_drug(title, drugs_list):
    """
    Find and return all matching drugs in title
    """
    match = []
    for d in drugs_list:
        if d in title:
            match.append(d)
    return set(match)
