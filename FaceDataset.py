import os
import pickle


FACE_DATA_SET_PATH = "./Dataset"
FACE_DIC_FILE_NAME = "FaceDict.dat"


class FaceDataset():
    def __init__(self):
        # Datasetフォルダが存在しない場合は生成する
        os.makedirs(FACE_DATA_SET_PATH, exist_ok=True)

        self.FaceDictFilePaht = FACE_DATA_SET_PATH + "/" + FACE_DIC_FILE_NAME
        self.FaceDict = {}
        self.load()


    #----------------------------------------------------------------------------------------------
    #- フォルダパスを取得
    #----------------------------------------------------------------------------------------------
    def GetPath(self):
        return FACE_DATA_SET_PATH


    #----------------------------------------------------------------------------------------------
    #- 辞書情報追加
    #----------------------------------------------------------------------------------------------
    def Insert(self, id, value):
        self.FaceDict.setdefault(id, value)


    #----------------------------------------------------------------------------------------------
    #- 辞書情報削除
    #----------------------------------------------------------------------------------------------
    def Delete(self, id):
        del self.FaceDict[id]


    #----------------------------------------------------------------------------------------------
    #- 辞書ファイルを読込む
    #----------------------------------------------------------------------------------------------
    def load(self):
        if os.path.exists(self.FaceDictFilePaht) == True:
            with open(self.FaceDictFilePaht, mode="rb") as fs:
                self.FaceDict = pickle.load(fs)
        else:
            self.FaceDict.clear()


    #----------------------------------------------------------------------------------------------
    #- 辞書情報を辞書ファイルに保存
    #----------------------------------------------------------------------------------------------
    def save(self):
        with open(self.FaceDictFilePaht, mode="wb") as fs:
                pickle.dump(self.FaceDict,fs)

    #----------------------------------------------------------------------------------------------
    #- 新規IDを取得
    #----------------------------------------------------------------------------------------------
    def getnextid(self):
        nextid = 1

        if os.path.exists(self.FaceDictFilePaht) == True:
            self.load()
            templist = sorted(self.FaceDict.keys())
            nextid = int(templist[-1]) + 1
        else:
            nextid = 1    

        return str(nextid)


    #----------------------------------------------------------------------------------------------
    #- 指定したIDの値を取得
    #----------------------------------------------------------------------------------------------
    def getvalue(self, id):
        return self.FaceDict.get(id, None)







