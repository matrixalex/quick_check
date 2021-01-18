import cv2
import numpy as np
import torch

from src.apps.neuro.model_training import get_model
from src.apps.neuro.segmentation import analyse_image, normalize
from matplotlib import pyplot as plt

from src.quick_check.settings import DEFAULT_TRAIN_DATA_PATH

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

model = get_model()


def make_answer(num_of_questions, filename, dictpath=DEFAULT_TRAIN_DATA_PATH):
    model = get_model(dictpath)
    answer = {}
    image = plt.imread(filename)
    image = cv2.resize(image, (1200, 1600))
    draw1 = image.copy()
    lines = analyse_image(num_of_questions,filename, model, dictpath)
    line_num = -1
    for line in lines:
        answer[line_num] = []
        for word in line:
            draw1 = cv2.rectangle(draw1, (word[1],word[2]),(word[3],word[4]),(255,0,0),3)
            word = cv2.resize(image[word[2]:word[4],word[1]:word[3],:], (100, 100))
            word = np.rollaxis(word, axis=2, start=0)
            word = torch.Tensor([normalize(word)])
            word = int(torch.argmax(model(word)))
            if word > 0:
                answer[line_num].append(decoder[int(word)])
        line_num += 1
    plt.imshow(draw1)
    plt.savefig(filename, bbox_inches='tight')
    return answer
