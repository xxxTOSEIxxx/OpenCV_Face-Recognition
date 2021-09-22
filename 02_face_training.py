import cv2
import numpy as np
from PIL import Image
import os
from FaceDataset import *


FACE_TRAINER_PATH = "./trainer"


dataset = FaceDataset()
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")


#----------------------------------------------------------------------------------------------
#- 指定フォルダに格納されている顔認証データを取得する
#----------------------------------------------------------------------------------------------
def getImagesAndLabels(path):
    faceSamples=[]
    ids = []   

    for d in os.listdir(path):
        # ディレクトリの場合
        imagePath = path + "/" + d
        if os.path.isdir(imagePath) == True:
            # パスからIDを取得
            id = int(d)

            # その中のファイルが顔認証データのはずなので、顔認証データファイルを全て読込む
            for f in os.listdir(imagePath):
                imageFilePath = imagePath + "/" + f
                if os.path.isfile(imageFilePath) == True:
                    PIL_img = Image.open(imageFilePath).convert('L')
                    img_numpy = np.array(PIL_img,'uint8')
                    faces = detector.detectMultiScale(img_numpy)
                    for (x,y,w,h) in faces:
                        faceSamples.append(img_numpy[y:y+h,x:x+w])
                        ids.append(id)

    return faceSamples, ids


#----------------------------------------------------------------------------------------------
#- メイン処理
#----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    os.makedirs(FACE_TRAINER_PATH, exist_ok=True)

    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

    # Datasetフォルダに格納されている顔認証データを取得する
    faces,ids = getImagesAndLabels(dataset.GetPath())

    # 取得した顔認証データをもとにトレーニングする
    recognizer.train(faces, np.array(ids))

    # トレーニングデータをファイルに保存する
    recognizer.write('trainer/trainer.yml')

    print("\n [INFO] {0} faces trained. Exiting Program\n".format(len(np.unique(ids))))





