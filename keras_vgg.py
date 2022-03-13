from keras.preprocessing import image
import requests
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
model = VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)

model.summary()




#画像をダンロードするための関数
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    #画像のダウンロード
#    url = 'https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg'
#    file_name = 'hamburger.jpg'
    file_name = 'キャプチャ.JPG'
#    download_img(url, file_name)
    img = image.load_img(file_name, target_size=(224, 224))
    
    # 読み込んだPIL形式の画像をarrayに変換
    ary = image.img_to_array(img)

    #サンプル数の次元を1つ増やし四次元テンソルに
    ary = np.expand_dims(ary, axis=0)

    #上位5を出力
    preds = model.predict(preprocess_input(ary))
    results = decode_predictions(preds, top=5)[0]
    for result in results:
        print(result)