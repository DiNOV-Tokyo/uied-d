# https://qiita.com/daichimizuno/items/d1a255fa56960302bcc5
from PIL import Image
import numpy as np
import glob
import os
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Flatten, Dense, Input, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.applications.resnet import ResNet152
from keras import optimizers
from tensorflow.keras.optimizers import SGD

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

input_tensor = Input(shape=(image_size, image_size, 3))
#ResNet50 = ResNet50(include_top=False, weights='imagenet',input_tensor=input_tensor)
#resnet101 = ResNet101(include_top=False, weights='imagenet',input_tensor=input_tensor)
resnet152 = ResNet152(include_top=False, weights='imagenet',input_tensor=input_tensor)

top_model = Sequential()
top_model.add(Flatten(input_shape=resnet152.output_shape[1:]))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(dense_size, activation='softmax'))

#print("\n\n")
#print(ResNet50)
#print("\n\n")
# ResNet50とFC層を結合してモデルを作成
top_model = Model(inputs=resnet152.input, outputs=top_model(resnet152.output))
#resnet50_model = Model(inputs=resnet50.input, outputs=top_model(resnet50.output))



#top_model = Model(input=ResNet50.input, output=top_model(ResNet50.output))
#top_model.compile(loss='categorical_crossentropy',optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),metrics=['accuracy'])
opt= SGD(learning_rate= 0.01, momentum=0.9)
top_model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])


top_model.summary()
result = top_model.fit(X_train, y_train, validation_split=0.15, epochs=epochs, batch_size=batch_size)
#top_model.save("saved_model.pb")
top_model.save("saved_model")

x = range(epochs)
plt.title('Model accuracy')
plt.plot(x, result.history['accuracy'], label='accuracy')
plt.plot(x, result.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0, ncol=2)

name = 'resnet_tobacco_dataset_reslut.jpg'
plt.savefig(name, bbox_inches='tight')
plt.close()
