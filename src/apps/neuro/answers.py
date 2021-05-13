import cv2
import numpy as np
import torch

from src.apps.neuro.model_training import get_model
from src.apps.neuro.segmentation import analyse_image, normalize
from matplotlib import pyplot as plt

from src.quick_check.settings import DEFAULT_TRAIN_DATA_PATH


class NeuroResult:
    def __init__(self):
        self.answers = {}
        self.data = []


decoder = {
    0: " ",
    1: "а", 2: "б", 3: "в", 4: "г",
    5: "д", 6: "е", 7: "ж", 8: "з",
    9: "и", 10: "к", 11: "л", 12: "м",
    13: "н", 14: "о", 15: "п", 16: "р",
    17: "с", 18: "т", 19: "у", 20: "ф",
    21: "х", 22: "ц", 23: "ч", 24: "ш",
    25: "щ", 26: "ь", 27: "ы", 28: "ъ",
    29: "э", 30: "ю", 31: "я", 32: "1",
    33: "2", 34: "3", 35: "4", 36: "5",
    37: "6", 38: "7", 39: "8", 40: "9", 41: "0"
}

decoder_reverse = {
    ' ': 0,
    'а': 1, 'б': 2, 'в': 3, 'г': 4,
    'д': 5, 'е': 6, 'ж': 7, 'з': 8,
    'и': 9, 'к': 10, 'л': 11, 'м': 12,
    'н': 13, 'о': 14, 'п': 15, 'р': 16,
    'с': 17, 'т': 18, 'у': 19, 'ф': 20,
    'х': 21, 'ц': 22, 'ч': 23, 'ш': 24,
    'щ': 25, 'ь': 26, 'ы': 27, 'ъ': 28,
    'э': 29, 'ю': 30, 'я': 31, '1': 32,
    '2': 33, '3': 34, '4': 35, '5': 36,
    '6': 37, '7': 38, '8': 39, '9': 40, '0': 41
}

model = get_model()


def make_answer(num_of_questions, filename, dictpath=DEFAULT_TRAIN_DATA_PATH):
    answer = NeuroResult()
    model = get_model(dictpath)
    image = plt.imread(filename)
    image = cv2.resize(image, (1200, 1600))
    draw1 = image.copy()
    lines = analyse_image(num_of_questions,filename, model, dictpath)
    line_num = -1
    for line in lines:
        answer.answers[line_num] = []
        for word in line:
            draw1 = cv2.rectangle(draw1, (word[1],word[2]),(word[3],word[4]),(255,0,0),3)
            x, y, x_end, y_end = word[1], word[2], word[3], word[4]
            word = cv2.resize(image[word[2]:word[4],word[1]:word[3],:], (100, 100))
            word = np.rollaxis(word, axis=2, start=0)
            word = torch.Tensor([normalize(word)])
            word = int(torch.argmax(model(word)))
            if word > 0:
                char = decoder[int(word)]
                answer.answers[line_num].append(char)
                answer.data.append((x, y, x_end, y_end, char))
        line_num += 1
    plt.imshow(draw1)
    plt.savefig(filename, bbox_inches='tight')
    return answer
