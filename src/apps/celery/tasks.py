import random
from datetime import datetime

import cv2
import torch
import uuid
from src.apps.celery.celery import app
from src.apps.core.models import Document
from src.apps.homework.models import SegmentationData, PupilHomework, Criterion
from src.apps.neuro.model_training import mach1, normalize
from src.apps.neuro.answers import decoder_reverse
from src.quick_check.settings import DEFAULT_KEYS_TRAIN_DATA_PATH, DEFAULT_TEXT_TRAIN_DATA_PATH, MEDIA_ROOT
import numpy as np


def get_pupils_set(segments):
    return list(set([segment.pupil_homework.pupil for segment in segments]))


def group_by_pupil_homework(segments):
    result = {}
    for segment in segments:
        if segment.pupil_homework.id not in result:
            result[segment.pupil_homework.id] = [segment]
        else:
            result[segment.pupil_homework.id].append(segment)

    return result


def train_neuro(data, num_of_epochs=50, pupil=None, default_data_path=DEFAULT_TEXT_TRAIN_DATA_PATH):
    model = mach1()
    model.load_state_dict(torch.load(default_data_path))
    model.eval()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    loss_func = torch.nn.NLLLoss()
    epoch = 0
    data_keys = list(data.keys())
    error_files_log = []
    error_files = set()
    while epoch < num_of_epochs:
        # print('epoch {} of {}'.format(epoch, num_of_epochs))
        random.shuffle(data_keys)
        for key in data_keys:
            x = []
            y = []
            batch = data[key]
            image_file_path = str(batch[0].pupil_homework.pupilhomework_document.file)
            img = cv2.imread(image_file_path)
            try:
                for segment in batch:
                    image = img[segment.x_start:segment.x_end, segment.y_start:segment.y_end, :]
                    if image.size > 0 and len(image.shape) > 2:
                        image = cv2.resize(image, (100, 100))
                        image = np.rollaxis(image, 2, 0)
                        image = normalize(image)
                        x.append(image)
                        y.append(decoder_reverse[segment.answer])
                    else:
                        if image_file_path not in error_files:
                            err_msg = 'segmentation error segment {}:{}, {}:{} of file {}, shape: {}'.format(
                                segment.x_start,
                                segment.x_end,
                                segment.y_start,
                                segment.y_end,
                                image_file_path,
                                img.shape
                            )
                            error_files.add(image_file_path)
                            error_files_log.append(err_msg)
                x = torch.autograd.Variable(torch.Tensor(x))
                y = torch.autograd.Variable(torch.LongTensor(y))
                output = model(x)
                out = loss_func(output, y)
                optimizer.zero_grad()
                out.backward()
                optimizer.step()
            except Exception as e:
                print(e)
                print('problem in file {}'.format(image_file_path))
                print('epoch {}'.format(epoch))
        epoch += 1
    if pupil:
        if pupil.neuro_data:
            torch.save(model.state_dict(), str(pupil.neuro_data.file))
        else:
            file_name = str(uuid.uuid4()) + '.d'
            file_path = MEDIA_ROOT + '/' + file_name
            torch.save(model.state_dict(), file_path)
            doc = Document.objects.create(file=file_path, file_name=file_name)
            pupil.neuro_data = doc
            pupil.save()
    else:
        torch.save(model.state_dict(), default_data_path)

    for err in error_files_log:
        print(err)


def process_training(segments_data, pupils_set, default_train_data_path=DEFAULT_TEXT_TRAIN_DATA_PATH):
    print('default training')
    segments_dict = group_by_pupil_homework(segments_data)
    train_neuro(segments_dict, default_data_path=default_train_data_path)
    print('pupils training start')
    for pupil in pupils_set:
        pupil_segments_data = group_by_pupil_homework(segments_data.filter(pupil_homework__pupil=pupil))
        train_neuro(pupil_segments_data, pupil=pupil, default_data_path=default_train_data_path)
        print('pupil {} complete'.format(pupil))


@app.task
def update_neuro_data():
    print('update_neuro_data start')
    time_start = datetime.now()
    segments_data = SegmentationData.objects.select_related(
        'pupil_homework',
        'pupil_homework__pupil',
        'pupil_homework__pupilhomework_document',
        'pupil_homework__homework_exercise__homework_criterion'
    ).filter(pupil_homework__status=PupilHomework.UPLOADED_HAS_ANSWER)
    pupils = get_pupils_set(segments_data)
    key_segments_data = segments_data.filter(
        pupil_homework__homework_exercise__homework_criterion__criterion_type=Criterion.KEY_TYPE
    )
    text_segments_data = segments_data.filter(
        pupil_homework__homework_exercise__homework_criterion__criterion_type=Criterion.TEXT_TYPE
    )
    print('keys training')
    process_training(key_segments_data, pupils, default_train_data_path=DEFAULT_KEYS_TRAIN_DATA_PATH)
    print('text training')
    process_training(text_segments_data, pupils, default_train_data_path=DEFAULT_TEXT_TRAIN_DATA_PATH)
    time_end = datetime.now()
    print('time spent {}'.format(time_end - time_start))
    print('update_neuro_data end')
