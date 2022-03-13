# https://qiita.com/daichimizuno/items/d1a255fa56960302bcc5
from PIL import Image
import numpy as np
import glob
import os
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.convolutional import MaxPooling2D
from keras.layers import  Conv2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

root = "dataset"
folder = os.listdir(root)
image_size = 224
dense_size = len(folder)
epochs = 3
batch_size = 16

X = []
Y = []
for index, name in enumerate(folder):
    dir = "./" + root + "/" + name
    print("dir : ", dir)
    files = glob.glob(dir + "/*")
    print("number : " + str(files.__len__()))
    for i, file in enumerate(files):
      try:
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))
        data = np.asarray(image)
        X.append(data)
        Y.append(index)
      except :
          print("read image error")

X = np.array(X)
Y = np.array(Y)
X = X.astype('float32')
X = X / 255.0

Y = np_utils.to_categorical(Y, dense_size)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(dense_size, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

result = model.fit(X_train, y_train, validation_split=0.15, epochs=epochs, batch_size=batch_size)
#model.save("saved_model.pb")
model.save("saved_model")


x = range(epochs)
plt.title('Model accuracy')
plt.plot(x, result.history['accuracy'], label='accuracy')
plt.plot(x, result.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0, ncol=2)

name = 'tobacco_dataset_reslut.jpg'
plt.savefig(name, bbox_inches='tight')
plt.close()


