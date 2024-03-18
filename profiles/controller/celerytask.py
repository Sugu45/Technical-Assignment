import os
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def count_words_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        word_count = len(content.split())
        return {'file': file_path, 'word_count': word_count}
    except Exception as e:
        return {'error': str(e)}
