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


class Report(BoxLayout):
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

        self.person_combo = Spinner(text="Choose person", size_hint=(0.7, 1))
        self.button_layout.add_widget(self.person_combo)

        self.generate_button = Button(text="Generate Report",size_hint=(0.3, 1))
        self.generate_button.bind(on_press=self.generate_report)
        self.button_layout.add_widget(self.generate_button)

        self.buildPersonCombo()

    def update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def buildPersonCombo(self):
        lst = []
        try:
            cur.execute("SELECT id, fname FROM op.person ORDER BY fname ASC;")
            for row in cur:
                lst.append(str(row[0]) + ', ' + row[1])
            self.person_combo.values = lst
        except psycopg2.Error as error:
            self.update_report_textbox(f"Error: {error}")

    def generate_report(self, instance):
        owner = self.person_combo.text.strip()
        try:
            owner_id = int(owner.split(',')[0].strip()) if owner else None
        except Exception as error:
            self.update_report_textbox(str(error))
            return
        
        #two queries are executed but both are reads so no conflict
        try:
            query = f"""SELECT * FROM op.person WHERE id = {owner_id};"""
            #id, fname, mname, lname, age, gender, race, hometown, birthday, height, status, job, last_seen, image, description
            cur.execute(query)
            result = cur.fetchone()

            if not result:
                self.update_report_textbox("Erm????")
                return

            person_id = result[0] 
            fname = result[1] 
            mname = result[2] if result[2] else ""
            lname = result[3] if result[3] else ""
            age = result[4] if result[4] else "???"
            gender = result[5]
            race = result[6] if result[6] else "???"
            hometown = result[7] if result[7] else "???"
            birthday = result[8] if result[8] else "???"
            height = result[9] if result[9] else "???"
            status = result[10] 
            job = result[11] if result[11] else "???"
            last_seen = result[12] if result[12] else "???"
            image = result[13]
            description = result[14] if result[14] else ""

            output = (
                f"ID: {person_id}\nName: {lname} {mname} {fname}\n"
                f"Age: {age}\nGender: {gender}\nRace: {race}\nHometown: {hometown}\n"
                f"Last Seen: {last_seen}\n"
                f"Birthday: {birthday}\nHeight: {height} cm\nStatus: {status}\n"
                f"Job: {job}\n\n"
            )

            query = f"""
            SELECT id, df_name, G.group_name, sword_name, object
            FROM op.person
            LEFT JOIN op.devil_fruit_eater ON eater={owner_id}
            LEFT JOIN op.membership as M ON person_id={owner_id}
            LEFT JOIN op.groups as G ON G.group_id=M.group_id
            LEFT JOIN op.swordsman ON swordsman={owner_id}
            LEFT JOIN op.sword ON sword=sword_id
            LEFT JOIN op.artifact ON owner={owner_id}
            WHERE id = {owner_id};
            """
            
            cur.execute(query)

            dfs = []
            groups = []
            swords = []
            objects = []

            for row in cur:
                if row[1] and row[1] not in dfs:
                    dfs.append(row[1])
                if row[2] and row[2] not in groups:
                    groups.append(row[2])
                if row[3] and row[3] not in swords:
                    swords.append(row[3])
                if row[4] and row[4] not in objects:
                    objects.append(row[4])

            if dfs:
                output += f"\nDevil Fruit:\n" + "\n".join(dfs)
            if groups:
                output += f"\n\nAffiliations:\n" + "\n".join(groups)
            if swords:
                output += f"\n\nWeapons:\n" + "\n".join(swords)
            if objects:
                output += f"\n\nPossessions:\n" + "\n".join(objects)

            output += "\n\n" + description

            self.update_report_textbox(output)
            self.handle_image(image, fname)
            self.report_textbox.cursor = (0, 0)

        except psycopg2.Error as error:
            self.update_report_textbox(f"Error generating report: {error}")


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
        return Report()

# if __name__ == '__main__':
#     ReportApp().run()
