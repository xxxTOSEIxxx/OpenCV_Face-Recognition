import cv2
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import numpy as np


FACE_FRAME_TOP = 70
FACE_FRAME_LEFT = 170
FACE_FRAME_BOTTOM = 370
FACE_FRAME_RIGHT = 480
FACE_FRAME_MARGIN = 50
FACE_REGISTRY_COUNT = 10


class VideoCaptureFrame(tk.Canvas):
    def __init__(self, master=None, width=640, height=480):
        super().__init__(master, width=width, height=height)
        self.width = width
        self.height = height

        # valiables configuration
        self.capture_flag = False

        # canvas configuration
        self.create_rectangle(0, 0, self.width, self.height, fill="black")
        self.pack()


    #----------------------------------------------------------------------------------------------
    #- キャプチャ開始
    #----------------------------------------------------------------------------------------------
    def start_cap(self):
        if not self.capture_flag:
            self.capture_flag = True
            self.capture = cv2.VideoCapture(0)
            self.after_id = self.after(10, self.update_cap)


    #----------------------------------------------------------------------------------------------
    #- キャプチャ画像更新
    #----------------------------------------------------------------------------------------------
    def update_cap(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))
            self.tk_frame = ImageTk.PhotoImage(
                Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                )
            )
            self.create_image(0, 0, image=self.tk_frame, anchor='nw')
        else:
            self.create_rectangle(0, 0, self.width, self.height, fill="black")
            self.create_text(self.width/2, self.height/2, text="None", fill="#fff")

        self.after_id = self.after(10, self.update_cap)


    #----------------------------------------------------------------------------------------------
    #- キャプチャ停止
    #----------------------------------------------------------------------------------------------
    def stop_cap(self):
        self.after_cancel(self.after_id)
        self.capture.release()
        cv2.destroyAllWindows()
        self.capture_flag = False


    #----------------------------------------------------------------------------------------------
    #- オーバーレイ処理
    #----------------------------------------------------------------------------------------------
    def overlay(self, cv_background_image, cv_overlay_image, point ):
        # OpenCV形式の画像をPIL形式に変換(α値含む)
        # 背景画像
        cv_rgb_bg_image = cv2.cvtColor(cv_background_image, cv2.COLOR_BGR2RGB)
        pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
        # オーバーレイ画像
        cv_rgb_ol_image = cv2.cvtColor(cv_overlay_image, cv2.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

        # composite()は同サイズ画像同士が必須のため、合成用画像を用意
        pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size, (255, 255, 255, 0))

        # 座標を指定し重ね合わせる
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
        result_image = Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

        # OpenCV形式画像へ変換
        cv_bgr_result_image = cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

        return cv_bgr_result_image





