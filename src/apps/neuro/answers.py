import cv2
import numpy as np
import torch

from src.apps.neuro.model_training import get_model
from src.apps.neuro.segmentation import analyse_image, normalize
from matplotlib import pyplot as plt

decoder = {
    0: " ", 1: "1", 2: "2", 3: "3", 4: "4",
    5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "а", 11: "б", 12: "в", 13: "г",
    14: "д", 15: "е", 16: "ж", 17: "з",
    18: "и", 19: "к", 20: "л", 21: "м",
    22: "н", 23: "о", 24: "п", 25: "р",
    26: "с", 27: "т", 28: "у", 29: "ф",
    30: "х", 31: "ц", 32: "ч", 33: "ш",
    34: "щ", 35: "ь", 36: "ы", 37: "ъ",
    38: "э", 39: "ю", 40: "я"
 }

model = get_model()


def make_answer(num_of_questions, filename):
    answer = []
    image = plt.imread(filename)
    image = cv2.resize(image, (1200, 1600))
    draw1 = image.copy()
    words = analyse_image(num_of_questions,filename)
    for word in words:
        draw1 = cv2.rectangle(draw1, (word[1],word[2]),(word[3],word[4]),(255,0,0),3)
        word = cv2.resize(image[word[2]:word[4],word[1]:word[3],:], (28,28))
        word = np.rollaxis(word, axis=2, start=0)
        word = torch.Tensor([normalize(word)])
        word = torch.argmax(model(word))
        answer.append(decoder[int(word)])
    plt.imshow(draw1)
    plt.savefig(filename, bbox_inches='tight')
    return answer
