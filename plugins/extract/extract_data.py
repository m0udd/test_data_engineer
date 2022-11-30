"""
This script should be scheduled to read/collect 
the data from all sources/services/systems and 
store everything into the 'raw' folder
"""

import os
import shutil

from dotenv import load_dotenv
load_dotenv()


def extract_from_test(test_path=os.getenv('TEST_PATH'), raw_path=os.getenv('RAW_PATH')):
    """
    Copy all files from source_path into destination_path
    return True if succed
    """

    # fetch all files
    for file_name in os.listdir(test_path):
        # construct full file path
        source = os.path.join(test_path, file_name)
        destination = os.path.join(raw_path, file_name)
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)
    return True
