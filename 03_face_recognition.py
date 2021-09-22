from genericpath import exists
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from cv2 import rectangle
from PIL import ImageFont, ImageDraw, Image
from VideoCaptureFrame import *
from FaceDataset import *
import os


class VideoCaptureExFrame(VideoCaptureFrame): 
    def __init__(self, master, width=640, height=480):
        super(VideoCaptureExFrame,self).__init__(master, width, height)
        
        # オーバーレイ画像を生成
        self.overlay_image = cv2.imread("face_frame.png", -1)
        self.overlay_image = cv2.resize(self.overlay_image, (width, height))

        # 顔判定用のカスケード分類機を読込む
        self.face_detector = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
        self.face_minsize_width = (FACE_FRAME_RIGHT - FACE_FRAME_MARGIN) - (FACE_FRAME_LEFT + FACE_FRAME_MARGIN)
        self.face_minsize_height = (FACE_FRAME_BOTTOM - FACE_FRAME_MARGIN) - (FACE_FRAME_TOP + FACE_FRAME_MARGIN)

        # 顔認証トレーニング情報を読込む
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('./trainer/trainer.yml')

        # Use HGS創英角ゴシックポップ体標準 to write Japanese.
        self.fontpath ='C:\Windows\Fonts\HGRPP1.TTC' # Windows10 だと C:\Windows\Fonts\ 以下にフォントがあります。
        self.font = ImageFont.truetype(self.fontpath, 24) # フォントサイズが16










    def update_cap(self):
        global registry_flag
        global registry_count

        bFaceFlag = False
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))

            # 顔判別
            temp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            face_image = frame[FACE_FRAME_TOP:FACE_FRAME_BOTTOM, FACE_FRAME_LEFT:FACE_FRAME_RIGHT]
            face_gray_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(face_gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(self.face_minsize_width,self.face_minsize_height))

            # オーバーレイ画像を重ね合わせる
            temp_image = self.overlay(frame, self.overlay_image, (0,0))
            
            # デバッグ用（顔認識有効枠）
            #rectangle(temp_image, (FACE_FRAME_LEFT, FACE_FRAME_TOP), (FACE_FRAME_RIGHT,FACE_FRAME_BOTTOM), (255,0,0), 3 )
            #rectangle(temp_image, ((FACE_FRAME_LEFT + FACE_FRAME_MARGIN), (FACE_FRAME_TOP + FACE_FRAME_MARGIN)), ((FACE_FRAME_RIGHT - FACE_FRAME_MARGIN),(FACE_FRAME_BOTTOM-FACE_FRAME_MARGIN)), (0,0,255), 3 )


            # 顔枠を表示
            for (x, y, w, h) in faces:
                bFaceFlag = True
                rectangle(temp_image, (FACE_FRAME_LEFT + x, FACE_FRAME_TOP + y), (FACE_FRAME_LEFT + x + w, FACE_FRAME_TOP + y + h), (255,0,0), 2)

                # 顔認証されているのか検索
                id, confidence = self.recognizer.predict(face_gray_image[y:y+h,x:x+w])
                if confidence < 70:
                    strName = dataset.getvalue(str(id))
                else:
                    strName = "未登録"

                strMessage = "{0} ({1})%".format(strName, round(100 - confidence))
                #strConfidence = "  {0}%".format(round(100 - confidence))

            # cv --> Pil
            temp_image = Image.fromarray(cv2.cvtColor(temp_image, cv2.COLOR_BGR2RGB))

            if bFaceFlag == True:
                draw = ImageDraw.Draw(temp_image)
                draw.text( xy=(x+5,y-5), text=strMessage, fill=(255,255,255), font= self.font)
                #cv2.putText(temp_image, strName, (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                #cv2.putText(temp_image, strConfidence, (x+5,y+5), self.font, 1, (255,255,0), 1)  

            self.tk_frame = ImageTk.PhotoImage(temp_image)
            self.create_image(0, 0, image=self.tk_frame, anchor='nw')

        else:
            self.create_rectangle(0, 0, self.width, self.height, fill="black")
            self.create_text(self.width/2, self.height/2, text="None", fill="#fff")

        self.after_id = self.after(10, self.update_cap)



# グローバル変数
dataset = FaceDataset()
app = Tk()


#----------------------------------------------------------------------------------------------
#- メイン処理
#----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #app = Tk()
    app.title("顔認証確認")
    app.geometry("700x600")
    
    #dataset = FaceDataset()
    #id = StringVar()
    #name = StringVar()

    # カメラ画像表示フレーム
    VideoCapture = VideoCaptureExFrame(master=app)

    VideoCapture.start_cap()

    app.mainloop()

    VideoCapture.stop_cap()




















