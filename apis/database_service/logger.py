import datetime
import logging


def logger(message):
    now = datetime.datetime.now()
    date = now.strftime("%d%b%Y").lower()
    print(f"============== Request Logs of time {date} =======================")
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.warning(message)
    return logging
