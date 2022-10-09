
import numpy as np
import cv2
from icrawler.builtin import BingImageCrawler
import keras

# 画像とモデルを渡して顔認証、戻り値:ラベル付きリザルト画像
def detect_face(model,image):
    print("detect_face 起動")
    # 画像をRGB形式へ変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # グレースケール変換
    image_gs = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # 顔認識の実行
    cascade = cv2.CascadeClassifier("./meta/haarcascade_frontalface_default.xml")
    face_list = cascade.detectMultiScale(image_gs)

    # 顔が１つ以上検出できた場合
    if len(face_list) > 0:
        print(f"認識した顔の数:{len(face_list)}")
        for (xpos, ypos, width, height) in face_list:
            # 認識した顔の切り抜き
            face_image = image[ypos:ypos+height, xpos:xpos+width]
            print(f"認識した顔のサイズ:{face_image.shape}")
            if face_image.shape[0] < 64 or face_image.shape[1] < 64:
                print("認識した顔のサイズが小さすぎます。")
                continue
            # 認識した顔のサイズ縮小
            face_image = cv2.resize(face_image, (64, 64))
            # 認識した顔のまわりを赤枠で囲む
            cv2.rectangle(image, (xpos, ypos), (xpos+width, ypos+height),
                          (255, 0, 0), thickness=2)
            # 認識した顔を1枚の画像を含む配列に変換
            face_image = np.expand_dims(face_image, axis=0)
            # 認識した顔から名前を特定
            name = detect_who(model, face_image)
            # 認識した顔に名前を描画
            cv2.putText(image, name, (xpos, ypos+height+20),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    # 顔が検出されなかった時
    else:
        print(f"顔を認識できません。")
    return image


# 顔認証ラベルを取得する関数　　detect_face()用の関数
def detect_who(model, face_image):
    name = ""
    result = model.predict(face_image)
    print(f"日本人の可能性:{result[0][0]*100:.3f}%")
    print(f"韓国人の可能性:{result[0][1]*100:.3f}%")
    # ラベルの作成
    name_number_label = np.argmax(result)
    if name_number_label == 0:
        name ="Japanese"
    elif name_number_label == 1:
        name ="Korean"
    return name


# サーチ関数
def search(keyword,index):
    crawler = BingImageCrawler(storage={"root_dir": "read"}, downloader_threads=4)
    crawler.crawl(keyword=keyword, max_num=index)
 
# 画像を参照してリザルト画像の作成。
def read_img(img_file_path,name):
    print("read_img 起動")
    # 画像ファイルの読み込み
    image = cv2.imread(img_file_path)
    # モデルファイルの読み込み
    model = keras.models.load_model("./meta/cnn.h5")
    # 顔認識
    result_image = detect_face(model,image)
    # 画像書き出し
    out_pass=f"./result/{name}.jpg"
    cv2.imwrite(out_pass,result_image)
    print(f"{name}の書き出し成功！")



    