import psycopg2
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from conn import *

def start(password):
    global conn
    global cur
    conn = connection(password)
    cur = conn.cursor()

    if conn == None:
        return None
    else:
        cur = conn.cursor()
        return cur

# https://stackoverflow.com/questions/37555377/how-to-set-a-height-to-some-buttons-of-gridlayout-in-kivy-python
# https://stackoverflow.com/questions/67954613/how-to-refresh-gridlayout-in-kivy-with-kv-file
# https://stackoverflow.com/questions/43545261/kivy-making-a-table-widget
# https://stackoverflow.com/questions/66178433/why-do-you-need-the-instance-variable-when-creating-a-method-in-kivy



class PersonTable(BoxLayout):
    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        start(password)
        self.orientation = "vertical" #this spaces out the table so it's not so packed together
        self.offset = 0
        self.limit = 5
        self.sort_column = "id"
        self.sort_direction = "ASC"
        self.total_rows = self.get_num_rows()

        self.op_label = Label(text="",size_hint_y=None,height=50)
        self.add_widget(self.op_label)

        #person table has 12 columns
        self.table_layout = GridLayout(cols=12, size_hint_y=None, row_default_height=50, row_force_default=True)

        self.col_names = ["id", "fname", "mname", "lname", "age", "gender", "race", "hometown", "birthday", "height", "status", "job"]

        for col in self.col_names:
            label = Label(text=col,size_hint_y=None,height=50)
            self.table_layout.add_widget(label)

        #scroll feature
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.table_layout)
        self.add_widget(self.scroll_view)

        self.column_combo = Spinner(values=self.col_names, size_hint_x=0.25)
        self.column_combo.bind(text=self.change_sort_column)

        self.direction_combo = Spinner(values=("ASC", "DESC"), size_hint_x=0.25)
        self.direction_combo.bind(text=self.change_sort_direction)

        #next and previous buttons
        self.prev_button = Button(text="Previous", size_hint_x=0.25)
        self.prev_button.bind(on_press=self.prev_rows)

        self.next_button = Button(text="Next", size_hint_x=0.25)
        self.next_button.bind(on_press=self.next_rows)

        self.change_page = BoxLayout(size_hint_y=None, height=50)
        self.change_page.add_widget(self.column_combo)
        self.change_page.add_widget(self.direction_combo)
        self.change_page.add_widget(self.prev_button)
        self.change_page.add_widget(self.next_button)

        self.add_widget(self.change_page)
        self.buildPersonTable()

    def change_sort_column(self, instance, column):
        self.sort_column = column
        self.buildPersonTable()
    
    def change_sort_direction(self, instance, direction):
        self.sort_direction = direction
        self.buildPersonTable()

    def get_num_rows(self):
        try:
            cur.execute("SELECT COUNT(*) FROM op.person")
            total = cur.fetchone()[0]
            return total
        except psycopg2.Error as error:
            print(error)
            return 0
        
    def get_person_rows_v2(self):
        try:
            query = f"""
                SELECT id, fname, mname, lname, age, gender, race, hometown, birthday, height, status, job
                FROM op.person
                ORDER BY {self.sort_column} {self.sort_direction}
                OFFSET {self.offset}
                LIMIT {self.limit};
            """
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as error:
            print(error)
            return []

    #rebuild table
    def buildPersonTable(self):
        # Clear table
        self.table_layout.clear_widgets()

        for col in self.col_names:
            label = Label(
                text=col,
                bold=True,
                size_hint_y=None,
                height=50
            )
            self.table_layout.add_widget(label)

        rows = self.get_person_rows_v2() 
        for row in rows:
            row_id = row[0] 
            for col, value in enumerate(row):
                cell = TextInput(
                    text = str(value) if value else "",
                    multiline=False,
                    size_hint_y=None,
                    height=50,
                    readonly = True if col==0 else False
                )
                col_name = self.col_names[col] 
                #cell.bind(on_text_validate=self.update(row_id,col_name,instance.text))
                #instance refers to the cell or thing that starts the function
                cell.bind(on_text_validate=lambda instance, row=row_id, col=col_name: self.update_cell(row, col, instance.text))
                self.table_layout.add_widget(cell)

        self.op_label.text = f"Showing rows {self.offset + 1} to {min(self.offset + self.limit, self.total_rows)} of {self.total_rows}"

    def update_person(self, id, column, new_val):
        try:
            new_val = int(new_val) if new_val.isnumeric() else f"'{new_val}'"
            query = f"""
                UPDATE op.person 
                SET {column}={new_val} 
                WHERE id={id};"""
            cur.execute(query, (new_val, id))
            return f"Updated #{id}: set {column} to {new_val}"
        except psycopg2.Error as error:
            return str(error)

    def update_cell(self, row_id, column_name, new_value):
        text = self.update_person(row_id, column_name, new_value)
        self.op_label.text = text

    def next_rows(self, instance):
        if self.offset + self.limit < self.total_rows:
            self.offset += self.limit
            self.buildPersonTable()

    def prev_rows(self, instance):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.buildPersonTable()

class PersonTableApp(App):
    def build(self):
        # start()
        return PersonTable()

# if __name__ == '__main__':
#     PersonTableApp().run()
