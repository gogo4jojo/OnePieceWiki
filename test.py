import getpass
import bcrypt
from app import *
from conn import *

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.core.window import Window

class PasswordGUI(RelativeLayout):
    def __init__(self, app, **kwargs):
        super(PasswordGUI, self).__init__(**kwargs)
        self.app = app
        self.gui()
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        Window.size = (500, 200)
        self.this_gui = self
        with self.this_gui.canvas.before:
            Color(0.254902, 0.254902, 0.254902, 1)
            self.rect = Rectangle(size=self.this_gui.size, pos=self.this_gui.pos)

        self.this_gui.bind(pos=self.update_rect, size=self.update_rect)

        #this is for postgres
        self.salt = b'$2b$12$Djf8e6we2/mi4WFiU0tybO'
        self.hashed = b'$2b$12$Djf8e6we2/mi4WFiU0tybOLGHNx6.qCeL8Wnh9YBROhD3jY0W9ZEa'



        self.password_textbox = TextInput(text = "", 
                                          password="True", 
                                          multiline = False, 
                                          pos_hint ={'x':0.4, 'y':0.49}, 
                                          size_hint = (0.22, 0.15))
        self.this_gui.add_widget(self.password_textbox)

        self.label = Label(text = "Enter Password:", 
                            halign='left', 
                            pos_hint ={'x':0.18, 'y':0.49}, 
                            size_hint = (0.24, 0.21))
        self.label.bind(size=self.label.setter('text_size'))
        self.this_gui.add_widget(self.label)

        self.submit_button = Button(text = "Submit", 
                                    pos_hint ={'x':0.42, 'y':0.19}, 
                                    size_hint = (0.18, 0.11))
        self.this_gui.add_widget(self.submit_button)
        self.submit_button.bind(on_press = self.check_password)

        return self.this_gui

    def check_password(self, instance):
        global password
        password = self.password_textbox.text.encode('utf-8')
        hash = bcrypt.hashpw(password, self.salt)

        if hash == self.hashed:
            self.app.password = password
            self.app.switch_to_main_app()
        else:
            print("Access denied")

class MainApp(App):
    def build(self):
        self.root = BoxLayout()
        self.passwordGUI = PasswordGUI(app=self)
        self.root.add_widget(self.passwordGUI)
        return self.root

    def switch_to_main_app(self):
        self.root.clear_widgets() 
        x = str(self.password)
        x = x[2:len(x)-1]
        self.app = AppGUI(password=x)
        self.root.add_widget(self.app) 

if __name__ == '__main__':
    MainApp().run()
