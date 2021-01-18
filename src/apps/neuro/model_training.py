import numpy as np
import torch

import torch.nn as nn


def normalize(image):
    if len(image.shape)==2:
        m = np.mean(image)
        sd = np.std(image)
        if sd!=0:
            return (image-m)/sd
        else:
            return (image-m)
    elif len(image.shape)==3:
        m = np.mean(image)
        sd = np.std(image)
        if sd!=0:
            return (image-m)/sd
        else:
            return (image-m)
    else:
        return np.nan


class mach1(nn.Module):
    def __init__(self):
        super(mach1, self).__init__()
        self.conv0 = nn.Conv2d(3, 96, 11, stride=4)
        self.pool0 = nn.MaxPool2d(3, stride=2)
        self.conv1 = nn.Conv2d(96, 256, 5, padding=2)
        self.pool1 = nn.MaxPool2d(3, stride=2, padding=1)
        self.conv2 = nn.Conv2d(256, 384, 3, padding=1)
        self.conv3 = nn.Conv2d(384, 384, 3, padding=1)
        self.pool2 = nn.MaxPool2d(3, stride=2)
        self.fc0 = nn.Linear(384 * 2 * 2, 42)
        self.fc1 = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.conv0(x)
        # print(x.shape)
        x = self.pool0(x)
        # print(x.shape)
        x = self.conv1(x)
        # print(x.shape)
        x = self.pool1(x)
        # print(x.shape)
        x = self.conv2(x)
        # print(x.shape)
        x = self.conv3(x)
        # print(x.shape)
        x = self.pool2(x)
        # print(x.shape)
        x = x.view(-1, 384 * 2 * 2)
        x = self.fc0(x)
        return self.fc1(x)


class mach2(nn.Module):
    def __init__(self):
        super(mach2, self).__init__()
        self.conv0 = nn.Conv2d(3, 96, 11, stride=4)
        self.pool0 = nn.MaxPool2d(3, stride=2)
        self.conv1 = nn.Conv2d(96, 256, 5, padding=2)
        self.pool1 = nn.MaxPool2d(3, stride=2, padding=1)
        self.conv2 = nn.Conv2d(256, 384, 3, padding=1)
        self.conv3 = nn.Conv2d(384, 384, 3, padding=1)
        self.pool2 = nn.MaxPool2d(3, stride=2)
        self.fc0 = nn.Linear(384 * 2 * 2, 42*42)
        self.fc1 = nn.LogSoftmax(dim=1)

    def forward(self, x):
        # print(x.shape)
        x = self.conv0(x)
        # print(x.shape)
        x = self.pool0(x)
        # print(x.shape)
        x = self.conv1(x)
        # print(x.shape)
        x = self.pool1(x)
        # print(x.shape)
        x = self.conv2(x)
        # print(x.shape)
        x = self.conv3(x)
        # print(x.shape)
        x = self.pool2(x)
        # print(x.shape)
        x = x.view(-1, 384 * 2 * 2)
        x = self.fc0(x)
        return self.fc1(x)



model1 = mach1()
model2 = mach1()
model3 = mach2()


ml_model = None


def get_model(data_path: str = None):
    global ml_model
    if ml_model:
        return ml_model
    assert data_path
    result = mach1()
    result.load_state_dict(torch.load(data_path))
    result.eval()
    ml_model = result
    return result


"""
def int_to_vector(x):
    answer = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    answer[x]=1
    return answer


X = df[["file"]]
y = df["label"].values

optimizer = torch.optim.Adam(model.parameters(), lr=0.04)

loss_fn = nn.CrossEntropyLoss()

losses = []
batch_size = 50


for e in range(2100):
    for batch in range(X.shape[0]//batch_size):
        X_batch = []
        for filename in X.values[batch*batch_size:min((batch+1)*batch_size, X.shape[0])]:
            img = cv2.imread('../input/russian-handwritten-letters/all_letters_image/all_letters_image/'+filename[0])
            img = cv2.resize(img, (28,28))
            img = normalize(img)
            X_batch.append(np.rollaxis(img, axis=2, start=0))
            
        y_batch = y[batch*batch_size:min((batch+1)*batch_size, X.shape[0])] 
        X_train, X_test, y_train, y_test = train_test_split(X_batch, y_batch)
        
        X_train = Variable(torch.from_numpy(np.array(X_train)).float())
        X_test = Variable(torch.from_numpy(np.array(X_test)).float())
        y_train = Variable(torch.from_numpy(np.array(y_train.tolist())).float())
        y_test = Variable(torch.from_numpy(np.array(y_test.tolist())).float())
        
        out = model(X_train)
        y_train = y_train.long()
        loss = loss_fn(out,y_train)
        losses.append(loss)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if e % 200 == 0:
            preds_test = model(X_test)
            y_test = y_test.long()
            loss_test = loss_fn(preds_test, y_test)
            s1 = torch.tensor([1]*len(y_test)).float()
            s2 = float(torch.abs(y_test-torch.argmax(preds_test, dim=1)) > 0)
            print("acc:", torch.mean(s1-s2))
            print('Epoch:{0}, Error-Loss:{1}'.format(e, loss.item()))
            print('Epoch:{0}, Error-Test-Loss:{1}'.format(e, loss.item()))
            print('------------------------------------------------------')
"""