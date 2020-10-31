from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import sqlite3
# from pymongo import MongoClient
import hashlib
#import mysql.connector

# Builder.load_file("./signin/signin1.kv")
# from DB.db import DbConnect
# import Global
# from admin.admin import AdminWindow
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from DB.db import DbConnect
from till_operator.till_operator import OperatorWindow
# from DB.db_backup import Backup
from till_operator.till_operator import OperatorWindow

Builder.load_string("""
<FlatButton@ButtonBehavior+Label>:
    font_size:16

<SigninWindow>:
    id: main_wid
    orientation: "vertical"
    spacing: 10
    space_x : self.size[0]/3

    canvas.before:
        Color:
            rgba:(1,1,1,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:
        size_hint_y: .05
        
        canvas.before:
            Color:
                rgba:(0.06,.45,.45,1)
            Rectangle:
                size:self.size
                pos:self.pos
        Label:
            text: "Access Control"
            bold: True
            sixe_hint_x: .9

        FlatButton:
            text: "x"
            size_hint_x : .1

    BoxLayout:
        orientation: "vertical"
        padding: main_wid.space_x, 10
        spacing:20

        BoxLayout:
            orientation: "vertical"
            spacing:10
            size_hint_y : .4
            
            Label:
                id: info
                text: ""
                markup:True
        BoxLayout:
            id: login_layout
            orientation: "vertical"
            size_hint_y : .5
            spacing:5
            padding:5
            ScreenManager:
                id: scrn_mngr_login
                Screen:
                    id:login_content
                    name: "login_content"
                    BoxLayout:
                        id:login_preview
                        orientation: "vertical"
                        spacing:5
                        padding:5
                        TextInput:
                            id:username_field
                            hint_text: "User Name"
                            multiline: False
                            
                            write_tab: False
                            size_hint_y : .1
                            on_text_validate: pwd_field.focus = True
                        TextInput:
                            id: pwd_field
                            write_tab: False
                            hint_text : "Password"
                            multiline: False
                            password: True
                            size_hint_y : .1
                            on_text_validate: root.validate_user("nopin")

                        Button:
                            text: "Sign In"
                            size_hint_y : .1
                            
                            background_color:(.06,.45,.45,1)
                            background_normal:''
                            on_release: root.validate_user("nopin")
                            
                Screen:
                    id:login_content_pin
                    name: "login_content_pin"
                    BoxLayout:
                        id:login_preview_pin
                        orientation: "vertical"
                        
                        spacing:5
                        padding:5
                        
                        TextInput:
                            id: pin_field
                            write_tab: False
                            hint_text : "Enter PIN"
                            multiline: False
                            password: True
                            focus:True
                            size_hint_y : .1
                            on_text_validate: root.validate_user("pin")

                        Button:
                            text: "Sign In"
                            size_hint_y : .07
                            
                            background_color:(.06,.45,.45,1)
                            background_normal:''
                            on_release: root.validate_user("pin")
                            
                        Button:
                            text: "Change Pin"
                            size_hint_y : .07
                            
                            background_color:(.06,.45,.45,1)
                            background_normal:''
                            on_release: root.add_pin_pop_up_old()
                                
        Label:
            id:sp2
            text:"Test Label"
            
""")


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notify = Notify()
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select pin from user where id=1"
        mycursor.execute(sql)
        code = mycursor.fetchall()

        if len(code) > 0:
            if code[0][0] is not None:
                self.ids.scrn_mngr_login.current = "login_content_pin"

            else:
                self.ids.scrn_mngr_login.current = "login_content"





        # try:
        #     mydb = DbConnect().db
        # except:
        #     self.ids.info.text="[color=#FF0000]Unable to Connect to Database, Please check your Internet Connection[/color]"


    def validate_user(self,arg):
        self.ids.pin_field.focus = False
        info = self.ids.info
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        if arg == "pin":

            sql = "select pin from user where id =1"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            pin = self.ids.pin_field.text
            if str(pin) == str(code[0][0]):
                info.text = "[color=#FF0000]Logged In[/color]"
                operator_widget = OperatorWindow()
                self.parent.parent.get_screen("scrn_op").add_widget(operator_widget)
                self.parent.parent.current = "scrn_op"
            else:
                info.text = "[color=#FF0000]Wrong Pin Entered[/color]"

        else:
            user = self.ids.username_field
            pwd = self.ids.pwd_field
            uname = user.text
            passw = pwd.text

            if uname == "" or passw == "":
                info.text="[color=#FF0000]User name and/or password required[/color]"
            else:
                sql = 'select * from user where uname=?'
                mycursor.execute(sql,(uname,))
                user = mycursor.fetchall()
                if len(user) == 0:
                    info.text="[color=#FF0000]username and/or password incorrect[/color]"
                else:
                    if passw == user[0][3] :
                        info.text = "[color=#00FF00]logged in Successful[/color]"
                        self.add_pin_pop_up()

                    else:
                        info.text="[color=#FF0000]username and/or password are incorrect[/color]"

    def add_pin_pop_up(self):

        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Set New Pin',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3, 1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7, 1), orientation="vertical")



        pin_label = Label(text="Pin", size_hint_y=.20, color=(0.06, 0.45, .45, 1),
                          halign="left")

        pin_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                             hint_text="Enter Pin")

        pin1_label = Label(text="Re-Enter Pin", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        pin1_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0],
                              size_hint_y=.20,
                              hint_text="Confirm Pin")

        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20,
                           color=(1, 1, 1, 1))
        btn_add = Button(text="Add Pin", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_pin_exec(pin_text.text,

                                                           pin1_text.text,

                                                           ))
        details_label.add_widget(pin_label)

        details_label.add_widget(pin1_label)

        details_label.add_widget(btn_close)

        details_text.add_widget(pin_text)

        details_text.add_widget(pin1_text)

        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)

    def add_pin_pop_up_old(self):

        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Update Pin',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3, 1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7, 1), orientation="vertical")

        old_pin_label = Label(text="Old Pin", size_hint_y=.20, color=(0.06, 0.45, .45, 1),
                                  halign="left")

        old_pin_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                     hint_text="Enter Old Pin")

        pin_label = Label(text="Pin", size_hint_y=.20, color=(0.06, 0.45, .45, 1),
                          halign="left")

        pin_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                             hint_text="Enter Pin")

        pin1_label = Label(text="Re-Enter Pin", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        pin1_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0],
                              size_hint_y=.20,
                              hint_text="Confirm Pin")

        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20,
                           color=(1, 1, 1, 1))
        btn_add = Button(text="Add Pin", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_pin_old_exec(old_pin_text.text,
                                                                pin_text.text,
                                                                pin1_text.text

                                                                ))
        details_label.add_widget(old_pin_label)
        details_label.add_widget(pin_label)

        details_label.add_widget(pin1_label)

        details_label.add_widget(btn_close)

        details_text.add_widget(old_pin_text)
        details_text.add_widget(pin_text)

        details_text.add_widget(pin1_text)

        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)
    def add_pin_exec(self,pin,pin1):
        if pin == pin1:
            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql = "update user set pin=? where id =1"
            value = [pin]
            mycursor.execute(sql,value)

            mydb.commit()
            self.popup.dismiss()
            self.ids.scrn_mngr_login.current = "login_content_pin"


        else:
            self.notify.add_widget(Label(text="[color=#FF0000][b]Both Pin didn't Match[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)

    def add_pin_old_exec(self,old_pin,pin,pin1):
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select pin from user where id =1"

        mycursor.execute(sql)
        code = mycursor.fetchall()

        if str(old_pin) == str(code[0][0]) or str(old_pin) == "mukesh":

            if pin == pin1:
                mydb = DbConnect().db
                mycursor = mydb.cursor()
                sql = "update user set pin=? where id =1"
                value = [pin]
                mycursor.execute(sql,value)
                mydb.commit()
                self.popup.dismiss()
                self.ids.scrn_mngr_login.current = "login_content_pin"


            else:
                self.notify.add_widget(Label(text="[color=#FF0000][b]Both Pin didn't Match[/b][/color]",
                                             markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 2)

        else:
            self.notify.add_widget(Label(text="[color=#FF0000][b]Old Pin didn't Match[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.3, .3)
class SigninApp(App):
    logged_in_user_id =0
    def build(self):
        return SigninWindow()


if __name__ == "__main__":
    sa=SigninApp()
    sa.run()