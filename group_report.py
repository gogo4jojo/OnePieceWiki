import psycopg2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
import os
from conn import *


def start(password):
    global conn
    global cur
    conn = connection(password)
    cur = conn.cursor()

    if conn is None:
        return None
    else:
        cur = conn.cursor()
        return cur


class GroupReport(BoxLayout):
    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        start(password)
        self.orientation = "vertical"
        
        with self.canvas.before:
            Color(0.82, 0.71, 0.55, 1)  #tan color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)

        self.top_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.7))
        self.add_widget(self.top_layout)

        self.image = Image(source="", size_hint=(0.5, 1))
        self.top_layout.add_widget(self.image)

        self.report_textbox = TextInput(text="", size_hint=(0.5, 1), readonly=True, multiline=True, background_color=(0.96, 0.93, 0.88, 1))
        self.top_layout.add_widget(self.report_textbox)

        self.button_layout = BoxLayout(orientation="horizontal",size_hint=(1, 0.3) )
        self.add_widget(self.button_layout)

        self.group_combo = Spinner(text="Choose group", size_hint=(0.7, 1))
        self.button_layout.add_widget(self.group_combo)

        self.generate_button = Button(text="Generate Report",size_hint=(0.3, 1))
        self.generate_button.bind(on_press=self.generate_report)
        self.button_layout.add_widget(self.generate_button)

        self.buildGroupCombo()

    def update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buildGroupCombo(self):
        lst = []
        try:
            cur.execute("SELECT group_id, group_name FROM op.groups ORDER BY group_name ASC;")
            for row in cur:
                lst.append(f'({row[0]}) '+row[1])
            self.group_combo.values = lst
        except psycopg2.Error as error:
            self.update_report_textbox(f"Error: {error}")

    def generate_report(self, instance):
        owner = self.group_combo.text.strip()
        try:
            text = self.group_combo.text.strip()
            if not text:
                return

            start = text.find('(') + 1 
            end = text.find(')')  
            group_id = int(text[start:end])  
        except Exception as error:
            self.update_report_textbox(str(error))
            return
        
        #two queries are executed but both are reads so no conflict
        try:
            query = f"""SELECT * FROM op.groups WHERE group_id = {group_id};"""
            cur.execute(query)
            result = cur.fetchone()

            if not result:
                self.update_report_textbox("Erm????")
                return

            group_id = result[0] 
            group_name = result[1] 
            base = result[2] if result[2] else ""
            leader_id = result[3] if result[3] else ""
            image = result[4]

            output = (
                f"{group_name}\n\n"
                f"Members:\n"
            )

            query = f"""
            SELECT p.lname, p.mname, p.fname
            FROM op.groups AS g
            JOIN op.membership AS m ON g.group_id = m.group_id
            JOIN op.person AS p ON m.person_id = p.id
            WHERE g.group_id={group_id};
            """

            cur.execute(query)

            members = []

            for row in cur:
                fname = row[2]
                mname = row[1] if row[1] else ""
                lname = row[0] if row[0] else ""
                output += f"{lname} {mname} {fname}".strip()
                output += "\n"


            query = f"""
            SELECT island_name
            FROM op.groups AS g
            JOIN op.island AS i ON g.group_name = i.territory
            WHERE g.group_id={group_id};
            """

            output += "\nTerritories:\n"
            cur.execute(query)
            for row in cur:
                output += f"{row[0]}\n"


            self.handle_image(image, group_name)
            self.update_report_textbox(output)
            self.report_textbox.cursor = (0, 0)
        except psycopg2.Error as error:
            self.update_report_textbox(f"Error: {error}")

    def update_report_textbox(self, message):
        self.report_textbox.text = message

    #https://www.tutorialspoint.com/how-to-write-binary-data-to-a-file-using-python
    def handle_image(self, image, name):
        if image:
            for filename in os.listdir("image/"):
                file_path = os.path.join("image/", filename)
                os.remove(file_path)
            file = open(f"image/{name}.png", "wb")
            file.write(image)
            file.close()
            self.image.source = f"image/{name}.png"
        else:
            self.image.source = "no_image.png"

        self.image.reload()

class ReportApp(App):
    def build(self):
        # start()
        return GroupReport()

# if __name__ == '__main__':
#     ReportApp().run()
