import cv2
import torch
import uuid
from src.apps.celery.celery import app
from src.apps.core.models import Document
from src.apps.homework.models import SegmentationData, PupilHomework
from src.apps.neuro.model_training import mach1, normalize
from src.quick_check.settings import DEFAULT_TRAIN_DATA_PATH, MEDIA_ROOT
import numpy as np


def get_pupils_set(segments):
    pupils = [segment.pupil_homework.pupil for segment in segments.distinct(
        'pupil_homework__pupil'
    )]
    return pupils


def train_neuro(data, num_of_epochs=200, batch_size=28, pupil=None):
    model = mach1()
    if pupil and pupil.neuro_data:
        model.load_state_dict(torch.load(str(pupil.neuro_data.file)))
    else:
        model.load_state_dict(torch.load(DEFAULT_TRAIN_DATA_PATH))
    model.eval()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    loss_func = torch.nn.NLLLoss()
    epoch = 0
    while epoch < num_of_epochs:
        data = data.order_by('?')
        for k in range(0, data.count() // batch_size):
            x = []
            y = []
            batch_data = data[k*batch_size:(k+1)*batch_size]
            for segment in batch_data:
                img = cv2.imread(str(segment.pupil_homework.pupilhomework_document.file))
                img = img[segment.x_start:segment.x_end, segment.y_start:segment.y_end, :]
                img = cv2.resize(img, (100, 100))
                img = np.rollaxis(img, 2, 0)
                img = normalize(img)
                x.append(img)
                y.append(segment.answer)
            x = torch.autograd.Variable(torch.Tensor(x))
            y = torch.autograd.Variable(torch.Tensor(y))
            output = model(x)
            out = loss_func(output, y)
            optimizer.zero_grad()
            out.backward()
            optimizer.step()
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
        torch.save(model.state_dict(), DEFAULT_TRAIN_DATA_PATH)


@app.task
def update_neuro_data():
    print('update_neuro_data start')
    segments_data = SegmentationData.objects.select_related(
        'pupil_homework', 'pupil_homework__pupil'
    ).filter(pupil_homework__status=PupilHomework.UPLOADED_HAS_ANSWER)

    train_neuro(segments_data)
    pupils = get_pupils_set(segments_data)
    for pupil in pupils:
        pupil_segments_data = segments_data.filter(pupil_homework__pupil=pupil)
        train_neuro(pupil_segments_data, pupil=pupil)
    print('update_neuro_data end')
