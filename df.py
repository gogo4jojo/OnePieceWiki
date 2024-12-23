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


class DevilFruit(BoxLayout):
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

        self.df_combo = Spinner(text="Choose Devil Fruit", size_hint=(0.7, 1))
        self.button_layout.add_widget(self.df_combo)

        self.generate_button = Button(text="Generate Report",size_hint=(0.3, 1))
        self.generate_button.bind(on_press=self.generate_report)
        self.button_layout.add_widget(self.generate_button)

        self.buildDFCombo()

    def update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buildDFCombo(self):
        lst = []
        try:
            cur.execute("SELECT df_name FROM op.devil_fruit ORDER BY df_name ASC;")
            for row in cur:
                lst.append(str(row[0]))
            self.df_combo.values = lst
        except psycopg2.Error as error:
            self.update_report_textbox(f"Error: {error}")

    def generate_report(self, instance):
        df = self.df_combo.text.strip()
        df_name = f"'{df}'" if df else ""

        #there are two queries that are executed here, but they are both read queries so no conflict
        try:
            query = f"""SELECT * FROM op.devil_fruit WHERE df_name={df_name};"""
            cur.execute(query)
            result = cur.fetchone()

            if not result:
                self.update_report_textbox("Erm... what the sigma????")
                return

            df_name = result[0] 
            type = result[1] 
            awakened = "Yes" if result[2] else "No"
            image = result[3]
            description = result[4] if result[4] else "???"

            output = (
                f"Name: {df_name}\n"
                f"Type: {type}\n"
                f"Awakened: {awakened}\n\n"
            )

            query = f"""
            SELECT fname, mname, lname
            FROM op.person AS P
            JOIN op.devil_fruit_eater AS dfe ON p.id = dfe.eater
            JOIN op.devil_fruit AS df ON dfe.df_name = df.df_name
            WHERE df.df_name='{df_name}';
            """
            
            cur.execute(query)

            people = []

            #row[2] = lname
            #row[1] = manme
            #row[0] = fname
            for row in cur:
                people.append(f"{row[2]} {row[1]} {row[0]}")
                

            if people:
                output += f"\nKnown Eaters:\n" + "\n".join(people)

            output += "\n\nAbilities:\n" + description

            self.update_report_textbox(output)
            self.handle_image(image, df_name)
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
            
        #this is needed to refresh image
        self.image.reload()


class DevilFruitApp(App):
    def build(self):
        # start()
        return DevilFruit()

# if __name__ == '__main__':
#     DevilFruitApp().run()
