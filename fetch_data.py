import json
import os
import time
from datetime import datetime

import requests

from log import logging

API_EXEVO_PAN_URL = 'https://www.exevopan.com/api/auctions'
FILE_NAME = 'auction_history'
DATE_FORMAT = '%d_%m_%Y'
OUTPUT_PATH = './output'


def fetch(descending: bool = False, history: bool = False, first_page: int = 0, page_size: int = 10) -> None:
    """
    Fetch date from Exevo Pan API and saves it into a jsonl file.

    :param descending: if true, fetch the latest auctions, otherwise the earliest;
    :param history: if true fetch the auctions from the history, otherwise get from current auctions;
    :param first_page: The initial page to start the fetching of data;
    :param page_size: The number of auctions present in response page.
    :return: None, but creates a jsonl file.
    """
    params = {
        'descending': descending,
        'history': history,
        'currentPage': first_page,
        'pageSize': page_size
    }
    has_next = True
    current_file_name = f"{FILE_NAME}_{datetime.now().strftime(DATE_FORMAT)}.jsonl"
    while has_next:
        try:
            logging.info(f"Getting page {params['currentPage']} data with params {params}...")
            response = requests.get(API_EXEVO_PAN_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                for auction in data['page']:
                    append_to_file(current_file_name, json.dumps(auction))
                has_next = data['hasNext']
                logging.info(f"Page {params['currentPage']} collected successfully.")
                params['currentPage'] += 1
            else:
                logging.info(f"Request gone wrong. Page: {params['currentPage']} Status code: {response.status_code}")
                break
            time.sleep(0.01)
        except Exception as error:
            logging.error(f"Error trying get data. Error: {error}  Page: {params['currentPage']}")
            break


def append_to_file(filename: str, content: str) -> None:
    """
    Appends content to file or creates it if its does not exist.

    :param filename: The file name for the final file;
    :param content:  The content to be appended to the file.
    :return: None
    """
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    with open(os.path.join(OUTPUT_PATH, filename), 'a') as jsonl_file:
        jsonl_file.write(content + "\n")


if __name__ == '__main__':
    fetch(descending=True, history=True, first_page=0, page_size=100)