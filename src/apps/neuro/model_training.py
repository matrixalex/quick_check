import torch
import torch.nn as nn
from torch.nn.functional import sigmoid

# df = pd.read_csv('../input/russian-handwritten-letters/all_letters_info.csv')
# df = df[(df["background"] == 0) & (df["label"] < 7)]


class mach1(nn.Module):
    def __init__(self):
        super(mach1, self).__init__()
        self.conv0 = nn.Conv2d(3, 28, 3)
        self.fc0 = nn.ReLU()
        self.conv1 = nn.Conv2d(28, 14, 3)
        self.pool1 = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(14*12*12,136)
        self.fc2 = nn.Linear(136,101)
        self.fc3 = nn.Linear(101,41)
        self.fc4 = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.conv0(x)
        x = self.fc0(x)
        x = self.conv1(x)
        x = self.pool1(x)
        x = x.view(-1,14*12*12)
        x = sigmoid(self.fc1(x))
        x = sigmoid(self.fc2(x))
        x = sigmoid(self.fc3(x))
        x = self.fc4(x)
        return x


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