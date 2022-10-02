import time
import shutil
import os
import csv

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
TARGET_DIR = '/home/me/projects/data/'

total, used, free = shutil.disk_usage("/")


from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


def check_size_file(file_length):
    total, used, free = shutil.disk_usage("/")
    if file_length < free:
        return True


@celery.task()
def reformat_file(file, dir):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dictionary = {}


    # making a list from the keys of the dict
        for row in reader:
            song_and_date_key = row[0] + '+' + row[1]
            try:
                value = int(dictionary[song_and_date_key])
                value += int(row[2])
                dictionary[song_and_date_key] = value
            except KeyError:
                dictionary[song_and_date_key] = row[2]

        rows = []
        for elem in dictionary:
            lhs, rhs = elem.split("+", 1)
            a_dict = [lhs, rhs, dictionary[elem]]
            rows.append(a_dict)

        string_file = str(file)
        arr = string_file.rsplit('/', 1)
        right_elem = 'new_'+ arr[1]
        new_name = arr[0]+ '/' +right_elem
        with open(new_name, 'w') as csvfile:
            writer = csv.writer(csvfile)

            # write a row to the csv file
            for row in rows:
                writer.writerow(row)
            if not check_size_file:
                raise 412
        return right_elem
