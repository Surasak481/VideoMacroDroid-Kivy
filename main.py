from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        self.file_path = "/sdcard/Download/test.mp4"
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label = Label(text='Video to MacroDroid\nพร้อมใช้งาน!\n\n1. เลือกวิดี
