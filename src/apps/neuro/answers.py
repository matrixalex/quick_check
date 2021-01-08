import cv2
import numpy as np
import torch

from src.apps.neuro.model_training import get_model
from src.apps.neuro.segmentation import analyse_image, normalize
from matplotlib import pyplot as plt

decoder = {
    0: "a",
    1: "б",
    2: "в",
    3: "г",
    4: "д",
    5: "е",
    6: "ж",
    7: "з"
}

model = get_model()


def make_answer(num_of_questions, filename):
    image = cv2.imread(filename)
    image = cv2.resize(image, (1200, 1600))
    blocks = analyse_image(10, filename)
    print('have blocks')
    i = 0
    answer = []
    for seg in blocks:
        # try:
            print('seg {}'.format(seg[5]))
            img = image[seg[2]:seg[4], seg[1]:seg[3]:-1 if seg[1] > seg[3] else 1, :]
            img = normalize(img)
            img = cv2.resize(img, (28,28))
            img = np.rollaxis(img, axis=2, start=0)
            img = torch.tensor([img]).float()
            draw1 = cv2.rectangle(image, (seg[1], seg[2]), (seg[3], seg[4]), (255, 0, 0), 3)
            answer.append(model(img).tolist()[0])
        # except:
        #     print('failed to parse segment {}'.format([seg[1:]]))
    res = torch.tensor(answer)
    counter = len(answer)
    answer = {}
    while counter > 0:
        torch.sum(torch.max(res))
        most_relevant = torch.argmax(torch.sum(torch.tensor(torch.max(res)==res).int(), dim=1))
        seg = blocks[most_relevant]
        draw2 = cv2.rectangle(image, (seg[1],seg[2]), (seg[3],seg[4]), (255,0,0), 3)
        answer[int(most_relevant) + 1] = decoder[int(torch.argmax(res[most_relevant, :]))]
        res = torch.cat((res[:most_relevant,:], res[min(most_relevant+1,res.shape[0]):,:]), dim=0)
        counter -= 1

    plt.imshow(draw2)
    plt.savefig(filename)
    return dict(sorted(answer.items(), key=lambda item: item[0]))
