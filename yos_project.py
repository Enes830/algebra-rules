import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import sqlite3
import os

app_path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(app_path, 'yos1.db'))

c = conn.cursor()

c.execute("SELECT lesson_name FROM matimatik1")
lessondb = c.fetchall()

kivy.require("1.10.1")


class ConnectPage(BoxLayout):
    global favdb
    # main page
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 10

        self.matimatik1 = Button(text="MATIMATIK 1")
        self.matimatik1.bind(on_press=self.matimatik1_button)
        self.add_widget(self.matimatik1)

        self.matimatik2 = Button(text="MATIMATIK 2")
        self.matimatik2.bind(on_press=self.matimatik2_button)
        self.add_widget(self.matimatik2)

        self.fav = Button(text="Favorites")
        self.fav.bind(on_press=self.fav1)
        self.add_widget(self.fav)

        # self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label(text="contact me\nemail: eneshalit9@gmail.com\ninstagram: anas_fateen_2003"))

    def matimatik1_button(self, instance):
        chatapp.screen_manager.transition = SlideTransition(direction='left')
        chatapp.screen_manager.current = "first"

    def matimatik2_button(self, instance):
        chatapp.screen_manager.transition = SlideTransition(direction='left')
        chatapp.screen_manager.current = "second"

    def fav1(self, instance):
        global favdb
        chatapp.screen_manager.transition = SlideTransition(direction='left')
        chatapp.screen_manager.current = "fav"
        
        c.execute("SELECT lesson_name FROM matimatik1 where isfavorite = 1")
        favdb = c.fetchall()
        print(favdb)


class first(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inside = GridLayout(cols=1)
        self.inside.size_hint_y = None
        self.inside.row_default_height = '100dp'
        self.inside.bind(minimum_height=self.inside.setter('height'))

        self.goback = Button(text="go back")
        self.goback.bind(on_press=self.goback_button)
        self.inside.add_widget(self.goback)


        for lesson in lessondb:
            for lesson1 in lesson:
                self.lesson = Button(text=lesson1)
                self.lesson.bind(on_press=self.lesson1)
                self.inside.add_widget(self.lesson)

        self.add_widget(self.inside)

    def fav_btn(self, instance):
        if instance.text == "put to Favorites":
            instance.text = "remove from favorites"
            c.execute(f"UPDATE matimatik1 SET isfavorite = 1 WHERE lesson_name = '{self.lesson_name}'")
            conn.commit()
        else:
            instance.text = "put to Favorites"
            c.execute(f"UPDATE matimatik1 SET isfavorite = 0 WHERE lesson_name = '{self.lesson_name}'")
            conn.commit()

    def goback_button(self, instance):
        self.what_btn = instance.text
        what_btn = self.what_btn
        if what_btn == "go back":
            chatapp.screen_manager.transition = SlideTransition(direction='right')
            chatapp.screen_manager.current = "Connect"
        else:
            chatapp.screen_manager.transition = SlideTransition(direction='right')
            chatapp.screen_manager.current = "lesson"
            chatapp.screen_manager.current = "first"
            self.remove_widget(self.inside1)
            self.add_widget(self.inside)

    def lesson1(self, instance):
        chatapp.screen_manager.transition = SlideTransition(direction='left')
        chatapp.screen_manager.current = "lesson"
        chatapp.screen_manager.current = "first"
        self.remove_widget(self.inside)
        self.lesson_name = instance.text

        self.inside1 = GridLayout(cols=1)
        self.inside1.size_hint_y = None
        self.inside1.row_default_height = '100dp'
        self.inside1.bind(minimum_height=self.inside1.setter('height'))

        self.goback = Button(text="Go back")
        self.goback.bind(on_press=self.goback_button)
        self.inside1.add_widget(self.goback)

        c.execute(f"select isfavorite from matimatik1 where lesson_name = '{self.lesson_name}'")
        favo = c.fetchone()

        if favo[0] == 0:
            self.fav = Button(text="put to Favorites")
        else:
            self.fav = Button(text="remove from favorites")

        self.fav.bind(on_press=self.fav_btn)
        self.inside1.add_widget(self.fav)

        self.add_widget(self.inside1)


        c.execute(f"SELECT id FROM matimatik1 where lesson_name = '{self.lesson_name}'")
        self.propertys = c.fetchone()
        self.propertys = self.propertys[0]
        c.execute(f"select content from matimatik1_content where lesson_id = {self.propertys}")
        self.final_prop = c.fetchall()

        for proplist in self.final_prop:
            for proptuple in proplist:
                self.inside1.add_widget(Label(text=proptuple, font_size=30))


class second(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inside = GridLayout()
        self.inside.cols = 1
        self.inside.size_hint_y = None
        self.inside.row_default_height = '100dp'

        self.goback = Button(text="go back")
        self.goback.bind(on_press=self.goback_button)
        self.inside.add_widget(self.goback)
        self.add_widget(self.inside)

    def goback_button(self, instance):
        chatapp.screen_manager.transition = SlideTransition(direction='right')
        chatapp.screen_manager.current = "Connect"


class lesson(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label())


class fav(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.inside = GridLayout()
        self.inside.cols = 1
        self.inside.size_hint_y = None
        self.inside.row_default_height = '100dp'

        self.goback = Button(text="go back")
        self.goback.bind(on_press=self.goback_button)
        self.inside.add_widget(self.goback)
        
        
        
        
        c.execute("SELECT lesson_name FROM matimatik1 where isfavorite = 1")
        favdb = c.fetchall()
        for lesson in favdb:
            for lesson1 in lesson:
                self.lesson = Button(text=lesson1)
                self.lesson.bind(on_press=self.lesson1)
                self.inside.add_widget(self.lesson)

        self.add_widget(self.inside)

    def fav_btn(self, instance):
        if instance.text == "put to Favorites":
            instance.text = "remove from favorites"
            c.execute(f"UPDATE matimatik1 SET isfavorite = 1 WHERE lesson_name = '{self.lesson_name}'")
            conn.commit()

        else:
            instance.text = "put to Favorites"
            c.execute(f"UPDATE matimatik1 SET isfavorite = 0 WHERE lesson_name = '{self.lesson_name}'")
            conn.commit()


    def goback_button(self, instance):
        self.what_btn = instance.text
        what_btn = self.what_btn
        if what_btn == "go back":
            chatapp.screen_manager.transition = SlideTransition(direction='right')
            chatapp.screen_manager.current = "Connect"

        else:
            chatapp.screen_manager.transition = SlideTransition(direction='right')
            chatapp.screen_manager.current = "lesson"
            chatapp.screen_manager.current = "fav"
            self.remove_widget(self.inside1)
            self.add_widget(self.inside)

    def lesson1(self, instance):
        chatapp.screen_manager.transition = SlideTransition(direction='left')
        chatapp.screen_manager.current = "lesson"
        chatapp.screen_manager.current = "fav"
        self.remove_widget(self.inside)
        self.lesson_name = instance.text

        self.inside1 = GridLayout(cols=1)
        self.inside1.size_hint_y = None
        self.inside1.row_default_height = '100dp'
        self.inside1.bind(minimum_height=self.inside1.setter('height'))

        self.goback = Button(text="Go back")
        self.goback.bind(on_press=self.goback_button)
        self.inside1.add_widget(self.goback)

        c.execute(f"select isfavorite from matimatik1 where lesson_name = '{self.lesson_name}'")
        favo = c.fetchone()

        if favo[0] == 0:
            self.fav = Button(text="put to Favorites")
        else:
            self.fav = Button(text="remove from favorites")

        self.fav.bind(on_press=self.fav_btn)
        self.inside1.add_widget(self.fav)

        self.add_widget(self.inside1)


        c.execute(f"SELECT id FROM matimatik1 where lesson_name = '{self.lesson_name}'")
        self.propertys = c.fetchone()
        self.propertys = self.propertys[0]
        c.execute(f"select content from matimatik1_content where lesson_id = {self.propertys}")
        self.final_prop = c.fetchall()

        for proplist in self.final_prop:
            for proptuple in proplist:
                self.inside1.add_widget(Label(text=proptuple, font_size=30))


class EpicApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        # first page
        self.first = first()
        screen = Screen(name='first')
        screen.add_widget(self.first)
        self.screen_manager.add_widget(screen)
        # second page
        self.second = second()
        screen = Screen(name='second')
        screen.add_widget(self.second)
        self.screen_manager.add_widget(screen)
        # demo page
        self.lesson = lesson()
        screen = Screen(name='lesson')
        screen.add_widget(self.lesson)
        self.screen_manager.add_widget(screen)

        self.fav = fav()
        screen = Screen(name='fav')
        screen.add_widget(self.fav)
        self.screen_manager.add_widget(screen)

        # self.screen_manager.current(second)

        return self.screen_manager


# conn.close()


if __name__ == "__main__":
    chatapp = EpicApp()
    chatapp.run()
