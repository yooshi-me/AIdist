# -*- coding:utf-8 -*-
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk


class Model():
    # 画像処理前か画像処理後かを指定
    BEFORE = 1
    AFTER = 2

    def __init__(self):

        # PIL画像オブジェクトを参照
        self.before_image = None
        self.after_image = None

        # Tkinter画像オブジェクトを参照
        self.before_image_tk = None
        self.after_image_tk = None

    def get_image(self, type):
        'Tkinter画像オブジェクトを取得する'

        if type == Model.BEFORE:
            if self.before_image is not None:
                # Tkinter画像オブジェクトに変換
                self.before_image_tk = ImageTk.PhotoImage(self.before_image)
            return self.before_image_tk

        elif type == Model.AFTER:
            if self.after_image is not None:
                # Tkinter画像オブジェクトに変換
                self.after_image_tk = ImageTk.PhotoImage(self.after_image)
            return self.after_image_tk

        else:
            return None

    def read(self, path):
        '画像の読み込みを行う'

        # pathの画像を読み込んでPIL画像オブジェクト生成
        self.before_image = Image.open(path)

    def round(self, value, min, max):
        'valueをminからmaxの範囲に丸める'
        
        ret = value
        if(value < min):
            ret = min
        if(value > max):
            ret = max

        return ret

    def crop(self, param):
        '画像をクロップ'

        if len(param) != 4:
            return
        if self.before_image is None:
            return

        print(param)
        # 画像上の選択範囲を取得（x1,y1）-（x2,y2）
        x1, y1, x2, y2 = param

        # 画像外の選択範囲を画像内に切り詰める
        x1 = self.round(x1, 0, self.before_image.width)
        x2 = self.round(x2, 0, self.before_image.width)
        y1 = self.round(y1, 0, self.before_image.height)
        y2 = self.round(y2, 0, self.before_image.height)
        if x2 - x1 < y2 - y1:
            x2 = x1 + (y2 - y1)
        else:
            y2 = y1 + (x2 - x1)
        
        new_img = self.before_image.crop((x1,y1,x2,y2))
        new_img.save("new.png")

        # x1 <= x2 になるように座標を調節
        if x1 <= x2:
            crop_x1 = x1
            crop_x2 = x2
        else:
            crop_x1 = x2
            crop_x2 = x1

        # y1 <= y2 になるように座標を調節
        if y1 <= y2:
            crop_y1 = y1
            crop_y2 = y2
        else:
            crop_y1 = y2
            crop_y2 = y1

        # PIL Imageのcropを実行
        self.after_image = self.before_image.crop(
            (
                crop_x1,
                crop_y1,
                crop_x2,
                crop_y2
            )
        )


class View():

    # キャンバス指定用
    LEFT_CANVAS = 1
    RIGHT_CANVAS = 2

    def __init__(self, app, model):

        self.master = app
        self.model = model

        # アプリ内のウィジェットを作成
        self.create_widgets()

    def create_widgets(self):
        'アプリ内にウィジェットを作成・配置する'

        # キャンバスのサイズ
        canvas_width = 400
        canvas_height = 400

        # キャンバスとボタンを配置するフレームの作成と配置
        self.main_frame = tkinter.Frame(
            self.master
        )
        self.main_frame.pack()

        # ラベルを配置するフレームの作成と配置
        self.sub_frame = tkinter.Frame(
            self.master
        )
        self.sub_frame.pack()

        # キャンバスを配置するフレームの作成と配置
        self.canvas_frame = tkinter.Frame(
            self.main_frame
        )
        self.canvas_frame.grid(column=1, row=1)

        # ボタンを８位するフレームの作成と配置
        self.button_frame = tkinter.Frame(
            self.main_frame
        )
        self.button_frame.grid(column=2, row=1)

        # １つ目のキャンバスの作成と配置
        self.left_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.left_canvas.grid(column=1, row=1)

        # ２つ目のキャンバスの作成と配置
        self.right_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.right_canvas.grid(column=2, row=1)


        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(
            self.button_frame,
            text="ファイル選択"
        )
        self.load_button.pack()

        # メッセージ表示ラベルの作成と配置

        # メッセージ更新用
        self.message = tkinter.StringVar()

        self.message_label = tkinter.Label(
            self.sub_frame,
            textvariable=self.message
        )
        self.message_label.pack()

    def draw_image(self, type):
        '画像をキャンバスに描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
            image = self.model.get_image(Model.BEFORE)
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
            image = self.model.get_image(Model.AFTER)
        else:
            return

        if image is not None:
            # キャンバス上の画像の左上座標を決定
            sx = (canvas.winfo_width() - image.width()) // 2
            sy = (canvas.winfo_height() - image.height()) // 2

            # キャンバスに描画済みの画像を削除
            objs = canvas.find_withtag("image")
            for obj in objs:
                canvas.delete(obj)

            # 画像をキャンバスの真ん中に描画
            canvas.create_image(
                sx, sy,
                image=image,
                anchor=tkinter.NW,
                tag="image"
            )

    def draw_selection(self, selection, type):
        '選択範囲を描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # 一旦描画済みの選択範囲を削除
        self.delete_selection(type)

        if selection:
            # 選択範囲を長方形で描画
            x1=selection[0]
            y1=selection[1]
            x2=selection[2]
            y2=selection[3]
            if x2 - x1 < y2 - y1:
                x2 = x1 + (y2 - y1)
            else:
                y2 = y1 + (x2 - x1)
            
            selection[0]=x1
            selection[1]=y1
            selection[2]=x2
            selection[3]=y2

            canvas.create_rectangle(
                selection[0],
                selection[1],
                selection[2],
                selection[3],
                outline="red",
                width=3,
                tag="selection_rectangle"
            )

    def delete_selection(self, type):
        '選択範囲表示用オブジェクトを削除する'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # キャンバスに描画済みの選択範囲を削除
        objs = canvas.find_withtag("selection_rectangle")
        for obj in objs:
            canvas.delete(obj)

    def draw_message(self, message):
        self.message.set(message)

    def select_file(self):
        'ファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(
            initialdir="."
        )
        return file_path


class Controller():

    INTERVAL = 50

    def __init__(self, app, model, view):
        self.master = app
        self.model = model
        self.view = view

        # マウスボタン管理用
        self.pressing = False
        self.selection = None

        # ラベル表示メッセージ管理用
        self.message = "ファイルを読み込んでください"

        self.set_events()

    def set_events(self):
        '受け付けるイベントを設定する'

        # キャンバス上のマウス押し下げ開始イベント受付
        self.view.left_canvas.bind(
            "<ButtonPress>",
            self.button_press
        )

        # キャンバス上のマウス動作イベント受付
        self.view.left_canvas.bind(
            "<Motion>",
            self.mouse_motion,
        )

        # キャンバス上のマウス押し下げ終了イベント受付
        self.view.left_canvas.bind(
            "<ButtonRelease>",
            self.button_release,
        )

        # 読み込みボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button

        # 画像の描画用のタイマーセット
        self.master.after(Controller.INTERVAL, self.timer)

    def timer(self):
        '一定間隔で画像等を描画'

        # 画像処理前の画像を左側のキャンバスに描画
        self.view.draw_image(
            View.LEFT_CANVAS
        )

        # 画像処理後の画像を右側のキャンバスに描画
        self.view.draw_image(
            View.RIGHT_CANVAS
        )

        # トリミング選択範囲を左側のキャンバスに描画
        self.view.draw_selection(
            self.selection,
            View.LEFT_CANVAS
        )

        # ラベルにメッセージを描画
        self.view.draw_message(
            self.message
        )

        # 再度タイマー設定
        self.master.after(Controller.INTERVAL, self.timer)

    def push_load_button(self):
        'ファイル選択ボタンが押された時の処理'

        # ファイル選択画面表示
        file_path = self.view.select_file()

        # 画像ファイルの読み込みと描画
        if len(file_path) != 0:
            self.model.read(file_path)

        self.selection = None

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(view.LEFT_CANVAS)

        # メッセージを更新
        self.message = "トリミングする範囲を指定してください"

    def button_press(self, event):
        'マウスボタン押し下げ開始時の処理'

        # マウスクリック中に設定
        self.pressing = True

        self.selection = None

        # 現在のマウスでの選択範囲を設定
        self.selection = [
            event.x,
            event.y,
            event.x,
            event.y
        ]

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(View.LEFT_CANVAS)

    def mouse_motion(self, event):
        'マウスボタン移動時の処理'

        if self.pressing:

            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

    def button_release(self, event):
        'マウスボタン押し下げ終了時の処理'

        if self.pressing:

            # マウスボタン押し下げ終了
            self.pressing = False

            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

            # 画像の描画位置を取得
            objs = self.view.left_canvas.find_withtag("image")
            if len(objs) != 0:
                draw_coord = self.view.left_canvas.coords(objs[0])

                # 選択範囲をキャンバス上の座標から画像上の座標に変換
                x1 = self.selection[0] - draw_coord[0]
                y1 = self.selection[1] - draw_coord[1]
                x2 = self.selection[2] - draw_coord[0]
                y2 = self.selection[3] - draw_coord[1]

                # 画像をcropでトリミング
                self.model.crop(
                    (int(x1), int(y1), int(x2), int(y2))
                )

                # メッセージを更新
                self.message = "トリミングしました！"


app = tkinter.Tk()

# アプリのウィンドウのサイズ設定
app.geometry("1000x430")
app.title("トリミングアプリ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()