from src.apps.celery.celery import app


@app.task
def update_neuro_data():
    print('update_neuro_data start')

    print('update_neuro_data end')
