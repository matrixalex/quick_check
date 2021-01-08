import cv2
import math
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from scipy.signal import argrelmin
warnings.simplefilter('ignore')
sns.set(rc={'figure.figsize' : (22, 10)})
sns.set_style("darkgrid", {'axes.grid' : True})


def createKernel(kernelSize, sigma, theta):
    "create anisotropic filter kernel according to given parameters"
    assert kernelSize % 2 # must be odd size
    halfSize = kernelSize // 2

    kernel = np.zeros([kernelSize, kernelSize])
    sigmaX = sigma
    sigmaY = sigma * theta

    for i in range(kernelSize):
        for j in range(kernelSize):
            x = i - halfSize
            y = j - halfSize

            expTerm = np.exp(-x**2 / (2 * sigmaX) - y**2 / (2 * sigmaY))
            xTerm = (x**2 - sigmaX**2) / (2 * math.pi * sigmaX**5 * sigmaY)
            yTerm = (y**2 - sigmaY**2) / (2 * math.pi * sigmaY**5 * sigmaX)

            kernel[i, j] = (xTerm + yTerm) * expTerm

    kernel = kernel / np.sum(kernel)
    return kernel

def crop_text_to_lines(text, blanks):
    x1 = 0
    y = 0
    lines = []
    for i, blank in enumerate(blanks):
        x2 = blank
        if x1 < x2:
            line = text[:, x1:x2]
            lines.append((line, x1, x2))
            x1 = blank
    return lines
    

def smooth(x, window_len=40, window='hanning'):
#     if x.ndim != 1:
#         raise ValueError("smooth only accepts 1 dimension arrays.") 
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.") 
    if window_len<3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'") 
    s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')
    return y

def display_lines(lines_arr, orient='vertical'):
    print('display_lines')
    plt.figure(figsize=(30, 30))
    if not orient in ['vertical', 'horizontal']:
        raise ValueError("Orientation is on of 'vertical', 'horizontal', defaul = 'vertical'") 
    if orient == 'vertical': 
        for i, l in enumerate(lines_arr):
            line = l[0]
            plt.subplot(5, 10, i+1)  # A grid of 2 rows x 10 columns
            plt.axis('off')
            plt.title("Line #{0}".format(i))
            _ = plt.imshow(line, cmap='gray', interpolation='bicubic')
            plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    else:
            for i, l in enumerate(lines_arr):
                line = l[0]
                plt.subplot(90, 1, i+1)  # A grid of 90 rows x 1 columns
                plt.axis('off')
                plt.title("Line #{0}".format(i))
                _ = plt.imshow(line, cmap='gray', interpolation='bicubic')
                plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def applySummFunctin(img):
    res = np.sum(img, axis=0)
    return res


def normalize(img):
    (m, s) = cv2.meanStdDev(img)
    m = m[0][0]
    s = s[0][0]
    img = img - m
    img = img / s if s>0 else img
    return img


def showImg(img, cmap=None):
    plt.imshow(img, cmap=cmap, interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def transpose_lines(lines):
    res = []
    for l in lines:
        line = np.transpose(l[0])
        res.append((line,l[1],l[2]))
    return res


def lineSegmentation(image, show=False, smoothness=50, kernelSize=11, sigma=4, theta=1.5):
    imgFiltered1 = cv2.filter2D(image, -1, createKernel(kernelSize, sigma, theta), borderType=cv2.BORDER_REPLICATE)
    img4 = normalize(imgFiltered1)
    (m, s) = cv2.meanStdDev(imgFiltered1)
    summ = applySummFunctin(img4)
    smoothed = smooth(summ, smoothness)
    mins = argrelmin(smoothed, order=2)
    arr_mins = np.array(mins)
    found_lines = crop_text_to_lines(img4, arr_mins[0])
    # if show:
    #     res_lines = transpose_lines(found_lines)
    #     display_lines(res_lines, 'horizontal')
    return found_lines


def wordSegmentation(image, show=False, smoothness=45, kernelSize=19, sigma=9, theta=7, minArea=0):
    img = np.transpose(image)
    imgFiltered1 = cv2.filter2D(img, -1, createKernel(kernelSize, sigma, theta), borderType=cv2.BORDER_REPLICATE)
    img4 = normalize(imgFiltered1)
    summ = applySummFunctin(img4)
    smoothed = smooth(summ, smoothness)
    mins = argrelmin(smoothed, order=2)
    arr_mins = np.array(mins)
    found_lines = crop_text_to_lines(img4, arr_mins[0])
    res_lines = []
    for i in range(len(found_lines)-1):
        res_lines.append(found_lines[i])
    # if show:
    #     display_lines(res_lines)
    return res_lines


def analyse_image(N_of_questions, filename):
    img = cv2.imread(filename)
    plt.imshow(img)
    img = cv2.resize(img, (1200, 1600))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = np.transpose(img)
    images = []
    i = 1
    for im in lineSegmentation(img):
        j = 0
        to_plot = []
        for word in wordSegmentation(im[0]):
            to_plot.append((word[0], 0, 0))
            images.append((word[0], word[1], im[1], word[2], im[2], i))
            j += 1
            if j == 3:
                # display_lines(to_plot)
                break
        if i == N_of_questions + 1:
            break
        i += 1
    return images
