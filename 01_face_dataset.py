from genericpath import exists
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from cv2 import rectangle
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

    def update_cap(self):
        global registry_flag
        global registry_count

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
                rectangle(temp_image, (FACE_FRAME_LEFT + x, FACE_FRAME_TOP + y), (FACE_FRAME_LEFT + x + w, FACE_FRAME_TOP + y + h), (255,0,0), 2)
                
                # 登録開始がTrueの場合
                if registry_flag == True:
                    cv2.imwrite(registry_file_path + "/" + str(registry_count) + ".jpg", face_gray_image)
                    registry_count = registry_count + 1
                    if registry_count >= FACE_REGISTRY_COUNT:
                        # 登録終了
                        dataset.Insert(strId,strName)
                        dataset.save()
                        registry_flag = False

                        app.after(500, end_registry)
                        

            self.tk_frame = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(temp_image, cv2.COLOR_BGR2RGB)))
            self.create_image(0, 0, image=self.tk_frame, anchor='nw')


        else:
            self.create_rectangle(0, 0, self.width, self.height, fill="black")
            self.create_text(self.width/2, self.height/2, text="None", fill="#fff")

        self.after_id = self.after(10, self.update_cap)


#----------------------------------------------------------------------------------------------
#- 登録開始処理
#----------------------------------------------------------------------------------------------
def start_registry():
    global registry_flag
    global registry_count
    global registry_file_path
    global strId
    global strName

    registry_button.configure(state="disable")

    # IDを取得
    strId = id_edit.get()

    # 名前入力チェック
    strName = name_edit.get()
    if len(strName) == 0:
        messagebox.showerror("登録開始","名前が設定されていません")
        registry_button.configure(state="enable")
        return

    # 登録開始
    registry_flag = True
    registry_count = 0

    # 顔データ保存場所フォルダを生成
    os.makedirs(dataset.GetPath() + "/" + strId, exist_ok=True)
    registry_file_path = dataset.GetPath() + "/" + strId



#----------------------------------------------------------------------------------------------
#- 登録完了処理
#----------------------------------------------------------------------------------------------
def end_registry():
    messagebox.showinfo("登録完了","顔認証登録が完了しました")

    # IDをセット
    id_edit.configure(state="NORMAL")
    id_edit.delete(0,END)
    id_edit.insert(END,dataset.getnextid())
    id_edit.configure(state="readonly")

    # 名前を消す
    name_edit.delete(0,END)

    # [登録開始]ボタンを有効にする
    registry_button.configure(state="enable")



# グローバル変数
dataset = FaceDataset()
app = Tk()
id_frame = ttk.Frame(master=app)
id_label = ttk.Label(master=id_frame, text="ID    : ")
id_edit = ttk.Entry(master=id_frame, width=15, justify=LEFT)
name_frame = ttk.Frame(master=app)
name_label = ttk.Label(master=name_frame, text="名前 : ")
name_edit = ttk.Entry(master=name_frame, width=32, justify=LEFT)
registry_button = ttk.Button(master=app, text="登録開始", command=start_registry)
registry_flag = False
registry_count = 0
registry_file_path = ""
strId = ""
strName = ""



#----------------------------------------------------------------------------------------------
#- メイン処理
#----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #app = Tk()
    app.title("顔認証登録")
    app.geometry("700x600")
    
    #dataset = FaceDataset()
    #id = StringVar()
    #name = StringVar()

    # カメラ画像表示フレーム
    VideoCapture = VideoCaptureExFrame(master=app)

    # ID(読み取り専用)
    #id_frame = ttk.Frame(master=app)
    id_frame.pack(fill="x", padx=100, pady=10, ipadx=1, ipady=1)
    #id_label = ttk.Label(master=id_frame, text="ID    : ")
    id_label.pack(side=LEFT)
    #id_edit = ttk.Entry(master=id_frame, textvariable=id, width=15, justify=LEFT)
    id_edit.configure(state="readonly")
    id_edit.pack(side=LEFT)

    # 名前
    #name_frame = ttk.Frame(master=app)
    name_frame.pack(fill="x", padx=100, pady=2, ipadx=1, ipady=1)
    #name_label = ttk.Label(master=name_frame, text="名前 : ")
    name_label.pack(side=LEFT)
    #name_edit = ttk.Entry(master=name_frame, textvariable=name, width=32, justify=LEFT)
    name_edit.pack(side=LEFT)

    # [登録開始]ボタン
    #registry_button = ttk.Button(master=app, text="登録開始", command=None)
    registry_button.pack()


    # IDをセット
    id_edit.configure(state="NORMAL")
    id_edit.insert(END,dataset.getnextid())
    id_edit.configure(state="readonly")

    VideoCapture.start_cap()

    app.mainloop()

    VideoCapture.stop_cap()
















