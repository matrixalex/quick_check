from src.apps.celery.celery import app
from src.apps.homework.models import SegmentationData


def get_pupils_set(segments):
    pupils = [segment.pupil_homework.pupil for segment in segments]
    return pupils


@app.task
def update_neuro_data():
    print('update_neuro_data start')
    segments_data = SegmentationData.objects.select_related(
        'pupil_homework', 'pupil_homework__pupil'
    )
    # TODO Обучение дефолтной модели
    pupils = get_pupils_set(segments_data)
    for pupil in pupils:
        pupil_segments_data = segments_data.filter(pupil_homework__pupil=pupil)
        # TODO Обучение модели ученика
    print('update_neuro_data end')
