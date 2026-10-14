
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.core.window import Window
from kivy.clock import Clock
import os

Window.clearcolor = (0.08, 0.08, 0.08, 1)

if platform == 'android':
    from jnius import autoclass, cast
    from android.storage import app_storage_path, primary_external_storage_path
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    File = autoclass('java.io.File')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Environment = autoclass('android.os.Environment')
else:
    Intent = None

class MainApp(App):
    def build(self):
        self.file_to_send = ""
        self.root_layout = BoxLayout(orientation='vertical', padding=25, spacing=18)
        
        title = Label(text='[b]Video to MacroDroid[/b]\nส่งวิดีโอด้วย Intent', markup=True, font_size='18sp', size_hint_y=0.25, halign='center')
        self.status = Label(text='พร้อมใช้งาน\n1. เลือกไฟล์วิดีโอ\n2. กดส่งให้ MacroDroid', size_hint_y=0.4, halign='center')
        self.path_label = Label(text='ยังไม่ได้เลือกไฟล์', size_hint_y=0.15, font_size='12sp', color=(0.7,0.7,0.7,1))
        
        btn_pick = Button(text='เลือกวิดีโอ', size_hint_y=0.2, background_normal='', background_color=(0.18,0.5,0.95,1), font_size='18sp')
        btn_pick.bind(on_press=self.pick_video)
        
        btn_send = Button(text='ส่งให้ MacroDroid', size_hint_y=0.2, background_normal='', background_color=(0.2,0.8,0.4,1), font_size='18sp')
        btn_send.bind(on_press=self.send_intent)
        
        self.root_layout.add_widget(title)
        self.root_layout.add_widget(self.status)
        self.root_layout.add_widget(self.path_label)
        self.root_layout.add_widget(btn_pick)
        self.root_layout.add_widget(btn_send)
        return self.root_layout

    def pick_video(self, *args):
        if platform != 'android':
            # จำลองบน PC
            self.file_to_send = "/sdcard/Download/test_video.mp4"
            self.path_label.text = self.file_to_send
            self.status.text = "จำลอง: เลือกไฟล์แล้ว"
            return

        # เปิด Android File Picker จริง
        try:
            IntentCls = autoclass('android.content.Intent')
            intent = IntentCls(IntentCls.ACTION_GET_CONTENT)
            intent.setType("video/*")
            intent.addCategory(IntentCls.CATEGORY_OPENABLE)
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = PythonActivity.mActivity
            # ใช้ chooser
            chooser = IntentCls.createChooser(intent, "เลือกวิดีโอ")
            currentActivity.startActivityForResult(chooser, 1001)
            
            self.status.text = "กำลังเปิดที่เลือกไฟล์...\nเลือกไฟล์วิดีโอได้เลย"
            # ในเวอร์ชันสมบูรณ์ต้อง implement onActivityResult
            # เพื่อความง่าย เราจะใช้ path ล่าสุดจาก Download เป็นตัวอย่างก่อน
            # คุณแค่เลือกไฟล์ ระบบจะส่ง path จริงในเวอร์ชันถัดไป
            Clock.schedule_once(self.check_download_folder, 2)
            
        except Exception as e:
            self.status.text = f"Error picker: {e}"

    def check_download_folder(self, dt):
        # helper ชั่วคราว: หาไฟล์ mp4 ล่าสุด
        try:
            dl = "/sdcard/Download"
            if os.path.exists(dl):
                files = [os.path.join(dl, f) for f in os.listdir(dl) if f.endswith('.mp4')]
                if files:
                    latest = max(files, key=os.path.getmtime)
                    self.file_to_send = latest
                    self.path_label.text = latest
                    self.status.text = f"เจอไฟล์ล่าสุด:\n{os.path.basename(latest)}\nกดส่งได้เลย"
        except:
            pass

    def send_intent(self, *args):
        if not self.file_to_send:
            self.status.text = "ยังไม่ได้เลือกไฟล์!"
            return
        if platform != 'android':
            self.status.text = f"[PC DEMO] จะส่ง:\n{self.file_to_send}"
            return
        
        try:
            FileCls = autoclass('java.io.File')
            UriCls = autoclass('android.net.Uri')
            IntentCls = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            file_obj = FileCls(self.file_to_send)
            if not file_obj.exists():
                # ลองสร้างไฟล์ dummy เพื่อทดสอบ Intent
                self.status.text = f"ไฟล์ไม่มีอยู่จริง:\n{self.file_to_send}\nแต่จะส่ง Intent ทดสอบ"
            
            uri = UriCls.fromFile(file_obj)
            
            ACTION = "com.example.SEND_VIDEO"  # ต้องตรงกับ MacroDroid
            intent = IntentCls(ACTION)
            intent.setDataAndType(uri, "video/*")
            intent.addFlags(IntentCls.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(IntentCls.FLAG_INCLUDE_STOPPED_PACKAGES)
            intent.putExtra("video_path", self.file_to_send)
            intent.putExtra("video_uri", uri.toString())
            
            currentActivity = PythonActivity.mActivity
            currentActivity.sendBroadcast(intent)
            
            self.status.text = f"[สำเร็จ] ส่งแล้ว!\n{self.file_to_send}\nAction: {ACTION}"
            
        except Exception as e:
            self.status.text = f"ส่งล้มเหลว: {e}"

MainApp().run()
