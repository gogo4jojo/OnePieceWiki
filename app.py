
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
from conn import *
from datetime import datetime
import re
from person_table import *
from report import *
from group_report import *
from df import *
from tkinter import Tk, filedialog
import bcrypt
import getpass

def start(password):
    global conn
    global cur
    conn = connection(password)

    if conn == None:
        return None
    else:
        cur = conn.cursor()
        return cur

def end():
    conn.close()
    
def valid_date(date):
    regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    return bool(re.match(regex, date))

class AppGUI(RelativeLayout):
    def __init__(self, password, **kwargs):
        super(AppGUI, self).__init__(**kwargs)
        self.password = password
        start(self.password)
        self.gui()
        self.buildPersonCombo()
        self.buildDevilFruitCombo()
        self.buildDfEaterCombo()
        self.buildSwordCombo()
        self.buildSwordsmanCombo()
        self.buildVesselCombo()
        self.buildGroupCombo()
        self.buildMembershipCombo()
        self.buildIslandCombo()
        self.buildPirateCombo()
        self.buildMarineCombo()
        self.buildArtifactCombo()

    def update_rect(self, instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        Window.size = (1279, 840)
        self.w1 = self
        with self.w1.canvas.before:
            Color(0.254902, 0.254902, 0.254902, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.tab1 = TabbedPanel(pos_hint ={'x':0, 'y':0}, size_hint = (1.00078, 1), do_default_tab = False)
        self.w1.add_widget(self.tab1)
        self.tab1_tab0 = TabbedPanelItem(text = "Insert/Delete")
        self.tab1_widget0 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.tab1_tab0.add_widget(self.tab1_widget0)
        self.obj = TabbedPanel(pos_hint ={'x':-0.0015674, 'y':-0.0359356}, size_hint = (1.00313, 1.04089), do_default_tab = False)
        self.tab1_widget0.add_widget(self.obj)

        self.person_image = None
        self.df_image = None
        self.file = None
        self.group_image = None

        #INSERT PERSON TAB 
        self.build_person_tab()

        #INSERT DEVIL FRUIT TAB
        self.build_df_tab()

        #INSERT DEVIL FRUIT EATER TAB
        self.build_df_eater_tab()

        #INSERT SWORD TAB
        self.build_sword_tab()

        #INSERT SWORDSMAN TAB
        self.build_swordsman_tab()

        #INSERT PIRATE TAB
        self.build_pirate_tab()

        #INSERT MARINE TAB
        self.build_marine_tab()
        
        #INSERT ISLAND TAB
        self.build_island_tab()

        #INSERT GROUP TAB
        self.build_group_tab()
        
        #INSERT MEMBERSHIP TAB
        self.build_membership_tab()

        #INSERT VESSEL TAB
        self.build_vessel_tab()
        
        #INSERT ARTIFACT TAB
        self.build_artifact_tab()

        
        #UPDATE TAB
        self.tab1_update = TabbedPanelItem(text = "Update")
        self.update_tabs = TabbedPanel(pos_hint ={'x':0, 'y':0}, size_hint = (1.00078, 1), do_default_tab = False)
        
        self.tab1_update.add_widget(self.update_tabs)

        self.tab1_widget1 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.update_tabs.add_widget(self.tab1_widget1)
        self.tab1.add_widget(self.update_tabs)

        self.tab1.add_widget(self.tab1_update)

        self.build_update_person_tab()

        self.build_update_df_tab()

        #PERSON TABLE TAB
        self.tab1_tab_table = TabbedPanelItem(text="Person Table")
        self.table_widget = PersonTable(password=self.password)
        self.tab1_tab_table.add_widget(self.table_widget)
        self.tab1.add_widget(self.tab1_tab_table)

        #REPORT TAB
        self.report_tab = TabbedPanelItem(text = "Person Report")
        self.report_widget = Report(password=self.password)
        self.report_tab.add_widget(self.report_widget)
        self.tab1.add_widget(self.report_tab)

        #DF REPORT TAB
        self.report_df_tab = TabbedPanelItem(text = "DF Report")
        self.report_df_widget = DevilFruit(password=self.password)
        self.report_df_tab.add_widget(self.report_df_widget)
        self.tab1.add_widget(self.report_df_tab)

        self.report_group_tab = TabbedPanelItem(text = "Group Report")
        self.report_group_widget = GroupReport(password=self.password)
        self.report_group_tab.add_widget(self.report_group_widget)
        self.tab1.add_widget(self.report_group_tab)
        
        return self.w1

    def build_update_df_tab(self):
        self.update_df_tab = TabbedPanelItem(text="Devil Fruit")
        self.obj_widget_update_df = RelativeLayout(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 1))
        self.update_df_tab.add_widget(self.obj_widget_update_df)

        self.label_df = Label(text="Devil Fruit:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.841388}, size_hint=(0.0705329, 0.0520446))
        self.label_df.bind(size=self.label_df.setter('text_size'))
        self.obj_widget_update_df.add_widget(self.label_df)

        self.df_combo3 = Spinner(text="", pos_hint={'x': 0.10815, 'y': 0.841388}, size_hint=(0.3, 0.039653))
        self.obj_widget_update_df.add_widget(self.df_combo3)

        self.label_description_df = Label(text="Description:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.7}, size_hint=(0.0705329, 0.0520446))
        self.label_description_df.bind(size=self.label_description_df.setter('text_size'))
        self.obj_widget_update_df.add_widget(self.label_description_df)

        self.df_description = TextInput(hint_text="Enter new description", multiline=True, pos_hint={'x': 0.5, 'y': 0.7}, size_hint=(0.3, 0.2))
        self.obj_widget_update_df.add_widget(self.df_description)

        self.label_image_df = Label(text="Image:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.6}, size_hint=(0.0705329, 0.0520446))
        self.label_image_df.bind(size=self.label_image_df.setter('text_size'))
        self.obj_widget_update_df.add_widget(self.label_image_df)

        self.upload_status_label_df = Label(text="No file selected", pos_hint={'x': 0.10815, 'y': 0.6}, size_hint=(0.25, 0.039653))
        self.obj_widget_update_df.add_widget(self.upload_status_label_df)

        self.upload_image_button_df = Button(text="Upload Image", pos_hint={'x': 0.37, 'y': 0.6}, size_hint=(0.15, 0.039653))
        self.obj_widget_update_df.add_widget(self.upload_image_button_df)
        self.upload_image_button_df.bind(on_press=self.upload_df_image)

        self.label_update_df = Label(text="UPDATE", halign='left', pos_hint={'x': 0.0376176, 'y': 0.08}, size_hint=(0.0862069, 0.0644362))
        self.label_update_df.bind(size=self.label_update_df.setter('text_size'))
        self.obj_widget_update_df.add_widget(self.label_update_df)

        self.update_df_button = Button(text="Update", pos_hint={'x': 0.2, 'y': 0.08}, size_hint=(0.1, 0.039653))
        self.obj_widget_update_df.add_widget(self.update_df_button)
        self.update_df_button.bind(on_press=self.update_df)

        self.update_tabs.add_widget(self.update_df_tab)

    def build_update_person_tab(self):
        self.update_person_tab = TabbedPanelItem(text="Update Person")
        self.obj_widget_update = RelativeLayout(pos_hint={'x': 0, 'y': 0}, size_hint=(1, 1))
        self.update_person_tab.add_widget(self.obj_widget_update)

        self.label_0 = Label(text="Person:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.841388}, size_hint=(0.0705329, 0.0520446))
        self.label_0.bind(size=self.label_0.setter('text_size'))
        self.obj_widget_update.add_widget(self.label_0)

        self.person_combo13 = Spinner(text="", pos_hint={'x': 0.10815, 'y': 0.841388}, size_hint=(0.15, 0.039653))
        self.obj_widget_update.add_widget(self.person_combo13)

        self.label_last_seen = Label(text="Last Seen:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.77943}, size_hint=(0.0705329, 0.0520446))
        self.label_last_seen.bind(size=self.label_last_seen.setter('text_size'))
        self.obj_widget_update.add_widget(self.label_last_seen)

        self.island_combo6 = Spinner(text="", pos_hint={'x': 0.10815, 'y': 0.77943}, size_hint=(0.15, 0.039653))
        self.obj_widget_update.add_widget(self.island_combo6)

        self.label_description = Label(text="Description:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.7}, size_hint=(0.0705329, 0.0520446))
        self.label_description.bind(size=self.label_description.setter('text_size'))
        self.obj_widget_update.add_widget(self.label_description)

        self.person_description = TextInput(hint_text="Enter description", multiline=True, pos_hint={'x': 0.3, 'y': 0.7}, size_hint=(0.4, 0.2))
        self.obj_widget_update.add_widget(self.person_description)

        self.label_image = Label(text="Image:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.6}, size_hint=(0.0705329, 0.0520446))
        self.label_image.bind(size=self.label_image.setter('text_size'))
        self.obj_widget_update.add_widget(self.label_image)

        self.upload_status_label3 = Label(text="No file selected", pos_hint={'x': 0.10815, 'y': 0.6}, size_hint=(0.25, 0.039653))
        self.obj_widget_update.add_widget(self.upload_status_label3)

        self.upload_image_button2 = Button(text="Upload Image", pos_hint={'x': 0.37, 'y': 0.6}, size_hint=(0.15, 0.039653))
        self.obj_widget_update.add_widget(self.upload_image_button2)
        self.upload_image_button2.bind(on_press=self.upload_person_image)

        self.label_update = Label(text="UPDATE", halign='left', pos_hint={'x': 0.0376176, 'y': 0.08}, size_hint=(0.0862069, 0.0644362))
        self.label_update.bind(size=self.label_update.setter('text_size'))
        self.obj_widget_update.add_widget(self.label_update)

        self.update_person_button = Button(text="Update", pos_hint={'x': 0.2, 'y': 0.08}, size_hint=(0.1, 0.039653))
        self.obj_widget_update.add_widget(self.update_person_button)
        self.update_person_button.bind(on_press=self.update_person)
        
        self.update_tabs.add_widget(self.update_person_tab)

    def build_person_tab(self):
        self.person_tab = TabbedPanelItem(text = "Person")
        self.obj_widget0 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.person_tab.add_widget(self.obj_widget0)

        self.label_image = Label(text="Image:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.172}, size_hint=(0.0705329, 0.039653))
        self.label_image.bind(size=self.label_image.setter('text_size'))
        self.obj_widget0.add_widget(self.label_image)
        self.upload_status_label = Label(text="No file selected", pos_hint={'x': 0.10815, 'y': 0.172}, size_hint=(0.0705329, 0.039653))
        self.obj_widget0.add_widget(self.upload_status_label)
        self.upload_image_button = Button(text="Upload", pos_hint={'x': 0.2, 'y': 0.172}, size_hint=(0.1, 0.039653))
        self.obj_widget0.add_widget(self.upload_image_button)
        self.upload_image_button.bind(on_press=self.upload_image)

        self.insert_person_button = Button(text="Insert", pos_hint={'x': 0.07, 'y': 0.08}, size_hint=(0.0705329, 0.039653))
        self.obj_widget0.add_widget(self.insert_person_button)
        self.insert_person_button.bind(on_press=self.insert_person)
        self.description_box = TextInput(hint_text="Enter description", multiline=True, pos_hint={'x': 0.3, 'y': 0.7}, size_hint=(0.4, 0.2))
        self.obj_widget0.add_widget(self.description_box)
        self.label4 = Label(text = "INSERT", halign='left', pos_hint ={'x':0.0376176, 'y':0.903346}, size_hint = (0.0862069, 0.0644362))
        self.label4.bind(size=self.label4.setter('text_size'))
        self.obj_widget0.add_widget(self.label4)
        self.label5 = Label(text = "fname:", halign='left', pos_hint ={'x':0.0376176, 'y':0.841388}, size_hint = (0.101881, 0.0520446))
        self.label5.bind(size=self.label5.setter('text_size'))
        self.obj_widget0.add_widget(self.label5)
        self.label6 = Label(text = "mname:", halign='left', pos_hint ={'x':0.0376176, 'y':0.77943}, size_hint = (0.0705329, 0.0520446))
        self.label6.bind(size=self.label6.setter('text_size'))
        self.obj_widget0.add_widget(self.label6)
        self.label7 = Label(text = "lname:", halign='left', pos_hint ={'x':0.0376176, 'y':0.717472}, size_hint = (0.0705329, 0.0520446))
        self.label7.bind(size=self.label7.setter('text_size'))
        self.obj_widget0.add_widget(self.label7)
        self.label8 = Label(text = "age:", halign='left', pos_hint ={'x':0.0376176, 'y':0.655514}, size_hint = (0.0705329, 0.0520446))
        self.label8.bind(size=self.label8.setter('text_size'))
        self.obj_widget0.add_widget(self.label8)
        self.label9 = Label(text = "gender:", halign='left', pos_hint ={'x':0.0376176, 'y':0.605948}, size_hint = (0.0705329, 0.039653))
        self.label9.bind(size=self.label9.setter('text_size'))
        self.obj_widget0.add_widget(self.label9)
        self.label10 = Label(text = "race:", halign='left', pos_hint ={'x':0.0376176, 'y':0.494424}, size_hint = (0.0705329, 0.0520446))
        self.label10.bind(size=self.label10.setter('text_size'))
        self.obj_widget0.add_widget(self.label10)
        self.label11 = Label(text = "hometown:", halign='left', pos_hint ={'x':0.0376176, 'y':0.432466}, size_hint = (0.0705329, 0.0520446))
        self.label11.bind(size=self.label11.setter('text_size'))
        self.obj_widget0.add_widget(self.label11)
        self.label12 = Label(text = "birthday:", halign='left', pos_hint ={'x':0.0376176, 'y':0.3829}, size_hint = (0.0705329, 0.039653))
        self.label12.bind(size=self.label12.setter('text_size'))
        self.obj_widget0.add_widget(self.label12)
        self.label13 = Label(text = "height:", halign='left', pos_hint ={'x':0.0376176, 'y':0.296159}, size_hint = (0.0705329, 0.0520446))
        self.label13.bind(size=self.label13.setter('text_size'))
        self.obj_widget0.add_widget(self.label13)
        self.label15 = Label(text = "job:", halign='left', pos_hint ={'x':0.0376176, 'y':0.234201}, size_hint = (0.0705329, 0.039653))
        self.label15.bind(size=self.label15.setter('text_size'))
        self.obj_widget0.add_widget(self.label15)
        self.fname_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.841388}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.fname_box)
        self.mname_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.77943}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.mname_box)
        self.lname_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.717472}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.lname_box)
        self.age_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.655514}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.age_box)
        self.race_box = Spinner(text = "", values = ("", "Human", "Giant", "Fishman", "Mermaid", "Mink", "Lunarian", "Oni", "Skypeian", "Animal", "Dwarf", "Fairy", "Buccaneer", "Celestial Dragon"), pos_hint ={'x':0.10815, 'y':0.494424}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.race_box)
        self.birthday_box = TextInput(hint_text="YYYY-MM-DD", text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.370508}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.birthday_box)
        self.height_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.296159}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.height_box)
        self.gender_box = Spinner(text = "", values = ("?", "M", "F"), pos_hint ={'x':0.10815, 'y':0.593556}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.gender_box)
        self.island_combo2 = Spinner(text = "", pos_hint ={'x':0.10815, 'y':0.432466}, size_hint = (0.15, 0.039653))
        self.obj_widget0.add_widget(self.island_combo2)
        self.label16 = Label(text = "DELETE", halign='left', pos_hint ={'x':0.8, 'y':0.7}, size_hint = (0.0705329, 0.039653))
        self.label16.bind(size=self.label16.setter('text_size'))
        self.obj_widget0.add_widget(self.label16)
        self.delete_person_button = Button(text = "Delete", pos_hint ={'x':0.9, 'y':0.65}, size_hint = (0.0705329, 0.039653))
        self.obj_widget0.add_widget(self.delete_person_button)
        self.delete_person_button.bind(on_press = self.delete_person)
        self.kill_person_button = Button(text = "Kill", pos_hint ={'x':0.9, 'y':0.55}, size_hint = (0.0705329, 0.039653))
        self.obj_widget0.add_widget(self.kill_person_button)
        self.kill_person_button.bind(on_press = self.kill_person)
        self.person_combo = Spinner(text = "", pos_hint ={'x':0.8, 'y':0.65}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.person_combo)
        self.error_label = Label(text = "", halign='left', pos_hint ={'x':0.225705, 'y':0.14746}, size_hint = (0.713166, 0.510533))
        self.error_label.bind(size=self.error_label.setter('text_size'))
        self.obj_widget0.add_widget(self.error_label)
        self.job_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.10815, 'y':0.221809}, size_hint = (0.0862069, 0.039653))
        self.obj_widget0.add_widget(self.job_box)
        self.obj.add_widget(self.person_tab)

    def build_df_tab(self):
        self.df_tab = TabbedPanelItem(text = "Devil Fruit")
        self.obj_widget1 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.df_tab.add_widget(self.obj_widget1)
        self.label18 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0532915, 'y':0.915737}, size_hint = (0.0705329, 0.039653))
        self.label18.bind(size=self.label18.setter('text_size'))
        self.obj_widget1.add_widget(self.label18)
        self.label19 = Label(text = "Name:", halign='left', pos_hint ={'x':0.0532915, 'y':0.828996}, size_hint = (0.0705329, 0.039653))
        self.label19.bind(size=self.label19.setter('text_size'))
        self.obj_widget1.add_widget(self.label19)
        self.label20 = Label(text = "Type:", halign='left', pos_hint ={'x':0.0532915, 'y':0.754647}, size_hint = (0.0705329, 0.039653))
        self.label20.bind(size=self.label20.setter('text_size'))
        self.obj_widget1.add_widget(self.label20)
        self.label22 = Label(text = "Awakened:", halign='left', pos_hint ={'x':0.0532915, 'y':0.61834}, size_hint = (0.0705329, 0.039653))
        self.label22.bind(size=self.label22.setter('text_size'))
        self.obj_widget1.add_widget(self.label22)
        self.df_name_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.147335, 'y':0.828996}, size_hint = (0.148903, 0.039653))
        self.obj_widget1.add_widget(self.df_name_box)
        self.df_type_combo = Spinner(text = "", values = ("", "Paramecia", "Logia", "Zoan", "Mythical Zoan", "Ancient Zoan", "Artificial Zoan"), pos_hint ={'x':0.147335, 'y':0.754647}, size_hint = (0.148903, 0.039653))
        self.obj_widget1.add_widget(self.df_type_combo)
        self.awakened_combo = Spinner(text = "false", values = ("false", "true"), pos_hint ={'x':0.147335, 'y':0.61834}, size_hint = (0.148903, 0.039653))
        self.obj_widget1.add_widget(self.awakened_combo)
        self.description_box2 = TextInput(hint_text="Enter description", multiline=True, pos_hint={'x': 0.1, 'y': 0.3}, size_hint=(0.4, 0.2))
        self.obj_widget1.add_widget(self.description_box2)

        # self.label_image2 = Label(text="Image:", halign='left', pos_hint={'x': 0.0532915, 'y': 0.55}, size_hint=(0.0705329, 0.039653))
        # self.label_image.bind(size=self.label_image2.setter('text_size'))
        # self.obj_widget1.add_widget(self.label_image2)
        # self.upload_status_label_df = Label(text="No file selected", pos_hint={'x': 0.10815, 'y': 0.55}, size_hint=(0.0705329, 0.039653))
        # self.obj_widget1.add_widget(self.upload_status_label_df)
        # self.upload_df_image_button = Button(text="Upload", pos_hint={'x': 0.2, 'y': 0.55}, size_hint=(0.1, 0.039653))
        # self.upload_df_image_button.bind(on_press=self.upload_df_image)
        # self.obj_widget1.add_widget(self.upload_df_image_button)

        self.label24 = Label(text = "Delete", halign='left', pos_hint ={'x':0.617555, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label24.bind(size=self.label24.setter('text_size'))
        self.obj_widget1.add_widget(self.label24)
        self.button5 = Button(text = "Delete", pos_hint ={'x':0.85, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.obj_widget1.add_widget(self.button5)
        self.button5.bind(on_press = self.delete_df)
        self.insert_df_button = Button(text = "Insert", pos_hint ={'x':0.115987, 'y':0.2}, size_hint = (0.0783699, 0.039653))
        self.obj_widget1.add_widget(self.insert_df_button)
        self.insert_df_button.bind(on_press = self.insert_df)
        self.df_combo = Spinner(text = "", pos_hint ={'x':0.617555, 'y':0.816605}, size_hint = (0.22, 0.039653))
        self.obj_widget1.add_widget(self.df_combo)
        self.obj.add_widget(self.df_tab)

    def build_df_eater_tab(self):
        self.df_eater_tab = TabbedPanelItem(text = "DF Eater")
        self.obj_widget9 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.df_eater_tab.add_widget(self.obj_widget9)

        self.label47 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0532915, 'y':0.915737}, size_hint = (0.0705329, 0.039653))
        self.label47.bind(size=self.label47.setter('text_size'))
        self.obj_widget9.add_widget(self.label47)

        self.label48 = Label(text = "Choose eater:", halign='left', pos_hint ={'x':0.0532915, 'y':0.85}, size_hint = (0.0705329, 0.039653))
        self.label48.bind(size=self.label48.setter('text_size'))
        self.obj_widget9.add_widget(self.label48)

        self.label49 = Label(text = "Choose fruit:", halign='left', pos_hint ={'x':0.0532915, 'y':0.81}, size_hint = (0.0705329, 0.039653))
        self.label49.bind(size=self.label49.setter('text_size'))
        self.obj_widget9.add_widget(self.label49)

        self.insert_df_eater_button = Button(text = "Insert", pos_hint ={'x':0.1, 'y':0.7}, size_hint = (0.0783699, 0.039653))
        self.insert_df_eater_button.bind(on_press = self.insert_df_eater)
        self.obj_widget9.add_widget(self.insert_df_eater_button)

        self.person_combo8 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.85}, size_hint = (0.22, 0.039653))
        self.obj_widget9.add_widget(self.person_combo8)

        self.df_combo2 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.81}, size_hint = (0.22, 0.039653))
        self.obj_widget9.add_widget(self.df_combo2)

        self.label50 = Label(text = "Delete", halign='left', pos_hint ={'x':0.617555, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label50.bind(size=self.label50.setter('text_size'))
        self.obj_widget9.add_widget(self.label50)

        self.delete_df_eater_button = Button(text = "Delete", pos_hint ={'x':0.85, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.obj_widget9.add_widget(self.delete_df_eater_button)
        self.delete_df_eater_button.bind(on_press = self.delete_df_eater)
        
        self.df_eater_combo = Spinner(text = "", pos_hint ={'x':0.617555, 'y':0.816605}, size_hint = (0.22, 0.039653))
        self.obj_widget9.add_widget(self.df_eater_combo)

        self.obj.add_widget(self.df_eater_tab)

    def build_sword_tab(self):
        self.sword_tab = TabbedPanelItem(text = "Sword")
        self.obj_widget2 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.sword_tab.add_widget(self.obj_widget2)
        self.label25 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0768025, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label25.bind(size=self.label25.setter('text_size'))
        self.obj_widget2.add_widget(self.label25)
        self.label26 = Label(text = "Name:", halign='left', pos_hint ={'x':0.0768025, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.label26.bind(size=self.label26.setter('text_size'))
        self.obj_widget2.add_widget(self.label26)
        self.label27 = Label(text = "Type:", halign='left', pos_hint ={'x':0.0768025, 'y':0.742255}, size_hint = (0.0705329, 0.039653))
        self.label27.bind(size=self.label27.setter('text_size'))
        self.obj_widget2.add_widget(self.label27)
        self.label28 = Label(text = "Classification:", halign='left', pos_hint ={'x':0.0768025, 'y':0.667906}, size_hint = (0.0940439, 0.039653))
        self.label28.bind(size=self.label28.setter('text_size'))
        self.obj_widget2.add_widget(self.label28)
        self.label29 = Label(text = "Grade:", halign='left', pos_hint ={'x':0.0768025, 'y':0.568773}, size_hint = (0.0705329, 0.039653))
        self.label29.bind(size=self.label29.setter('text_size'))
        self.obj_widget2.add_widget(self.label29)
        # self.label30 = Label(text = "Owner:", halign='left', pos_hint ={'x':0.0768025, 'y':0.494424}, size_hint = (0.0705329, 0.039653))
        # self.label30.bind(size=self.label30.setter('text_size'))
        # self.obj_widget2.add_widget(self.label30)
        self.label31 = Label(text = "Delete", halign='left', pos_hint ={'x':0.672414, 'y':0.878563}, size_hint = (0.0705329, 0.039653))
        self.label31.bind(size=self.label31.setter('text_size'))
        self.obj_widget2.add_widget(self.label31)
        self.sword_name_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.18652, 'y':0.816605}, size_hint = (0.133229, 0.039653))
        self.obj_widget2.add_widget(self.sword_name_box)
        self.sword_type_combo = Spinner(text = "axe", values = ("axe", "cutlass", "dao", "jian", "kanabo", "katana", "kogatana", "kukri", "longsword", "machete", "naginata", "nandao", "nodachi", "rapier", "saber", "shikomizue", "shinai", "shirasaya", "shotel", "tanto", "urumi", "wakizashi", "zanbato"), pos_hint ={'x':0.18652, 'y':0.742255}, size_hint = (0.133229, 0.039653))
        self.obj_widget2.add_widget(self.sword_type_combo)
        self.sword_class_combo = Spinner(text = "", values = ("", "Meito", "Kokuto", "Yoto"), pos_hint ={'x':0.18652, 'y':0.655514}, size_hint = (0.133229, 0.039653))
        self.obj_widget2.add_widget(self.sword_class_combo)
        self.sword_grade_combo = Spinner(text = "", values = ("", "Great","Skillful", "Great", "Supreme"), pos_hint ={'x':0.18652, 'y':0.568773}, size_hint = (0.133229, 0.039653))
        self.obj_widget2.add_widget(self.sword_grade_combo)
        # self.person_combo3 = Spinner(text = "", pos_hint ={'x':0.18652, 'y':0.482032}, size_hint = (0.133229, 0.039653))
        # self.obj_widget2.add_widget(self.person_combo3)
        self.sword_combo = Spinner(text = "", pos_hint ={'x':0.672414, 'y':0.816605}, size_hint = (0.125392, 0.039653))
        self.obj_widget2.add_widget(self.sword_combo)
        self.button7 = Button(text = "Delete", pos_hint ={'x':0.844828, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.obj_widget2.add_widget(self.button7)
        self.button7.bind(on_press = self.delete_sword)
        self.insert_sword_button = Button(text = "Insert", pos_hint ={'x':0.10815, 'y':0.320942}, size_hint = (0.0705329, 0.039653))
        self.obj_widget2.add_widget(self.insert_sword_button)
        self.insert_sword_button.bind(on_press = self.insert_sword)
        self.obj.add_widget(self.sword_tab)

    def build_swordsman_tab(self):
        self.swordsman_tab = TabbedPanelItem(text = "Swordsman")
        self.obj_widget10 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.swordsman_tab.add_widget(self.obj_widget10)

        self.label65 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0532915, 'y':0.915737}, size_hint = (0.0705329, 0.039653))
        self.label65.bind(size=self.label65.setter('text_size'))
        self.obj_widget10.add_widget(self.label65)

        self.label66 = Label(text = "Choose swordsman:", halign='left', pos_hint ={'x':0.0532915, 'y':0.85}, size_hint = (0.0705329, 0.039653))
        self.label66.bind(size=self.label66.setter('text_size'))
        self.obj_widget10.add_widget(self.label66)

        self.label67 = Label(text = "Choose sword:", halign='left', pos_hint ={'x':0.0532915, 'y':0.81}, size_hint = (0.0705329, 0.039653))
        self.label67.bind(size=self.label67.setter('text_size'))
        self.obj_widget10.add_widget(self.label67)

        self.insert_swordsman_button = Button(text = "Insert", pos_hint ={'x':0.1, 'y':0.7}, size_hint = (0.0783699, 0.039653))
        self.insert_swordsman_button.bind(on_press = self.insert_swordsman)
        self.obj_widget10.add_widget(self.insert_swordsman_button)

        self.person_combo9 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.85}, size_hint = (0.22, 0.039653))
        self.obj_widget10.add_widget(self.person_combo9)

        self.sword_combo2 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.81}, size_hint = (0.22, 0.039653))
        self.obj_widget10.add_widget(self.sword_combo2)

        self.label68 = Label(text = "Delete", halign='left', pos_hint ={'x':0.617555, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label68.bind(size=self.label68.setter('text_size'))
        self.obj_widget10.add_widget(self.label68)

        self.delete_swordsman_button = Button(text = "Delete", pos_hint ={'x':0.85, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.obj_widget10.add_widget(self.delete_swordsman_button)
        self.delete_swordsman_button.bind(on_press = self.delete_swordsman)
        
        self.swordsman_combo = Spinner(text = "", pos_hint ={'x':0.617555, 'y':0.816605}, size_hint = (0.22, 0.039653))
        self.obj_widget10.add_widget(self.swordsman_combo)

        self.obj.add_widget(self.swordsman_tab)

    def build_pirate_tab(self):
        self.pirate_tab = TabbedPanelItem(text = "Pirate")
        self.obj_widget3 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.pirate_tab.add_widget(self.obj_widget3)
        self.label32 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0532915, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label32.bind(size=self.label32.setter('text_size'))
        self.obj_widget3.add_widget(self.label32)
        self.label48 = Label(text = "Person:", halign='left', pos_hint ={'x':0.0689655, 'y':0.791822}, size_hint = (0.0705329, 0.039653))
        self.label48.bind(size=self.label48.setter('text_size'))
        self.obj_widget3.add_widget(self.label48)
        self.label49 = Label(text = "Role:", halign='left', pos_hint ={'x':0.0689655, 'y':0.705081}, size_hint = (0.0705329, 0.039653))
        self.label49.bind(size=self.label49.setter('text_size'))
        self.obj_widget3.add_widget(self.label49)
        # self.label50 = Label(text = "Crew:", halign='left', pos_hint ={'x':0.0689655, 'y':0.605948}, size_hint = (0.0705329, 0.039653))
        # self.label50.bind(size=self.label50.setter('text_size'))
        # self.obj_widget3.add_widget(self.label50)
        self.label51 = Label(text = "Bounty:", halign='left', pos_hint ={'x':0.0689655, 'y':0.519207}, size_hint = (0.0705329, 0.039653))
        self.label51.bind(size=self.label51.setter('text_size'))
        self.obj_widget3.add_widget(self.label51)
        self.label52 = Label(text = "Active:", halign='left', pos_hint ={'x':0.0689655, 'y':0.420074}, size_hint = (0.0705329, 0.039653))
        self.label52.bind(size=self.label52.setter('text_size'))
        self.obj_widget3.add_widget(self.label52)
        self.person_combo6 = Spinner(text = "", pos_hint ={'x':0.155172, 'y':0.791822}, size_hint = (0.125392, 0.039653))
        self.obj_widget3.add_widget(self.person_combo6)
        self.role_combo = Spinner(text = "Captain", values = ("Captain", "1st Commander", "2nd Commander", "3rd Commander", "Commander", "First Mate", "Second Mate", "Swordsman", "Navigator", "Sniper", "Cook", "Doctor", "Archaeologist", "Shipwright", "Musician", "Helmsman", "Fodder"), pos_hint ={'x':0.155172, 'y':0.692689}, size_hint = (0.125392, 0.039653))
        self.obj_widget3.add_widget(self.role_combo)
        # self.group_combo2 = Spinner(text = "", pos_hint ={'x':0.155172, 'y':0.593556}, size_hint = (0.125392, 0.039653))
        # self.obj_widget3.add_widget(self.group_combo2)
        self.pirate_bounty_box = TextInput(text = "", input_filter="int", multiline = False, pos_hint ={'x':0.155172, 'y':0.506815}, size_hint = (0.125392, 0.039653))
        self.obj_widget3.add_widget(self.pirate_bounty_box)
        self.pirate_active_combo = Spinner(text = "true", values = ("true", "false"), pos_hint ={'x':0.155172, 'y':0.407683}, size_hint = (0.125392, 0.039653))
        self.obj_widget3.add_widget(self.pirate_active_combo)
        self.insert_pirate_button = Button(text = "Insert", pos_hint ={'x':0.115987, 'y':0.296159}, size_hint = (0.0705329, 0.039653))
        self.obj_widget3.add_widget(self.insert_pirate_button)
        self.insert_pirate_button.bind(on_press = self.insert_pirate)
        self.label53 = Label(text = "Delete", halign='left', pos_hint ={'x':0.648903, 'y':0.878563}, size_hint = (0.0705329, 0.039653))
        self.label53.bind(size=self.label53.setter('text_size'))
        self.obj_widget3.add_widget(self.label53)
        self.pirate_combo = Spinner(text = "", pos_hint ={'x':0.609718, 'y':0.804213}, size_hint = (0.125392, 0.039653))
        self.obj_widget3.add_widget(self.pirate_combo)
        self.delete_pirate_button = Button(text = "Delete", pos_hint ={'x':0.782132, 'y':0.804213}, size_hint = (0.0705329, 0.039653))
        self.obj_widget3.add_widget(self.delete_pirate_button)
        self.delete_pirate_button.bind(on_press = self.delete_pirate)
        self.obj.add_widget(self.pirate_tab)

    def build_marine_tab(self):
        self.marine_tab = TabbedPanelItem(text = "Marine")
        self.obj_widget4 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.marine_tab.add_widget(self.obj_widget4)
        self.label55 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0846395, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label55.bind(size=self.label55.setter('text_size'))
        self.obj_widget4.add_widget(self.label55)
        self.label56 = Label(text = "Person:", halign='left', pos_hint ={'x':0.0846395, 'y':0.828996}, size_hint = (0.0705329, 0.039653))
        self.label56.bind(size=self.label56.setter('text_size'))
        self.obj_widget4.add_widget(self.label56)
        self.label57 = Label(text = "Rank:", halign='left', pos_hint ={'x':0.0846395, 'y':0.754647}, size_hint = (0.0705329, 0.0272615))
        self.label57.bind(size=self.label57.setter('text_size'))
        self.obj_widget4.add_widget(self.label57)
        self.person_combo7 = Spinner(text = "", pos_hint ={'x':0.18652, 'y':0.816605}, size_hint = (0.101881, 0.039653))
        self.obj_widget4.add_widget(self.person_combo7)
        self.rank_combo = Spinner(text = "", 
                                values = ("", "Fleet Admiral", 
                                            "Admiral", 
                                            "Vice Admiral", 
                                            "Rear Admiral", 
                                            "Commodore", 
                                            "Captain", 
                                            "Commander", 
                                            "Lieutenant Commander", 
                                            "Lieutenant", 
                                            "Lieutenant Junior Grade", 
                                            "Ensign", 
                                            "Warrant Officer", 
                                            "Master Chief Petty Officer", 
                                            "Chief Petty Officer", 
                                            "Petty Officer", 
                                            "Seaman First Class", 
                                            "Seaman Apprentice", 
                                            "Seaman Recruit", 
                                            "Chore Boy", 
                                            "Base Commander", 
                                            "Inspector General", 
                                            "Instructor", 
                                            "Cook", 
                                            "Doctor", 
                                            "Scientist", 
                                            "Shipwright", 
                                            "Custodian"), 
                                pos_hint ={'x':0.18652, 'y':0.742255}, size_hint = (0.151881, 0.039653))
        self.obj_widget4.add_widget(self.rank_combo)
        self.label58 = Label(text = "Bounty:", halign='left', pos_hint ={'x':0.0846395, 'y':0.643123}, size_hint = (0.0705329, 0.039653))
        self.label58.bind(size=self.label58.setter('text_size'))
        self.obj_widget4.add_widget(self.label58)
        # self.label59 = Label(text = "Squad:", halign='left', pos_hint ={'x':0.0846395, 'y':0.531599}, size_hint = (0.0705329, 0.039653))
        # self.label59.bind(size=self.label59.setter('text_size'))
        # self.obj_widget4.add_widget(self.label59)
        self.label60 = Label(text = "Active:", halign='left', pos_hint ={'x':0.0846395, 'y':0.432466}, size_hint = (0.0705329, 0.039653))
        self.label60.bind(size=self.label60.setter('text_size'))
        self.obj_widget4.add_widget(self.label60)
        self.bounty_box2 = TextInput(text = "", multiline = False, pos_hint ={'x':0.18652, 'y':0.630731}, size_hint = (0.101881, 0.039653))
        self.obj_widget4.add_widget(self.bounty_box2)
        self.marine_active_combo = Spinner(text = "true", values = ("true", "false"), pos_hint ={'x':0.18652, 'y':0.420074}, size_hint = (0.101881, 0.039653))
        self.obj_widget4.add_widget(self.marine_active_combo)
        self.insert_marine_button = Button(text = "Insert", pos_hint ={'x':0.100313, 'y':0.30855}, size_hint = (0.0705329, 0.039653))
        self.obj_widget4.add_widget(self.insert_marine_button)
        self.insert_marine_button.bind(on_press = self.insert_marine)
        self.label61 = Label(text = "Delete", halign='left', pos_hint ={'x':0.617555, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label61.bind(size=self.label61.setter('text_size'))
        self.obj_widget4.add_widget(self.label61)
        self.marine_combo = Spinner(text = "", pos_hint ={'x':0.609718, 'y':0.828996}, size_hint = (0.101881, 0.039653))
        self.obj_widget4.add_widget(self.marine_combo)
        self.delete_marine_button = Button(text = "Delete", pos_hint ={'x':0.766458, 'y':0.828996}, size_hint = (0.0705329, 0.039653))
        self.obj_widget4.add_widget(self.delete_marine_button)
        self.delete_marine_button.bind(on_press = self.delete_marine)
        # self.group_combo3 = Spinner(text = "", pos_hint ={'x':0.18652, 'y':0.519207}, size_hint = (0.101881, 0.039653))
        # self.obj_widget4.add_widget(self.group_combo3)
        self.obj.add_widget(self.marine_tab)

    def build_island_tab(self):
        self.island_tab = TabbedPanelItem(text = "Island")
        self.obj_widget5 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.island_tab.add_widget(self.obj_widget5)
        self.label2 = Label(text = "INSERT", halign='left', pos_hint ={'x':0.0219436, 'y':0.903346}, size_hint = (0.133229, 0.0768278), font_family = "Comic Sans MS", font_size = "18")
        self.label2.bind(size=self.label2.setter('text_size'))
        self.obj_widget5.add_widget(self.label2)
        self.label2_copy = Label(text = "DELETE", halign='left', pos_hint ={'x':0.423197, 'y':0.910781}, size_hint = (0.133229, 0.0768278), font_family = "Comic Sans MS", font_size = "18")
        self.label2_copy.bind(size=self.label2_copy.setter('text_size'))
        self.obj_widget5.add_widget(self.label2_copy)
        self.island_name_textbox = TextInput(text = "", multiline = False, pos_hint ={'x':0.131661, 'y':0.853779}, size_hint = (0.101881, 0.039653))
        self.obj_widget5.add_widget(self.island_name_textbox)
        self.label3_copy = Label(text = "Region:", halign='left', pos_hint ={'x':0.0626959, 'y':0.786865}, size_hint = (0.0705329, 0.039653))
        self.label3_copy.bind(size=self.label3_copy.setter('text_size'))
        self.obj_widget5.add_widget(self.label3_copy)
        self.label3_copy_copy = Label(text = "Affiliation:", halign='left', pos_hint ={'x':0.0626959, 'y':0.700124}, size_hint = (0.0783699, 0.039653))
        self.label3_copy_copy.bind(size=self.label3_copy_copy.setter('text_size'))
        self.obj_widget5.add_widget(self.label3_copy_copy)
        self.ruler_label = Label(text = "Ruler:", halign='left', pos_hint ={'x':0.0470219, 'y':0.6}, size_hint = (0.0783699, 0.039653))
        self.obj_widget5.add_widget(self.ruler_label)
        self.territory_label = Label(text = "Territory:", halign='left', pos_hint ={'x':0.0470219, 'y':0.5}, size_hint = (0.0783699, 0.039653))
        self.obj_widget5.add_widget(self.territory_label)
        #self.region_textbox = TextInput(text = "", multiline = False, pos_hint ={'x':0.133229, 'y':0.786865}, size_hint = (0.101881, 0.039653))
        self.region_combo = Spinner(text = "", 
                          values = ('Calm Belt', 'East Blue', 'Grand Line', 'New World', 'North Blue', 'Paradise', 'Red Line', 'Sky', 'South Blue', 'Under the Sea', 'West Blue'), 
                          pos_hint ={'x':0.133229, 'y':0.786865}, 
                          size_hint = (0.101881, 0.039653)
                          )
        self.obj_widget5.add_widget(self.region_combo)

        self.person_combo10 = Spinner(text = "", pos_hint ={'x':0.131661, 'y':0.6}, size_hint = (0.101881, 0.039653))
        self.obj_widget5.add_widget(self.person_combo10)

        self.group_combo5 = Spinner(text = "", pos_hint ={'x':0.131661, 'y':0.5}, size_hint = (0.101881, 0.039653))
        self.obj_widget5.add_widget(self.group_combo5)

        self.insert_island_button = Button(text = "Insert", pos_hint ={'x':0.0376176, 'y':0.31834}, size_hint = (0.0783699, 0.039653))
        self.obj_widget5.add_widget(self.insert_island_button)
        self.insert_island_button.bind(on_press = self.insert_island)
        self.island_combo = Spinner(text = "", pos_hint ={'x':0.42163, 'y':0.841388}, size_hint = (0.117555, 0.0520446))
        self.obj_widget5.add_widget(self.island_combo)
        self.label3_copy_copy_copy = Label(text = "Name:", halign='left', pos_hint ={'x':0.0626959, 'y':0.848823}, size_hint = (0.0626959, 0.039653))
        self.label3_copy_copy_copy.bind(size=self.label3_copy_copy_copy.setter('text_size'))
        self.obj_widget5.add_widget(self.label3_copy_copy_copy)
        self.affiliation_combo = Spinner(text = "IND", values = ("IND", "WLG", "YNK"), pos_hint ={'x':0.131661, 'y':0.680297}, size_hint = (0.0862069, 0.0644362))
        self.obj_widget5.add_widget(self.affiliation_combo)
        self.delete_island_button = Button(text = "Delete", pos_hint ={'x':0.562696, 'y':0.841388}, size_hint = (0.0783699, 0.0520446))
        self.obj_widget5.add_widget(self.delete_island_button)
        self.delete_island_button.bind(on_press = self.delete_island)
        self.obj.add_widget(self.island_tab)

    def build_group_tab(self):
        self.group_tab = TabbedPanelItem(text = "Group")
        self.obj_widget6 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.group_tab.add_widget(self.obj_widget6)
        self.label33 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0611285, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label33.bind(size=self.label33.setter('text_size'))
        self.obj_widget6.add_widget(self.label33)
        self.label34 = Label(text = "Name:", halign='left', pos_hint ={'x':0.0611285, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.label34.bind(size=self.label34.setter('text_size'))
        self.obj_widget6.add_widget(self.label34)
        self.label35 = Label(text = "Base:", halign='left', pos_hint ={'x':0.0611285, 'y':0.742255}, size_hint = (0.0705329, 0.039653))
        self.label35.bind(size=self.label35.setter('text_size'))
        self.obj_widget6.add_widget(self.label35)
        self.label37 = Label(text = "Leader:", halign='left', pos_hint ={'x':0.0611285, 'y':0.643123}, size_hint = (0.0705329, 0.039653))
        self.label37.bind(size=self.label37.setter('text_size'))
        self.obj_widget6.add_widget(self.label37)
        self.insert_group_button = Button(text = "Insert", pos_hint ={'x':0.0924765, 'y':0.506815}, size_hint = (0.0705329, 0.039653))
        self.obj_widget6.add_widget(self.insert_group_button)
        self.insert_group_button.bind(on_press = self.insert_group)
        self.group_name_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.147335, 'y':0.804213}, size_hint = (0.117555, 0.039653))
        self.obj_widget6.add_widget(self.group_name_box)
        self.island_combo3 = Spinner(text = "", pos_hint ={'x':0.147335, 'y':0.729864}, size_hint = (0.117555, 0.039653))
        self.obj_widget6.add_widget(self.island_combo3)
        self.person_combo4 = Spinner(text = "", pos_hint ={'x':0.147335, 'y':0.630731}, size_hint = (0.117555, 0.039653))
        self.obj_widget6.add_widget(self.person_combo4)
        self.group_combo = Spinner(text = "", pos_hint ={'x':0.641066, 'y':0.853779}, size_hint = (0.148903, 0.039653))
        self.obj_widget6.add_widget(self.group_combo)
        self.delete_group_button = Button(text = "Delete", pos_hint ={'x':0.829154, 'y':0.853779}, size_hint = (0.0783699, 0.039653))
        self.obj_widget6.add_widget(self.delete_group_button)
        self.disband_group_button = Button(text = "Defeat/Disband", pos_hint ={'x':0.829154, 'y':0.753779}, size_hint = (0.0783699, 0.039653))
        self.obj_widget6.add_widget(self.disband_group_button)
        self.disband_group_button.bind(on_press=self.disband_group)
        self.delete_group_button.bind(on_press = self.delete_group)
        self.label47 = Label(text = "Delete", halign='left', pos_hint ={'x':0.664577, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label47.bind(size=self.label47.setter('text_size'))
        self.obj_widget6.add_widget(self.label47)

        self.label00 = Label(text="Image:", halign='left', pos_hint={'x': 0.0376176, 'y': 0.172}, size_hint=(0.0705329, 0.039653))
        self.label00.bind(size=self.label00.setter('text_size'))
        self.obj_widget6.add_widget(self.label00)
        self.upload_status_group = Label(text="No file selected", pos_hint={'x': 0.10815, 'y': 0.172}, size_hint=(0.0705329, 0.039653))
        self.obj_widget6.add_widget(self.upload_status_group)
        self.upload_group_button = Button(text="Upload", pos_hint={'x': 0.2, 'y': 0.172}, size_hint=(0.1, 0.039653))
        self.obj_widget6.add_widget(self.upload_group_button)
        self.upload_group_button.bind(on_press=self.upload_group_image)

        self.obj.add_widget(self.group_tab)

    def build_membership_tab(self):
        self.membership_tab = TabbedPanelItem(text = "Membership")
        self.obj_widget12 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.membership_tab.add_widget(self.obj_widget12)

        self.label80 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0532915, 'y':0.915737}, size_hint = (0.0705329, 0.039653))
        self.label80.bind(size=self.label80.setter('text_size'))
        self.obj_widget12.add_widget(self.label80)

        self.label81 = Label(text = "Choose person:", halign='left', pos_hint ={'x':0.0532915, 'y':0.85}, size_hint = (0.0705329, 0.039653))
        self.label81.bind(size=self.label81.setter('text_size'))
        self.obj_widget12.add_widget(self.label81)

        self.label82 = Label(text = "Choose group:", halign='left', pos_hint ={'x':0.0532915, 'y':0.81}, size_hint = (0.0705329, 0.039653))
        self.label82.bind(size=self.label82.setter('text_size'))
        self.obj_widget12.add_widget(self.label82)

        self.insert_membership_button = Button(text = "Insert", pos_hint ={'x':0.1, 'y':0.7}, size_hint = (0.0783699, 0.039653))
        self.insert_membership_button.bind(on_press = self.insert_membership)
        self.obj_widget12.add_widget(self.insert_membership_button)

        self.person_combo11 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.85}, size_hint = (0.22, 0.039653))
        self.obj_widget12.add_widget(self.person_combo11)

        self.group_combo8 = Spinner(text = "", pos_hint ={'x':0.15, 'y':0.81}, size_hint = (0.22, 0.039653))
        self.obj_widget12.add_widget(self.group_combo8)

        self.label83 = Label(text = "Delete", halign='left', pos_hint ={'x':0.617555, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label83.bind(size=self.label83.setter('text_size'))
        self.obj_widget12.add_widget(self.label83)

        self.delete_membership_button = Button(text = "Delete", pos_hint ={'x':0.85, 'y':0.816605}, size_hint = (0.0705329, 0.039653))
        self.obj_widget12.add_widget(self.delete_membership_button)
        self.delete_membership_button.bind(on_press = self.delete_membership)
        
        self.membership_combo = Spinner(text = "", pos_hint ={'x':0.617555, 'y':0.816605}, size_hint = (0.22, 0.039653))
        self.obj_widget12.add_widget(self.membership_combo)

        self.obj.add_widget(self.membership_tab)

    def build_vessel_tab(self):
        self.vessel_tab = TabbedPanelItem(text = "Vessel")
        self.obj_widget7 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.vessel_tab.add_widget(self.obj_widget7)
        self.label38 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0768025, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label38.bind(size=self.label38.setter('text_size'))
        self.obj_widget7.add_widget(self.label38)
        self.vessel_name_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.178683, 'y':0.742255}, size_hint = (0.117555, 0.039653))
        self.obj_widget7.add_widget(self.vessel_name_box)
        self.label39 = Label(text = "Name:", halign='left', pos_hint ={'x':0.0768025, 'y':0.742255}, size_hint = (0.0705329, 0.039653))
        self.label39.bind(size=self.label39.setter('text_size'))
        self.obj_widget7.add_widget(self.label39)
        self.label40 = Label(text = "Size:", halign='left', pos_hint ={'x':0.0768025, 'y':0.643123}, size_hint = (0.0705329, 0.039653))
        self.label40.bind(size=self.label40.setter('text_size'))
        self.obj_widget7.add_widget(self.label40)
        self.vessel_size_slider = Slider(min = 5, max = 1000, value = 5, step = 5, orientation = "horizontal", pos_hint ={'x':0.178683, 'y':0.630731}, size_hint = (0.117555, 0.0520446))
        self.obj_widget7.add_widget(self.vessel_size_slider)
        self.insert_vessel_button = Button(text = "Insert", pos_hint ={'x':0.115987, 'y':0.36}, size_hint = (0.0705329, 0.039653))
        self.obj_widget7.add_widget(self.insert_vessel_button)
        self.insert_vessel_button.bind(on_press = self.insert_vessel)
        self.label41 = Label(text = "Delete", halign='left', pos_hint ={'x':0.648903, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label41.bind(size=self.label41.setter('text_size'))
        self.obj_widget7.add_widget(self.label41)
        self.vessel_combo = Spinner(text = "", pos_hint ={'x':0.641066, 'y':0.804213}, size_hint = (0.125392, 0.039653))
        self.obj_widget7.add_widget(self.vessel_combo)
        self.delete_vessel_button = Button(text = "Delete", pos_hint ={'x':0.81348, 'y':0.804213}, size_hint = (0.0705329, 0.039653))
        self.obj_widget7.add_widget(self.delete_vessel_button)
        self.delete_vessel_button.bind(on_press = self.delete_vessel)
        self.label63 = Label(text = "Owner:", halign='left', pos_hint ={'x':0.0768025, 'y':0.556382}, size_hint = (0.0705329, 0.039653))
        self.label63.bind(size=self.label63.setter('text_size'))
        self.obj_widget7.add_widget(self.label63)
        self.group_combo4 = Spinner(text = "", pos_hint ={'x':0.178683, 'y':0.54399}, size_hint = (0.117555, 0.039653))
        self.obj_widget7.add_widget(self.group_combo4)

        self.label62 = Label(text = "Shipwright:", halign='left', pos_hint ={'x':0.0768025, 'y':0.44399}, size_hint = (0.0705329, 0.039653))
        self.label62.bind(size=self.label62.setter('text_size'))
        self.obj_widget7.add_widget(self.label62)
        self.person_combo12 = Spinner(text = "", pos_hint ={'x':0.178683, 'y':0.44399}, size_hint = (0.117555, 0.039653))
        self.obj_widget7.add_widget(self.person_combo12)

        self.obj.add_widget(self.vessel_tab)

    def build_artifact_tab(self):
        self.artifact_tab = TabbedPanelItem(text = "Artifact")
        self.obj_widget8 = RelativeLayout(pos_hint ={'x':0, 'y':0}, size_hint = (1, 1))
        self.artifact_tab.add_widget(self.obj_widget8)
        self.label42 = Label(text = "Insert", halign='left', pos_hint ={'x':0.0611285, 'y':0.890954}, size_hint = (0.0705329, 0.039653))
        self.label42.bind(size=self.label42.setter('text_size'))
        self.obj_widget8.add_widget(self.label42)
        self.label43 = Label(text = "Object:", halign='left', pos_hint ={'x':0.0611285, 'y':0.804213}, size_hint = (0.0470219, 0.039653))
        self.label43.bind(size=self.label43.setter('text_size'))
        self.obj_widget8.add_widget(self.label43)
        self.artifact_name_box = TextInput(text = "", multiline = False, pos_hint ={'x':0.155172, 'y':0.804213}, size_hint = (0.133229, 0.039653))
        self.obj_widget8.add_widget(self.artifact_name_box)
        self.label44 = Label(text = "Location:", halign='left', pos_hint ={'x':0.0611285, 'y':0.729864}, size_hint = (0.0705329, 0.039653))
        self.label44.bind(size=self.label44.setter('text_size'))
        self.obj_widget8.add_widget(self.label44)
        self.island_combo5 = Spinner(text = "", pos_hint ={'x':0.155172, 'y':0.717472}, size_hint = (0.133229, 0.039653))
        self.obj_widget8.add_widget(self.island_combo5)
        self.label45 = Label(text = "Owner:", halign='left', pos_hint ={'x':0.0611285, 'y':0.61834}, size_hint = (0.0705329, 0.039653))
        self.label45.bind(size=self.label45.setter('text_size'))
        self.obj_widget8.add_widget(self.label45)
        self.person_combo5 = Spinner(text = "", pos_hint ={'x':0.155172, 'y':0.61834}, size_hint = (0.133229, 0.039653))
        self.obj_widget8.add_widget(self.person_combo5)
        self.insert_artifact_button = Button(text = "Insert", pos_hint ={'x':0.100313, 'y':0.506815}, size_hint = (0.0705329, 0.039653))
        self.obj_widget8.add_widget(self.insert_artifact_button)
        self.insert_artifact_button.bind(on_press = self.insert_artifact)
        self.artifact_combo = Spinner(text = "", pos_hint ={'x':0.664577, 'y':0.841388}, size_hint = (0.125392, 0.039653))
        self.obj_widget8.add_widget(self.artifact_combo)
        self.delete_artifact_button = Button(text = "Delete", pos_hint ={'x':0.829154, 'y':0.841388}, size_hint = (0.0705329, 0.039653))
        self.obj_widget8.add_widget(self.delete_artifact_button)
        self.delete_artifact_button.bind(on_press = self.delete_artifact)
        self.label46 = Label(text = "Delete", halign='left', pos_hint ={'x':0.680251, 'y':0.903346}, size_hint = (0.0705329, 0.039653))
        self.label46.bind(size=self.label46.setter('text_size'))
        self.obj_widget8.add_widget(self.label46)
        self.obj.add_widget(self.artifact_tab)
        self.tab1.add_widget(self.tab1_tab0)


    def update_df(self, instance):
        df = self.df_combo3.text.strip()
        description = self.df_description.text.strip()
        image = None
        if self.df_image:
            try:
                with open(self.df_image, 'rb') as pic:
                    image = pic.read()
            except Exception as error:
                print(error)
        
        query = "UPDATE op.devil_fruit SET "
        lst = []

        if image:
            lst.append(f"image=%s")
        if description:
            lst.append(f"description='{description}'")
        
        query += ", ".join(lst)
        if df:
            query += f" WHERE df_name='{df}';"

        try:
            cur.execute(query, (image,))
            self.df_combo3.text = ""
        except psycopg2.Error as error:
            print(error)

    def update_person(self, widget):
        person = self.person_combo13.text.split(',')[0].strip()
        id = int(person) if person.isnumeric() else "Null"

        last_seen = self.island_combo6.text
        image = None
        if self.person_image:
            try:
                with open(self.person_image, 'rb') as pic:
                    image = pic.read()  
            except Exception as error:
                print(error)

        description = self.person_description.text

        query = "UPDATE op.person SET "
        lst = []

        if last_seen:
            lst.append(f"last_seen='{last_seen}'")
        if image:
            lst.append(f"image=%s")
        if description:
            lst.append(f"description='{description}'")
        
        query += ", ".join(lst)
        if id:
            query += f" WHERE id={id};"

        try:
            #print(image)
            cur.execute(query, (image,))
        
        except psycopg2.Error as error:
            print(error)

    #https://stackoverflow.com/questions/50123315/how-do-i-create-an-import-file-button-with-tkinter 
    def upload_image(self, instance):
        root = Tk()
        root.withdraw() 
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            file = path.split("/")[-1]  
            self.upload_status_label.text = f"Uploaded {file}"
            self.file = path  
        else:
            self.file = None
            self.upload_status_label.text = "Choose a pic lil bro"

    def upload_person_image(self, instance):
        root = Tk()
        root.withdraw() 
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            file = path.split("/")[-1]  
            self.upload_status_label3.text = f"Uploaded {file}"
            self.person_image = path  
        else:
            self.person_image = None
            self.upload_status_label3.text = "Choose a pic lil bro"

    def upload_df_image(self, instance):
        root = Tk()
        root.withdraw() 
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            file = path.split("/")[-1]  
            self.upload_status_label_df.text = f"Uploaded {file}"
            self.df_image = path  
        else:
            self.df_image = None
            self.upload_status_label_df.text = "Choose a pic lil bro"

    def upload_group_image(self, instance):
        root = Tk()
        root.withdraw() 
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            file = path.split("/")[-1]  
            self.upload_status_group.text = f"Uploaded {file}"
            self.group_image = path  
        else:
            self.group_image = None
            self.upload_status_group.text = "Choose a pic lil bro"

    def insert_island(self, widget):
        name = self.island_name_textbox.text.strip()
        region = self.region_combo.text.strip()
        affiliation = self.affiliation_combo.text.strip()
        ruler = self.person_combo10.text.split(',')[0].strip()

        territory = self.group_combo5.text.strip()
        if territory:
            start = territory.find(')') + 1
            territory = "'"+territory[start:].strip()+"'"
        else:
            territory = "Null"
        
        name_value = f"'{name}'" if name else "Null"
        region_value = f"'{region}'" if region else "Null"
        affiliation_value = f"'{affiliation}'" if affiliation else "Null"
        ruler_value = int(ruler) if ruler.isnumeric() else "Null"
        #territory_value = f"'{territory}'" if territory else "Null"
        
        query = f"""
            INSERT INTO op.island(
            island_name, region, affiliation, ruler, territory)
            VALUES ({name_value}, {region_value}, {affiliation_value}, {ruler_value}, {territory});
        """
        try:
            cur.execute(query)
            conn.commit()
            self.buildIslandCombo()
            self.island_name_textbox.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_island(self, widget):
        name = self.island_combo.text.strip()
        query = f"""
            DELETE FROM op.island
            WHERE island_name='{name}';
        """
        cur.execute(query)
        conn.commit()
        self.buildIslandCombo()
        self.island_combo.text = ""

    def insert_person(self, widget):
        fname = self.fname_box.text.strip()
        mname = self.mname_box.text.strip()
        lname = self.lname_box.text.strip()
        age = self.age_box.text.strip()
        gender = self.gender_box.text.strip()
        race = self.race_box.text.strip()
        hometown = self.island_combo2.text.strip()
        birthday = self.birthday_box.text.strip()
        height = self.height_box.text.strip()
        job = self.job_box.text.strip()
        description = self.description_box.text.strip()

        mname_val = f"'{mname}'" if mname else "''"
        lname_val = f"'{lname}'" if lname else "''"
        age_val = int(age) if age.isnumeric() else "Null"
        height_val = int(height) if height.isnumeric() else "Null"
        gender_val = f"'{gender}'" if gender else "Null"
        race_val = f"'{race}'" if race else "Null"
        hometown_val = f"'{hometown}'" if hometown else "Null"
        job_val = f"'{job}'" if job else "Null"
        description_val = f"'{description}'" if description else "Null"

        if not (valid_date(birthday)):
            birthday = "Null"
        else:
            birthday = f"'{birthday}'"

        image = None
        if self.file:
            try:
                with open(self.file, 'rb') as pic:
                    image = pic.read()  
            except Exception as error:
                print(error)

        query = f"""
            INSERT INTO op.person(fname, mname, lname, age, gender, race, hometown, birthday, height, status, job, image, description)
            VALUES ('{fname}', {mname_val}, {lname_val}, {age_val}, {gender_val}, {race_val}, {hometown_val}, {birthday}, {height_val}, 'A', {job_val}, %s, {description_val});
        """

        # query = """
        #     INSERT INTO op.person(fname, mname, lname, age, gender, race, hometown, birthday, height, status, job, image, description)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s, %s, %s);
        # """
        try:
            cur.execute(query, (image,))
            conn.commit()
            self.buildPersonCombo()
            self.error_label.text = ''
            self.fname_box.text = ''
            self.mname_box.text = ''
            self.lname_box.text = ''
            self.age_box.text = ''
            self.gender_box.text = ''
            self.race_box.text = ''
            self.island_combo2.text = ''
            self.birthday_box.text = ''
            self.height_box.text = ''
            self.job_box.text = ''
            self.description_box.text = ''  
        except psycopg2.Error as error:
            self.error_label.text = str(error)

    def delete_person(self, widget):
        id = self.person_combo.text.split(',')[0].strip()       
        id_val = int(id) if id.isnumeric() else "Null"
        query = f"""
            DELETE FROM op.person
            WHERE id={id_val};
        """
        try:
            cur.execute(query)
            conn.commit()
            self.buildPersonCombo()
            self.person_combo.text = ""
        except psycopg2.Error as error:
            print(error)

    def kill_person(self, widget):
        text = self.person_combo.text.strip()
        if not text:
            return

        id = self.person_combo.text.split(',')[0].strip()       
        id_val = int(id) if id.isnumeric() else "Null"

        query = f"""
            BEGIN;

            UPDATE op.person
            SET status='D'
            WHERE id={id_val};

            UPDATE op.artifact
            SET owner=Null
            WHERE owner={id_val};

            UPDATE op.groups
            SET leader_id=Null
            WHERE leader_id={id_val};

            COMMIT;
        """

        try:
            cur.execute(query)
            conn.commit()
            self.person_combo.text = ''
        except psycopg2.Error as error:
            print(error)

    def insert_df(self, widget):
        df_name = self.df_name_box.text.strip()
        type = self.df_type_combo.text.strip()
        awakened = self.awakened_combo.text.strip()
        description = self.description_box2.text.strip()
        
        image = None
        try:
            with open(self.df_image, 'rb') as pic:
                image = pic.read()  
        except Exception as error:
            print(error)


        name_val = f"'{df_name}'" if df_name else "Null"
        type_val = f"'{type}'" if type else "Null"
        description_val = f"'{description}'" if description else "Null"


        query = f"""
            INSERT INTO op.devil_fruit(
            df_name, type, awakened, image, description)
            VALUES ({name_val}, {type_val}, {awakened}, %s, {description_val});
        """

        try:
            cur.execute(query, (image,))
            conn.commit()
            self.buildDevilFruitCombo()
            self.df_name_box.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_df(self, widget):
        name = self.df_combo.text.strip()
        
        query = f"""
            DELETE FROM op.devil_fruit
            WHERE df_name='{name}';
        """
        cur.execute(query)
        conn.commit()
        self.buildDevilFruitCombo()
        self.df_combo.text = ""

    def insert_df_eater(self, widget):
        eater = self.person_combo8.text.split(',')[0].strip()
        df = self.df_combo2.text.strip()

        df_val = f"'{df}'" if df else "Null"
        eater_val = int(eater) if eater.isnumeric() else "Null"

        query = f"""
            INSERT INTO op.devil_fruit_eater(
            df_name, eater)
            VALUES ({df_val}, {eater_val});
        """
        
        try:
            cur.execute(query)
            conn.commit()
            self.buildDfEaterCombo()
            self.person_combo8.text = ''
            self.df_combo2.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_df_eater(self, widget):
        text = self.df_eater_combo.text.strip()
        if not text:
            return

        start = text.find('(') + 1 
        end = text.find(')')  
        id = int(text[start:end])  

        df = "'"+text.split(',')[1].strip()+"'"

        query = f"""
            DELETE FROM op.devil_fruit_eater
            WHERE df_name={df} and eater={id};
        """

        try:
            cur.execute(query)
            conn.commit()
            self.buildDfEaterCombo()
            self.df_eater_combo.text = ''
        except psycopg2.Error as error:
            print(error)

    def insert_pirate(self, widget):
        id = self.person_combo6.text 
        id_value = int(id.split(',')[0].strip()) if id else "Null"

        role = self.role_combo.text.strip()
        role_value = f"'{role}'" if role else "Null"
        #crew = self.group_combo2.text.strip()
        #crew_value = f"'{crew}'" if crew else "Null"
        bounty = self.pirate_bounty_box.text.strip()
        bounty_value = int(bounty) if bounty.isnumeric() else "Null"
        active = self.pirate_active_combo.text.strip()

        query = f"""
        INSERT INTO op.pirate(id, role, bounty, active)
        VALUES ({id_value}, {role_value}, {bounty_value}, '{active}');
        """

        try:
            cur.execute(query)
            conn.commit()
            self.buildPirateCombo()
            self.person_combo6.text = ''
            self.pirate_bounty_box.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_pirate(self, widget):
        
        id = self.pirate_combo.text 
        id_value = int(id.split(',')[0].strip()) if id else "Null"
        
        query = f"""
            DELETE FROM op.pirate
            WHERE id={id_value};
        """
        try:
            cur.execute(query)
            conn.commit()
            self.pirate_combo.text = ""
            self.buildPirateCombo()
        except psycopg2.Error as error:
            print(error)

    def insert_marine(self, widget):
        id = self.person_combo7.text 
        id_value = int(id.split(',')[0].strip()) if id else "Null"

        rank = self.rank_combo.text.strip()
        rank_value = f"'{rank}'" if rank else "Null"
        # squad = self.group_combo3.text.strip()
        # squad_value = f"'{squad}'" if squad else "Null"
        bounty = self.bounty_box2.text.strip()
        bounty_value = int(bounty) if bounty.isnumeric() else "Null"
        active = self.marine_active_combo.text.strip()

        query = f"""
        INSERT INTO op.marine(id, rank, bounty, active)
        VALUES ({id_value}, {rank_value}, {bounty_value}, '{active}');
        """

        try:
            cur.execute(query)
            conn.commit()
            self.buildMarineCombo()
            self.person_combo7.text = ''
            self.bounty_box2.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_marine(self, widget):
        id = self.marine_combo.text 
        id_value = int(id.split(',')[0].strip()) if id else "Null"
        
        query = f"""
            DELETE FROM op.marine
            WHERE id={id_value};
        """
        try:
            cur.execute(query)
            conn.commit()
            self.marine_combo.text = ""
            self.buildMarineCombo()
        except psycopg2.Error as error:
            print(error)

    def insert_group(self, widget):
        name = self.group_name_box.text.strip()
        base = self.island_combo3.text.strip()

        id = self.person_combo4.text 
        leader_id = int(id.split(',')[0].strip()) if id else "Null"

        base_value = f"'{base}'" if base else "Null"

        image = None
        if self.group_image:
            try:
                with open(self.group_image, 'rb') as pic:
                    image = pic.read()  
            except Exception as error:
                print(error)

        query = f"""
        INSERT INTO op.groups(group_name, base, leader_id, image)
	    VALUES ('{name}', {base_value}, {leader_id}, %s);
        """

        try:
            cur.execute(query, (image,))
            conn.commit()
            self.buildGroupCombo()
            self.group_name_box.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_group(self, widget):
        text = self.group_combo.text.strip()
        if not text:
            return

        start = text.find('(') + 1 
        end = text.find(')')  
        id = int(text[start:end])  
        try:
            cur.execute(f"DELETE FROM op.groups WHERE group_id='{id}';")
            conn.commit()
            self.buildGroupCombo()
            self.group_combo.text = ''
        except psycopg2.Error as error:
            print(error)

    def disband_group(self, widget):
        text = self.group_combo.text.strip()
        if not text:
            return

        start = text.find('(') + 1 
        end = text.find(')')  
        id = int(text[start:end])  
        name = text[end+2:]


        query = f"""
            BEGIN;

            UPDATE op.island
            SET territory=Null
            WHERE territory='{name}';

            UPDATE op.artifact
            SET owner=Null
            WHERE owner IN (
                SELECT person_id
                FROM op.membership
                WHERE group_id={id}
            );

            DELETE 
            FROM op.vessel
            WHERE owner={id};

            COMMIT;
        """

        try:
            cur.execute(query)
            conn.commit()
            self.group_combo.text = ''
        except psycopg2.Error as error:
            print(error)
        
    def insert_membership(self, widget):
        person = self.person_combo11.text.split(',')[0].strip()
        person_id = int(person) if person.isnumeric() else "Null"

        text = self.group_combo8.text.strip()
        if not text:
            return
        start = text.find('(') + 1 
        end = text.find(')')  
        group_id = int(text[start:end])  

        
        query = f"""
            INSERT INTO op.membership(
            person_id, group_id)
            VALUES ({person_id}, {group_id});
        """
        
        try:
            cur.execute(query)
            conn.commit()
            self.buildMembershipCombo()
            self.group_combo8.text = ''
            self.person_combo11.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_membership(self, widget):
        text = self.membership_combo.text.strip()
        if not text:
            return
        
        pair = text.split(',')

        start = pair[0].find('(') + 1 
        end = pair[0].find(')')  
        person_id = int(pair[0][start:end])  

        start = pair[1].find('(') + 1 
        end = pair[1].find(')')  
        group_id = int(pair[1][start:end])  

        query = f"""
            DELETE FROM op.membership
            WHERE person_id={person_id} and group_id={group_id};
        """

        try:
            cur.execute(query)
            conn.commit()
            self.buildMembershipCombo()
            self.membership_combo.text = ''
        except psycopg2.Error as error:
            print(error)

    def insert_vessel(self, widget):
        name = self.vessel_name_box.text.strip()
        size = self.vessel_size_slider.value

        text = self.group_combo4.text.strip()
        
        try:
            start = text.find('(') + 1 
            end = text.find(')')  
            group_id = int(text[start:end]) 
        except:
            group_id = "Null"

        name_val = f"'{name}'" if name else "Null"

        shipwright = self.person_combo12.text.split(',')[0].strip()
        shipwright_id = int(shipwright) if shipwright.isnumeric() else "Null"

        query = f"""
        INSERT INTO op.vessel(vessel_name, size, owner, shipwright)
	    VALUES ({name_val}, {size}, {group_id}, {shipwright_id});
        """
        try:
            cur.execute(query)
            conn.commit()
            self.vessel_name_box.text = ''
            self.buildVesselCombo()
        except psycopg2.Error as error:
            print(error)
        
    def delete_vessel(self, widget):
        text = self.vessel_combo.text.strip()
        if not text:
            return
        start = text.find('(') + 1 
        end = text.find(')')  
        vessel_id = int(text[start:end])  

        try:
            cur.execute(f"DELETE FROM op.vessel WHERE vessel_id='{vessel_id}';")
            conn.commit()
            self.vessel_combo.text = ''
            self.buildVesselCombo()
        except psycopg2.Error as error:
            print(error)

    def insert_artifact(self, widget):
        object = self.artifact_name_box.text.strip()
        location = self.island_combo5.text.strip()
        owner = self.person_combo5.text

        owner_id = int(owner.split(',')[0].strip()) if owner else "Null"
        object_value = f"'{object}'" if object else "Null"
        location_value = f"'{location}'" if location else "Null"

        
        
        query = f"""
        INSERT INTO op.artifact(object, location, owner)
	    VALUES ({object_value}, {location_value}, {owner_id});
        """

        try:
            cur.execute(query)
            conn.commit()
            self.artifact_name_box.text = ''
            self.buildArtifactCombo()
        except psycopg2.Error as error:
            print(error)

    def delete_artifact(self, widget):
        id = self.artifact_combo.text 
        id_value = int(id.split(',')[0].strip()) if id else "Null"
        
        query = f"""
            DELETE FROM op.artifact
            WHERE artifact_id={id_value};
        """
        try:
            cur.execute(query)
            conn.commit()
            self.artifact_combo.text = ""
            self.buildArtifactCombo()
        except psycopg2.Error as error:
            print(error)

    def insert_sword(self, widget):
        sword_name = self.sword_name_box.text.strip()
        type = self.sword_type_combo.text.strip()
        grade = self.sword_grade_combo.text.strip() 
        classification = self.sword_class_combo.text.strip() 
        
        #owner = self.person_combo3.text.split(',')[0].strip()
        
        name_val = f"'{sword_name}'" if sword_name else "Null"
        type_val = f"'{type}'" if type else "Null"
        grade_val = f"'{grade}'" if grade else "Null"
        class_val = f"'{classification}'" if classification else "Null"
        #owner_id = int(id.split(',')[0].strip()) if owner else "Null"

        query = f"""
            INSERT INTO op.sword(sword_name, type, classification, grade)
	        VALUES ({name_val}, {type_val}, {class_val}, {grade_val});
        """
        
        try:
            cur.execute(query)
            conn.commit()
            self.buildSwordCombo()
            self.sword_name_box.text = ''
        except psycopg2.Error as error:
            print(error)

    def delete_sword(self, widget):
        id = self.sword_combo.text.split(',')[0].strip()
        sword_id = int(id) if id.isnumeric() else "Null"

        query = f"""
            DELETE FROM op.sword
            WHERE sword_id={sword_id};
        """
        cur.execute(query)
        conn.commit()
        self.buildSwordCombo()
        self.sword_combo.text = ""
            
    def insert_swordsman(self, widget):
        swordsman = self.person_combo9.text.split(',')[0].strip()
        sword = self.sword_combo2.text.split(',')[0].strip()

        sword_val = int(sword) if sword.isnumeric() else "Null"
        swordsman_val = int(swordsman) if swordsman.isnumeric() else "Null"

        query = f"""
            INSERT INTO op.swordsman(
            swordsman, sword)
            VALUES ({swordsman_val}, {sword_val});
        """
        
        try:
            cur.execute(query)
            conn.commit()
            self.buildSwordsmanCombo()
            self.person_combo9.text = ''
            self.sword_combo2.text = ''
        except psycopg2.Error as error:
            print(error)
    
    def delete_swordsman(self, widget):
        text = self.swordsman_combo.text.strip()
        if not text:
            return
        
        pair = text.split(',')

        start = pair[0].find('(') + 1 
        end = pair[0].find(')')  
        swordsman_id = int(pair[0][start:end])  

        start = pair[1].find('(') + 1 
        end = pair[1].find(')')  
        sword_id = int(pair[1][start:end])  

        query = f"""
            DELETE FROM op.swordsman
            WHERE swordsman={swordsman_id} and sword={sword_id};
        """

        try:
            cur.execute(query)
            conn.commit()
            self.buildSwordsmanCombo()
            self.swordsman_combo.text = ''
        except psycopg2.Error as error:
            print(error)

    def buildSwordCombo(self):
        lst = []
        cur.execute("SELECT sword_id, sword_name FROM op.sword ORDER BY sword_name ASC;")
        for row in cur:
            lst.append(str(row[0])+', '+row[1])
        self.sword_combo.values = lst
        self.sword_combo2.values = lst
        self.sword_combo2.text = lst[0]

    def buildSwordsmanCombo(self):
        lst = []
        cur.execute("""
            SELECT swordsman, fname, sword_id, sword_name
            FROM op.swordsman 
            JOIN op.person ON swordsman=id
            JOIN op.sword ON sword=sword_id
            ORDER BY fname ASC;
        """)
        #row[0] = 7 (swordsman_id)
        #row[1] = Zoro
        #row[2] = 30 (sword_id)
        #row[3] = Enma
        for row in cur:
            lst.append('('+str(row[0])+') '+row[1]+', ('+str(row[2])+') '+row[3])
        self.swordsman_combo.values = lst
        
    def buildDevilFruitCombo(self):
        lst = []
        cur.execute("SELECT * FROM op.devil_fruit ORDER BY df_name ASC;")
        for row in cur:
            lst.append(row[0])
        self.df_combo.values = lst
        self.df_combo2.values = lst
        self.df_combo2.text = lst[0]
        self.df_combo3.values = lst

        self.report_df_widget.buildDFCombo()

    def buildDfEaterCombo(self):
        lst = []
        cur.execute("""
            SELECT df_name, eater, fname
            FROM op.devil_fruit_eater 
            JOIN op.person ON eater=id
            ORDER BY df_name ASC;
        """)
        for row in cur:
            lst.append('('+str(row[1])+') '+str(row[2])+', '+row[0])
        self.df_eater_combo.values = lst

    def buildIslandCombo(self):
        lst = []
        cur.execute("SELECT * FROM op.island ORDER BY island_name ASC;")
        for row in cur:
            lst.append(row[0])
        self.island_combo.values = lst
        self.island_combo2.values = lst
        self.island_combo3.values = [''] + lst
        self.island_combo5.values = [''] + lst
        self.island_combo6.values = lst

    def buildPersonCombo(self):
        lst = []
        cur.execute("SELECT id, fname from op.person ORDER BY fname ASC;")
        for row in cur:
            lst.append(str(row[0])+', '+row[1])
        self.person_combo.values = lst
        #self.person_combo2.values = [''] + lst
        #self.person_combo3.values = [''] + lst
        self.person_combo4.values = [''] + lst
        self.person_combo5.values = [''] + lst
        self.person_combo6.values = [''] + lst
        self.person_combo7.values = [''] + lst
        self.person_combo8.values = lst
        self.person_combo8.text = lst[0]
        self.person_combo9.values = lst
        self.person_combo9.text = lst[0]
        self.person_combo10.values = [''] + lst
        self.person_combo11.values = lst
        self.person_combo12.values = [''] + lst
        self.person_combo13.values = lst
        self.report_widget.buildPersonCombo()
        self.table_widget.buildPersonTable()
        
    def buildVesselCombo(self):
        lst = []
        cur.execute("SELECT vessel_id, vessel_name from op.vessel ORDER BY vessel_name ASC;")
        for row in cur:
            lst.append(f'({row[0]}) '+row[1])
        self.vessel_combo.values = lst

    def buildGroupCombo(self):
        lst = []
        cur.execute("SELECT group_id, group_name from op.groups ORDER BY group_name ASC;")
        for row in cur:
            lst.append(f'({row[0]}) '+row[1])
        self.group_combo.values = lst
        #self.group_combo2.values = lst
        #self.group_combo3.values = lst
        self.group_combo4.values = lst
        self.group_combo4.values = [''] + lst
        self.group_combo5.values = lst
        self.group_combo5.values = [''] + lst
        self.group_combo8.values = lst

        self.report_group_widget.buildGroupCombo()
    
    def buildMembershipCombo(self):
        lst = []
        cur.execute("""
            SELECT P.id, P.fname, G.group_id, G.group_name
            FROM op.membership as M 
            JOIN op.person as P ON M.person_id=P.id
            JOIN op.groups as G ON M.group_id=G.group_id
            ORDER BY G.group_name, P.fname ASC;
        """)

        for row in cur:
            lst.append('('+str(row[0])+') '+str(row[1])+', ('+str(row[2])+") "+row[3])
        self.membership_combo.values = lst

    def buildPirateCombo(self):
        lst = []
        cur.execute("""
        SELECT per.id, per.fname
        FROM op.person as per 
        JOIN op.pirate as pir ON per.id=pir.id;
        """)
        for row in cur:
            lst.append(str(row[0])+', '+row[1])
        self.pirate_combo.values = lst
    
    def buildMarineCombo(self):
        lst = ['']
        cur.execute("""
        SELECT per.id, per.fname
        FROM op.person as per 
        JOIN op.marine as mar ON per.id=mar.id;
        """)
        for row in cur:
            lst.append(str(row[0])+', '+row[1])
        self.marine_combo.values = lst

    def buildArtifactCombo(self):
        lst = []
        cur.execute("SELECT artifact_id, object from op.artifact ORDER BY object ASC;")
        for row in cur:
            lst.append(str(row[0])+', '+row[1])
        self.artifact_combo.values = lst

# class MainApp(App):
#     def build(self):
#         self.root = AppGUI(password='onepiece')
#         return self.root

# if __name__ == '__main__':
#         MainApp().run()

     