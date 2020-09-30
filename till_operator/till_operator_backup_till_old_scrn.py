from datetime import datetime
from functools import partial

from kivy import app
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from DB.db import DbConnect

Builder.load_string("""
<FlatButton@ButtonBehavior+Label>:
    font_size: 14
    
<CanvasBoxLayout@BoxLayout>:
    canvas.before:
        Color:
            rgba:(.06,.45,.45,1)
        Rectangle:
            size: self.size
            pos:self.pos
<CanvasGridLayout@GridLayout>:
    canvas.before:
        Color:
            rgba:(.06,.45,.45,1)
        Rectangle:
            size: self.size
            pos:self.pos
<CanvasPopup@Popup>:
    canvas.before:
        Color:
            rgba:(.06,.45,.45,1)
        Rectangle:
            size: self.size
            pos:self.pos
<OperatorWindow>:
    id: main_wid
    orientation: "vertical"

    canvas.before:
        Color:
            rgb:(1,1,1,1)
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        id: header
        size_hint_y: .05
        spacing:5


        canvas.before:
            Color:
                rgb:(.06,.45,.45,1)
            Rectangle:
                size: self.size
                pos: self.pos

        Label:
            text: ""
            id:label_client_name
            size_hint_x: .9
            bold: True
            color:(1,1,1,1)
        FlatButton:
            id: logged_in_user
            text: "Mukesh"
            color:(1,1,1,1)



    BoxLayout:
        id: preview_nav
        orientation: "vertical"
        spacing:5
        padding:5
        BoxLayout:
            id:vendor
            spacing:5
            size_hint_y: .1
            
            canvas.before:
                Color:
                    rgb:(.06,.45,.45,1)
                Rectangle:
                    size:self.size
                    pos: self.pos
            Label:
                text: "Vendor"
                id:label_c
                size_hint_x:.15
                bold: True
                color:(1,1,1,1)
            TextInput:
                id: vendor_id
                hint_text: "Search by Name"
                padding:[5,0,0,0]
                size_hint_x: .50
                on_text_validate:root.get_vendor()
                
                
                multiline:False
                write_tab: False
                focus:True
            Button:
                text: "Add New vendor"
                background_normal: ""
                background_color: (.06,.32,.32,1)
                size_hint_x:.35
                on_release:root.add_new_vendor()
        BoxLayout:
            id: preview_tabs

            size_hint_x:1
            size_hint_y:.1

            spacing:3
            canvas.before:
                Color:
                    rgb:(.06,.40,.40,1)
                Rectangle:
                    size: self.size
                    pos: self.pos
            ToggleButton:
                id: booking_toggle
                text:"Booking"
                size_hint_x:.3
                state:"down"
                background_color: (0.06,.47,.47,1)
                background_normal:""
                group:"admin_navs"
                on_state: root.change_scrn(self)
                
            ToggleButton:
                id: delivery_toggle
                text:"Delivery"
                size_hint_x:.3
                
                background_color: (0.06,.47,.47,1)
                background_normal:""
                group:"admin_navs"
                on_state: root.change_scrn(self)
            ToggleButton:
                id: approval_toggle
                text:"Approval"
                size_hint_x:.3
                
                background_color: (0.06,.47,.47,1)
                background_normal:""
                group:"admin_navs"
                on_state: root.change_scrn(self)
            
            
        BoxLayout:
            id: preview
            orientation: "vertical"
            
            size_hint_y:.8
            spacing:5
            padding:5
            
            ScreenManager:
                id: scrn_mngr_operator


                Screen:
                    id:book_content
                    name: "book_content"
                    BoxLayout:
                        id:book_preview
                        orientation: "vertical"
                        spacing:5
                        padding:5
                        
                        
                    
                        
                Screen:
                    id:delivery_content
                    name: "delivery_content"
                    BoxLayout:
                        id:delivery_preview
                        orientation: "vertical"
                        spacing:5
                        padding:5
                Screen:
                    id:approval_content
                    name: "approval_content"
                    BoxLayout:
                        id:approval_preview
                        orientation: "vertical"
                        spacing:5
                        padding:5
                Screen:
                    id: blank
                    name: "blank"
                    BoxLayout:
                        id:blank_preview
                        orientation: "vertical"



 """)


class WrappedLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))


class WrappedButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))


class CanvasBoxLayout(BoxLayout):
    pass

class CanvasPopup(Popup):
    pass


class CanvasGridLayout(GridLayout):
    pass

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.3, .3)

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notify = Notify()
        self.vendor_id =0
        self.back_count = 0
        Window.bind(on_keyboard=self.on_key)

    def stop_app(self,arg):

        App.get_running_app().stop()


    def on_key(self, window, key, *args):


        if key == 27:

            details = BoxLayout(size_hint_y=1, pos_hint={'top': 1}, orientation="vertical")
            # products_container.add_widget(details)
            self.popup = Popup(title='Exit Confirmation!!',
                               content=details,
                               size_hint=(.8, .25))

            self.popup.open()
            lb4 = Label(text='[color=ff3333]Are You Sure to Exit?[/color][color=3333ff][/color]' + "\n\n",
                        markup=True, size_hint=(.8, .4))
            details.add_widget(lb4)
            details_action = BoxLayout(size_hint=(1, .2))
            details.add_widget(details_action)
            btn_close = Button(text="No", on_release=self.popup.dismiss, size_hint=(.5,1), color=(1, 1, 1, 1))
            btn_dlt = Button(text="Yes", size_hint=(.5,1), color=(1, 1, 1, 1),
                             on_release=self.stop_app)

            details_action.add_widget(btn_dlt)
            details_action.add_widget(btn_close)
            return True
        else:
            pass







    def change_scrn(self,instance):
        if instance.state == "down":

            if instance.text == "Booking":
                self.ids.scrn_mngr_operator.current = "book_content"
                self.get_booking(1)

            elif instance.text == "Delivery":
                self.ids.scrn_mngr_operator.current = "delivery_content"
                self.get_delivery(1)

            elif instance.text == "Approval":
                self.ids.scrn_mngr_operator.current = "approval_content"
                self.get_approval(1)





        else:
            self.ids.scrn_mngr_operator.current = "blank"


    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def get_vendor(self):
        input_text = str(self.ids.vendor_id.text)
        if len(input_text) > 2:
            details = BoxLayout(size_hint_y=.9, pos_hint={'top': 1})
            # products_container.add_widget(details)
            self.popup = Popup(title='Vendor',
                               content=details,
                               size_hint=(.9, .9))



            details_1 = BoxLayout(size_hint=(1, 1), orientation="vertical")
            details.add_widget(details_1)
            root = ScrollView(size_hint=(1, 1),
                              pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
            details_1.add_widget(root)
            layout = GridLayout(cols=2, spacing=10,
                                size_hint=(1, None))
            layout.bind(minimum_height=layout.setter('height'))
            root.add_widget(layout)

            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql = "select * from vendor where name like ? or contact like ?"
            value = [input_text+ "%",input_text+ "%"]
            mycursor.execute(sql,value)
            code = mycursor.fetchall()

            if len(code) > 0:
                self.popup.open()

                for i in code:
                    name = str(i[1])
                    if len(name) > 25:
                        name = name[:25] + "..."
                    adrs = str(i[2])
                    if len(adrs) > 25:
                        adrs = adrs[:25] + "..."
                    contact = str(i[3])
                    if len(contact) > 25:
                        contact = contact[:25] + "..."
                    btn = WrappedButton(
                        text="  " + str(name) + "\n  " + str(adrs) + "\n  " + str(contact),
                        size_hint=(.8, None), height=Window.height / 6, font_size=40,
                        on_release=partial(self.set_vendor, i[0],str(i[1]),str(i[2]),str(i[3])),background_color=(0.06, .47, .47, 1),
                        background_normal="")
                    edit_btn = WrappedButton(
                        text="\n Update  \n",
                        size_hint=(.2, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.edit_vendor, str(i[0])))
                    layout.add_widget(btn)
                    layout.add_widget(edit_btn)

    def set_vendor(self, id, name,adrs,contact,arg):
        self.popup.dismiss()

        container = self.ids.vendor_id
        vendor_text = name+", "+adrs+", "+contact
        if len(vendor_text) > 40:
            vendor_text = vendor_text[:40]+"..."

        container.text = vendor_text
        #container.clear_widgets()

        self.vendor_id = int(id)
        self.popup.dismiss()

        # booking_toggle = ToggleButton(text="Booking", size_hint_x=.3,
        #                                background_color=(0.06, .47, .47, 1),
        #                               background_normal="", group="admin_navs"
        #                               )
        # booking_toggle.bind(state=self.get_booking)
        # delivery_toggle = ToggleButton(text="Delivery", size_hint_x=.3,
        #                                 background_color=(0.06, .47, .47, 1),
        #                                background_normal="", group="admin_navs")
        # delivery_toggle.bind(state=self.get_delivery)
        # approval_toggle = ToggleButton(text="Approval", size_hint_x=.3,
        #                                 background_color=(0.06, .47, .47, 1),
        #                                background_normal="", group="admin_navs")
        # approval_toggle.bind(state=self.get_approval)
        # container.add_widget(booking_toggle)
        # container.add_widget(delivery_toggle)
        # container.add_widget(approval_toggle)
        self.get_booking(1)

    def edit_vendor(self,id,arg):
        self.popup.dismiss()
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Update Vendor',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3, 1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7, 1), orientation="vertical")
        details_action = BoxLayout(size_hint=(1, .2))

        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select * from vendor where id=?"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()
        for i in code:
            name_label = Label(text="Name", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

            name_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                   hint_text="Name", text=str(i[1]))

            ad_label = Label(text="Address", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            ad_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                    hint_text="Enter Address", text=str(i[2]))
            c_label = Label(text="Contact", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            c_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                  hint_text="Enter Contact Number", text=str(i[3]))

            btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
            btn_add = Button(text="Update", size_hint_y=1, color=(1, 1, 1, 1),
                             on_release=lambda x: self.edit_vendor_exec(name_text.text,

                                                                         ad_text.text,
                                                                         c_text.text,
                                                                         str(i[0])
                                                                         ))
            btn_dlt = Button(text="Delete", size_hint_y=1, color=(1, 1, 1, 1),
                             on_release=lambda x: self.delete_vendor_exec(
                                                                        str(i[0])
                                                                        ))
            details_label.add_widget(name_label)

            details_label.add_widget(ad_label)
            details_label.add_widget(c_label)

            details_label.add_widget(btn_close)

            details_text.add_widget(name_text)

            details_text.add_widget(ad_text)
            details_text.add_widget(c_text)
            details_text.add_widget(details_action)

            details_action.add_widget(btn_dlt)

            details_action.add_widget(btn_add)

            details.add_widget(details_label)
            details.add_widget(details_text)


    def delete_vendor_exec(self, id):
        self.popup.dismiss()

        mydb = DbConnect().db
        mycursor = mydb.cursor()

        sql = "delete from vendor where id=?"

        value = [id]
        mycursor.execute(sql, value)
        mydb.commit()


    def edit_vendor_exec(self, name, ad, con, id):


        if name == "" or ad == "" or con == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All fields are \nrequired[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "update vendor set name=?,address=?,contact=? where id=?"

            value = [name, ad, con, id]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()



    def get_booking(self,arg):
        if self.vendor_id == 0:
            container = self.ids.book_preview
            container.clear_widgets()
        else:

            details = BoxLayout(size_hint_y=.9, pos_hint={'top': 1})

            container = self.ids.book_preview

            container.clear_widgets()
            btn_add = WrappedButton(
                text=" Add New Booking",
                size_hint=(1, None), height=Window.height / 9, font_size=40,
                background_color=(0.06, .47, .47, 1),
                background_normal="",on_release = partial(self.add_new_booking) )
            container.add_widget(btn_add)
            container.add_widget(details)

            # products_container.add_widget(details)
            # self.popup = Popup(title='Vendor',
            #                    content=details,
            #                    size_hint=(.8, .7))
            # self.popup.open()

            details_1 = BoxLayout(size_hint=(1, 1), orientation="vertical")
            details.add_widget(details_1)
            root = ScrollView(size_hint=(1, 1),
                              pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
            details_1.add_widget(root)
            layout = GridLayout(cols=3, spacing=10,
                                size_hint=(1, None))
            layout.bind(minimum_height=layout.setter('height'))
            root.add_widget(layout)

            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql = "select * from book where vendor_id=?"
            value = [self.vendor_id]
            mycursor.execute(sql, value)
            code = mycursor.fetchall()


            if len(code) > 0:
                for i in code:
                    metal = str(i[2])
                    if len(metal) > 10:
                        metal = metal[:10] + "..."
                    wt = str(i[3])
                    if len(wt) > 12:
                        wt = wt[:12] + "..."
                    rt = str(i[4])
                    if len(rt) > 12:
                        rt = rt[:12] + "..."
                    dt = str(i[5])
                    btn = WrappedButton(
                        text=" Metal: " + str(metal) + "\n Weight: " + str(wt) + " gm\n Rate/gm : " + str(rt)+ "\n Date: " + str(dt),
                        size_hint=(.7, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                                           background_normal="",)
                    edit_btn = WrappedButton(
                        text="\n Edit"+ "\n \n ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="",on_release=partial(self.edit_booking,str(i[0])) )
                    dlt_btn = WrappedButton(
                        text="\n Dlt"+ "\n \n ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="",on_release=partial(self.dlt_booking,str(i[0])) )
                    layout.add_widget(btn)
                    layout.add_widget(edit_btn)
                    layout.add_widget(dlt_btn)
    def edit_booking(self,id,arg):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Edit Booking',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select * from book where id=?"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()
        for i in code:
            metal_label = Label(text="Metal", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

            metal_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                   hint_text="Metal",text=str(i[2]))

            weight_label = Label(text="Weight", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            weight_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                    hint_text="Enter weight",text=str(i[3]))
            rate_label = Label(text="Rate", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            rate_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                  hint_text="Enter Rate",text=str(i[4]))

            btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
            btn_add = Button(text="Update Booking", size_hint_y=.20, color=(1, 1, 1, 1),
                             on_release=lambda x: self.edit_booking_exec(metal_text.text,

                                                                   weight_text.text,
                                                                   rate_text.text,
                                                                         str(i[0])
                                                                   ))
            details_label.add_widget(metal_label)

            details_label.add_widget(weight_label)
            details_label.add_widget(rate_label)

            details_label.add_widget(btn_close)

            details_text.add_widget(metal_text)

            details_text.add_widget(weight_text)
            details_text.add_widget(rate_text)

            details_text.add_widget(btn_add)

            details.add_widget(details_label)
            details.add_widget(details_text)

    def edit_booking_exec(self, metal, weight, rate,id):
        f_weight = "wrong"

        f_rate = "wrong"
        # f_date = "wrong"

        try:
            f_weight = round(float(weight), 4)
            f_rate = round(float(rate), 2)

            # f_date = datetime.strptime(date, '%d-%m-%Y')

        except:
            pass
        if weight == "" or rate == "":
            f_weight = "wrong"

            f_rate = "wrong"

        if metal == "" or f_rate == "wrong" or f_weight == "wrong":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Enter Correct Number \nor Metal[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "update book set metal=?,weight=?,rate=? where id=?"

            value = [metal, weight, rate, id]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_booking(1)
        # self.ids.products.remove_widget(id_form.parent)
    def dlt_booking(self,id,arg1):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1}, orientation="vertical")
        # products_container.add_widget(details)
        self.popup = Popup(title='Delete Booking Confirmation!!',
                           content=details,
                           size_hint=(.8, .25))

        self.popup.open()
        lb4 = Label(text='[color=ff3333]Are You Sure to Delete?[/color][color=3333ff][/color]'+"\n\n",
                    markup=True, size_hint=(.8, .4))
        details.add_widget(lb4)
        details_action = BoxLayout(size_hint=(1, .2))
        details.add_widget(details_action)
        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint=(.5,1), color=(1, 1, 1, 1))
        btn_dlt = Button(text="Delete Booking", size_hint=(.5,1), color=(1, 1, 1, 1),
                         on_release=lambda x: self.delete_booking_exec(
                                                                     id
                                                                     ))
        details_action.add_widget(btn_close)
        details_action.add_widget(btn_dlt)

    def delete_booking_exec(self,id):
        self.popup.dismiss()
        mydb = DbConnect().db
        mycursor = mydb.cursor()

        sql = "delete from book where id=?"

        value = [id]
        mycursor.execute(sql, value)
        mydb.commit()
        self.get_booking(1)






    def get_delivery(self,arg):
        if self.vendor_id == 0:
            container = self.ids.delivery_preview
            container.clear_widgets()
        else:
            details = BoxLayout(size_hint_y=.9, pos_hint={'top': 1})
            container = self.ids.delivery_preview
            container.clear_widgets()
            header_layout = GridLayout(cols=3, spacing=10,
                                size_hint=(1, None),height=Window.height / 6,)
            btn_add = WrappedButton(
                text=" Add New \n Delivery",
                size_hint=(.25, None), height=Window.height / 9, font_size=40,
                background_color=(0.06, .47, .47, 1),
                background_normal="", on_release=partial(self.add_new_delivery))
            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql ="SELECT sum(amount)-sum(paid)-sum(paying) as amount from " \
                 "payment  p where delivery_id in " \
                 " (SELECT distinct(oi.delivery_id) FROM payment oi " \
                 "where oi.delivery_id <> 0 and vendor_id =? ) " \
                 " and id=(select max(id) from payment p1" \
                 " where p1.delivery_id=p.delivery_id)"
            value = [self.vendor_id]
            mycursor.execute(sql, value)
            total_amount_code = mycursor.fetchall()
            total_amount = 0
            if len(total_amount_code) > 0 and total_amount_code[0][0] is not None:

                total_amount = int(total_amount_code[0][0])

            sql = "select sum(amount) from payment where delivery_id = 0 and vendor_id=?"
            value = [self.vendor_id]
            mycursor.execute(sql, value)
            advance_amount_code = mycursor.fetchall()
            advance_amount =0

            if len(advance_amount_code) > 0 and advance_amount_code[0][0] is not None:
                advance_amount = int(advance_amount_code[0][0])
            final_total_amount = total_amount - advance_amount
            btn_add1 = WrappedButton(
                text=" Total:\n "+ str(final_total_amount),
                size_hint=(.35, None), height=Window.height / 9, font_size=40,
                background_color=(0.06, .47, .47, 1),
                background_normal="")


            btn_add2 = WrappedButton(
                text=" Extra:\n "+str(advance_amount),
                size_hint=(.35, None), height=Window.height / 9, font_size=40,
                background_color=(0.06, .47, .47, 1),
                background_normal="", on_release=partial(self.show_payment, 0 ))
            container.add_widget(header_layout)
            header_layout.add_widget(btn_add)
            header_layout.add_widget(btn_add1)
            header_layout.add_widget(btn_add2)
            container.add_widget(details)
            # products_container.add_widget(details)
            # self.popup = Popup(title='Vendor',
            #                    content=details,
            #                    size_hint=(.8, .7))
            # self.popup.open()

            details_1 = BoxLayout(size_hint=(1, 1), orientation="vertical")
            details.add_widget(details_1)
            root = ScrollView(size_hint=(1, 1),
                              pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
            details_1.add_widget(root)
            layout = GridLayout(cols=3, spacing=10,
                                size_hint=(1, None))
            layout.bind(minimum_height=layout.setter('height'))
            root.add_widget(layout)

            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql = "select * from delivery where vendor_id=?"
            value = [self.vendor_id]
            mycursor.execute(sql, value)
            code = mycursor.fetchall()

            if len(code) > 0:
                for i in code:
                    metal = str(i[5])
                    if len(metal) > 10:
                        metal = metal[:10] + "..."
                    wt = str(i[2])
                    if len(wt) > 12:
                        wt = wt[:12] + "..."
                    rt = str(i[3])
                    if len(rt) > 12:
                        rt = rt[:12] + "..."
                    dt = str(i[4])
                    btn = WrappedButton(
                        text=" " + str(metal) + " Wt: " + str(wt) + " gm\n Rs:" +str(int(round(float(i[2]),4)*round(float(i[3]),4))) +"\n Rate/gm: " + str(rt) + "\n Date: " + str(dt),
                        size_hint=(.7, None), height=Window.height / 6, font_size=40,
                         background_color=(0.06, .47, .47, 1),
                        background_normal="",on_release=partial(self.show_payment, str(i[0])) )
                    edit_btn = WrappedButton(
                        text="\n Edit"+ "\n " + "\n  ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.edit_delivery, str(i[0])))
                    dlt_btn = WrappedButton(
                        text="\n Dlt"+ "\n " + "\n  ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.dlt_delivery, str(i[0])))
                    layout.add_widget(btn)
                    layout.add_widget(edit_btn)
                    layout.add_widget(dlt_btn)

    def show_payment(self,id,arg):
        id = int(id)
        details_master = BoxLayout(size_hint_y=1,  pos_hint={'top': 1},
                                   orientation="vertical")
        # products_container.add_widget(details)
        self.popup = Popup(title='Delivery Payment Details',
                           content=details_master,
                           size_hint=(1, .8))
        self.popup.open()
        details = BoxLayout(size_hint=(1,.3), pos_hint={'top': 1})
        details_history = BoxLayout(size_hint=(1,.6), orientation="vertical")
        details_master.add_widget(details)
        details_master.add_widget(details_history)

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")
        details.add_widget(details_label)
        details.add_widget(details_text)

        add_label = Label(text="Amount", size_hint_y=.25, color=(0.06, 0.45, .45, 1))
        txt_add_payment = TextInput(hint_text="Enter Amount", multiline=False, size_hint_y=.25)
        des_label = Label(text="Description", size_hint_y=.25, color=(0.06, 0.45, .45, 1))
        txt_des = TextInput(hint_text="Description", multiline=False, size_hint_y=.25)
        date_label = Label(text="Date", size_hint_y=.25, color=(0.06, 0.45, .45, 1))
        date_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.25,
                              text=datetime.now().strftime("%d-%m-%Y"))
        btn_submit_add_payment = Button(text="Add Payment", size_hint_y=.25,
                                        on_release=lambda x: self.add_payment_exec(txt_add_payment.text, id,
                                                                                        txt_des.text,
                                                                                        date_text.text))
        btn_remove_add_payment = Button(text="Cancel", size_hint_y=.25,
                                        on_release=self.popup.dismiss)

        # bx_add_payment.add_widget(lb_add_payment)
        details_label.add_widget(add_label)
        details_label.add_widget(date_label)
        details_label.add_widget(des_label)

        details_label.add_widget(btn_remove_add_payment)

        details_text.add_widget(txt_add_payment)
        details_text.add_widget(date_text)
        details_text.add_widget(txt_des)
        details_text.add_widget(btn_submit_add_payment)

        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "SELECT amount, paid, paying, amount-paid-paying," \
              " date,id,des FROM payment where delivery_id=? and vendor_id=?"
        value = [id,self.vendor_id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()


        root = ScrollView(size_hint=(1, .6),
                          pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)

        layout = GridLayout(cols=1, spacing=5,
                            size_hint=(1, None))

        layout.bind(minimum_height=layout.setter('height'))
        root.add_widget(layout)
        history_label = Label(text="Payment History", size_hint=(.1, None), height=Window.height / 20)

        layout.add_widget(history_label)

        description_layout = GridLayout(cols=1, spacing=0,
                                        size_hint=(1,.1))
        details_history.add_widget(description_layout)
        details_history.add_widget(root)

        def call_inner_function(des, args):

            description_layout.clear_widgets()
            des_label = Label(text="Description:" + str(des), size_hint=(1, .1),
                              color=(0.06, 0.45, .45, 1))
            description_layout.add_widget(des_label)

        layout11 = GridLayout(cols=7, spacing=2,
                             size_hint=(1, None), height=Window.height / 20)
        btn1 = Button(text="#",
                      size_hint=(.05,.1))
        btn2 = Button(text="Amount",size_hint=(.19,.1))
        btn3 = Button(text="Paid", size_hint=(.17,.1))
        btn4 = Button(text="Paying", size_hint=(.17,.1))
        btn5 = Button(text="Remaining", size_hint=(.18,.1))
        btn6 = Button(text="Date", size_hint=(.19,.1))
        btn7 = Button(text="Des", size_hint=(.09,.1))
        layout11.add_widget(btn1)
        layout11.add_widget(btn2)
        layout11.add_widget(btn3)
        layout11.add_widget(btn4)
        layout11.add_widget(btn5)
        layout11.add_widget(btn6)
        layout11.add_widget(btn7)

        layout.add_widget(layout11)
        count = 1

        for i in code:
            layout1 = GridLayout(cols=7, spacing=2,
                             size_hint=(1, None), height=Window.height / 20)
            btn1 = Button(text="X", size_hint=(.05,.1),on_release=partial(self.delete_payment_item,int(i[5])))
            btn2 = Button(text=str(i[0]), size_hint=(.19,.1))
            btn3 = Button(text=str(i[1]), size_hint=(.17,.1))
            btn4 = Button(text=str(i[2]), size_hint=(.17,.1))
            btn5 = Button(text=str(i[3]), size_hint=(.18,.1))
            btn6 = Button(text=str(datetime.strftime(datetime.strptime(i[4],'%d-%m-%Y'),'%d-%m-%Y')), size_hint=(.19,.1))
            desc_text = ""
            if str(i[6]) != "None":
                desc_text = "Click"

            btn7 = Button(text=desc_text, size_hint=(.09,.1),on_release = partial(call_inner_function,str(i[6])))

            layout1.add_widget(btn1)
            layout1.add_widget(btn2)
            layout1.add_widget(btn3)
            layout1.add_widget(btn4)
            layout1.add_widget(btn5)
            layout1.add_widget(btn6)
            layout1.add_widget(btn7)

            layout.add_widget(layout1)
            count += 1



    def delete_payment_item(self,id,arg):
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "delete from payment where id=?"
        value = [int(id)]
        mycursor.execute(sql, value)
        mydb.commit()
        self.popup.dismiss()
        self.get_delivery(1)

    def add_payment_exec(self,amount,id,des,date):
        f_amount = "wrong"

        f_date = "wrong"

        try:
            f_amount = round(float(amount), 2)

            f_date = datetime.strptime(date, '%d-%m-%Y')

        except:
            pass
        if amount == "":
            f_amount = "wrong"

        if f_amount == "wrong" or f_date == "wrong":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Enter Correct Number \nor Date[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:

            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "SELECT paid+paying,amount FROM payment where delivery_id=? order by id desc limit 1"
            value = [id]
            mycursor.execute(sql, value)
            code = mycursor.fetchall()
            paid = 0
            amount_total = 0
            if len(code) > 0:
                paid = code[0][0]
                amount_total = code[0][1]
            if id == 0:
                paid = 0
                amount_total = amount
                amount = 0


            sql = "insert into payment(delivery_id,amount,paid,paying,des,date,vendor_id) values(?,?,?,?,?,?,?)"

            value = [id,amount_total,paid,amount,des,date,self.vendor_id]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_delivery(1)

    def edit_delivery(self,id,arg):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Edit Delivery',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select * from delivery where id=?"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()
        for i in code:
            metal_label = Label(text="Metal", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

            metal_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                   hint_text="Metal",text=str(i[5]))

            weight_label = Label(text="Weight", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            weight_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                    hint_text="Enter weight",text=str(i[2]))
            rate_label = Label(text="Rate", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
            rate_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                  hint_text="Enter Rate",text=str(i[3]))

            btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
            btn_add = Button(text="Update Delivery", size_hint_y=.20, color=(1, 1, 1, 1),
                             on_release=lambda x: self.edit_delivery_exec(metal_text.text,

                                                                   weight_text.text,
                                                                   rate_text.text,
                                                                         str(i[0])
                                                                   ))
            details_label.add_widget(metal_label)

            details_label.add_widget(weight_label)
            details_label.add_widget(rate_label)

            details_label.add_widget(btn_close)

            details_text.add_widget(metal_text)

            details_text.add_widget(weight_text)
            details_text.add_widget(rate_text)

            details_text.add_widget(btn_add)

            details.add_widget(details_label)
            details.add_widget(details_text)

    def edit_delivery_exec(self, metal, weight, rate,id):
        f_weight = "wrong"

        f_rate = "wrong"
        # f_date = "wrong"

        try:
            f_weight = round(float(weight), 4)
            f_rate = round(float(rate), 2)

            # f_date = datetime.strptime(date, '%d-%m-%Y')

        except:
            pass
        if weight == "" or rate == "":
            f_weight = "wrong"

            f_rate = "wrong"

        if metal == "" or f_rate == "wrong" or f_weight == "wrong":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Enter Correct Number \nor Metal[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "update delivery set metal=?,weight=?,rate=? where id=?"

            value = [metal, weight, rate, id]
            mycursor.execute(sql, value)
            sql = "update payment set amount=? where delivery_id=?"

            value = [int(round(float(weight),4)*round(float(rate),4)), id]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_delivery(1)
        # self.ids.products.remove_widget(id_form.parent)
    def dlt_delivery(self,id,arg1):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1}, orientation="vertical")
        # products_container.add_widget(details)
        self.popup = Popup(title='Delete Delivery Confirmation!!',
                           content=details,
                           size_hint=(.8, .25))

        self.popup.open()
        lb4 = Label(text='[color=ff3333]Are You Sure to Delete?[/color][color=3333ff][/color]'+"\n\n",
                    markup=True, size_hint=(.8, .4))
        details.add_widget(lb4)
        details_action = BoxLayout(size_hint=(1, .2))
        details.add_widget(details_action)
        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint=(.5,1), color=(1, 1, 1, 1))
        btn_dlt = Button(text="Delete Delivery", size_hint=(.5,1), color=(1, 1, 1, 1),
                         on_release=lambda x: self.delete_delivery_exec(
                                                                     id
                                                                     ))
        details_action.add_widget(btn_close)
        details_action.add_widget(btn_dlt)

    def delete_delivery_exec(self,id):
        self.popup.dismiss()
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql ="select paid+paying-amount as f_amount from payment where delivery_id=? order by id desc limit 1"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()

        if len(code)> 0:
            if int(code[0][0])>0:
                details = BoxLayout(size_hint_y=1, pos_hint={'top': 1}, orientation="vertical")
                # products_container.add_widget(details)
                self.popup = Popup(title='Add Extra Payment Confirmation!!',
                                   content=details,
                                   size_hint=(.8, .25))

                self.popup.open()
                lb4 = Label(text='[color=ff3333]Do you want to keep Extra payment of[/color][color=3333ff]'+str(code[0][0])+'[/color]' + "\n\n",
                            markup=True, size_hint=(.8, .4))
                details.add_widget(lb4)
                details_action = BoxLayout(size_hint=(1, .2))
                details.add_widget(details_action)
                btn_close = Button(text="No", on_release=self.popup.dismiss, size_hint=(.5,1),
                                   color=(1, 1, 1, 1))
                btn_dlt = Button(text="Yes", size_hint=(.5,1), color=(1, 1, 1, 1),
                                 on_release=lambda x: self.add_zero_payment(
                                     code[0][0]
                                 ))
                details_action.add_widget(btn_close)
                details_action.add_widget(btn_dlt)
        sql = "delete from delivery where id=?"

        value = [id]
        mycursor.execute(sql, value)
        sql = "delete from payment where delivery_id=?"


        mycursor.execute(sql, value)
        mydb.commit()
        self.get_delivery(1)

    def add_zero_payment(self,amount):
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "insert into payment(delivery_id," \
              "amount,date,vendor_id) " \
              "values(?,?,?,?)"
        value = [0,amount, datetime.now().strftime("%d-%m-%Y"),self.vendor_id]
        mycursor.execute(sql, value)
        mydb.commit()
        self.get_delivery(1)
        self.popup.dismiss()


    def get_approval(self,arg):
        if self.vendor_id == 0:
            container = self.ids.approval_preview
            container.clear_widgets()
        else:
            details = BoxLayout(size_hint_y=.9, pos_hint={'top': 1})
            container = self.ids.approval_preview
            container.clear_widgets()
            btn_add = WrappedButton(
                text=" Add New Approval",
                size_hint=(1, None), height=Window.height / 9, font_size=40,
                background_color=(0.06, .47, .47, 1),
                background_normal="", on_release=partial(self.add_new_approval))
            container.add_widget(btn_add)
            container.add_widget(details)
            # products_container.add_widget(details)
            # self.popup = Popup(title='Vendor',
            #                    content=details,
            #                    size_hint=(.8, .7))
            # self.popup.open()

            details_1 = BoxLayout(size_hint=(1, 1), orientation="vertical")
            details.add_widget(details_1)
            root = ScrollView(size_hint=(1, 1),
                              pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
            details_1.add_widget(root)
            layout = GridLayout(cols=3, spacing=10,
                                size_hint=(1, None))
            layout.bind(minimum_height=layout.setter('height'))
            root.add_widget(layout)

            mydb = DbConnect().db
            mycursor = mydb.cursor()
            sql = "select * from approval where vendor_id=?"
            value = [self.vendor_id]
            mycursor.execute(sql, value)
            code = mycursor.fetchall()

            if len(code) > 0:
                for i in code:
                    item = str(i[1])
                    if len(item) > 10:
                        item = item[:10] + "..."
                    des = str(i[2])
                    if len(des) > 13:
                        des = des[:13] + "..."
                        if "\n" in des:

                            des = des[:des.find("\n")] + "..."
                    dt = str(i[4])
                    btn = WrappedButton(
                        text=" Item:  " + str(item) + "\n Date: " + str(dt) + "\n Description: " + str(des),
                        size_hint=(.7, None), height=Window.height / 3, font_size=40,
                         background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.show_approval, str(i[0])))
                    edit_btn = WrappedButton(
                        text="\n Edit" + "\n  ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.edit_approval, str(i[0])))
                    dlt_btn = WrappedButton(
                        text="\n Dlt" + "\n  ",
                        size_hint=(.1, None), height=Window.height / 6, font_size=40,
                        background_color=(0.06, .47, .47, 1),
                        background_normal="", on_release=partial(self.dlt_approval, str(i[0])))
                    layout.add_widget(btn)
                    layout.add_widget(edit_btn)
                    layout.add_widget(dlt_btn)
    def show_approval(self,id,arg):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Approval Details',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select * from approval where id=?"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()
        for i in code:
            item_label = Label(text="Item", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

            item_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                   hint_text="Metal",text=str(i[1]),disabled = True)

            des_label = Label(text="Description", size_hint_y=.40, color=(0.06, 0.45, .45, 1))
            des_text = TextInput(write_tab=False, multiline=True, padding=[5, 0, 0, 0], size_hint_y=.40,
                                    hint_text="Enter weight",text=str(i[2]),disabled = True)


            btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))

            details_label.add_widget(item_label)

            details_label.add_widget(des_label)


            details_label.add_widget(btn_close)

            details_text.add_widget(item_text)

            details_text.add_widget(des_text)


            #details_text.add_widget(btn_add)

            details.add_widget(details_label)
            details.add_widget(details_text)

    def edit_approval(self,id,arg):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Edit Approval',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")
        mydb = DbConnect().db
        mycursor = mydb.cursor()
        sql = "select * from approval where id=?"
        value = [id]
        mycursor.execute(sql, value)
        code = mycursor.fetchall()
        for i in code:
            item_label = Label(text="Item", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

            item_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                   hint_text="Metal",text=str(i[1]))

            des_label = Label(text="Description", size_hint_y=.40, color=(0.06, 0.45, .45, 1))
            des_text = TextInput(write_tab=False, multiline=True, padding=[5, 0, 0, 0], size_hint_y=.40,
                                    hint_text="Enter weight",text=str(i[2]))


            btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
            btn_add = Button(text="Update Approval", size_hint_y=.20, color=(1, 1, 1, 1),
                             on_release=lambda x: self.edit_approval_exec(item_text.text,

                                                                   des_text.text,

                                                                         str(i[0])
                                                                   ))
            details_label.add_widget(item_label)

            details_label.add_widget(des_label)


            details_label.add_widget(btn_close)

            details_text.add_widget(item_text)

            details_text.add_widget(des_text)


            details_text.add_widget(btn_add)

            details.add_widget(details_label)
            details.add_widget(details_text)

    def edit_approval_exec(self, item,des,id):

        if item == "" or des == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All Fields "
                                              "Required[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "update approval set item=?,description=? where id=?"

            value = [item,des, id]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_approval(1)
        # self.ids.products.remove_widget(id_form.parent)
    def dlt_approval(self,id,arg1):
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1}, orientation="vertical")
        # products_container.add_widget(details)
        self.popup = Popup(title='Delete Approval Confirmation!!',
                           content=details,
                           size_hint=(.8, .25))

        self.popup.open()
        lb4 = Label(text='[color=ff3333]Are You Sure to Delete?[/color][color=3333ff][/color]'+"\n\n",
                    markup=True, size_hint=(.8, .4))
        details.add_widget(lb4)
        details_action = BoxLayout(size_hint=(1, .2))
        details.add_widget(details_action)
        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint=(.5,1), color=(1, 1, 1, 1))
        btn_dlt = Button(text="Delete Approval", size_hint=(.5,1), color=(1, 1, 1, 1),
                         on_release=lambda x: self.delete_approval_exec(
                                                                     id
                                                                     ))
        details_action.add_widget(btn_close)
        details_action.add_widget(btn_dlt)

    def delete_approval_exec(self,id):
        self.popup.dismiss()
        mydb = DbConnect().db
        mycursor = mydb.cursor()

        sql = "delete from approval where id=?"

        value = [id]
        mycursor.execute(sql, value)
        mydb.commit()
        self.get_approval(1)


    def add_new_vendor(self):

        #products_container = self.ids.products
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Add New Vendor',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1),  orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1),  orientation="vertical")

        fname_label = Label(text="First Name", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

        fname_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                               hint_text="Enter Name")

        address_label = Label(text="Address", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        address_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter Address")
        contact_label = Label(text="Contact", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        contact_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter Contact Number")


        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
        btn_add = Button(text="Add Vendor", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_vendor(fname_text.text,

                                                                address_text.text,
                                                                contact_text.text,
                                                                ))
        details_label.add_widget(fname_label)

        details_label.add_widget(address_label)
        details_label.add_widget(contact_label)

        details_label.add_widget(btn_close)

        details_text.add_widget(fname_text)

        details_text.add_widget(address_text)
        details_text.add_widget(contact_text)

        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)

    def add_vendor(self, fname, address, contact):

        if fname == ""  or address == "" or contact == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All Fields "
                                              "Required[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "insert into vendor(name," \
                  "address,contact) " \
                  "values(?,?,?)"

            value = [fname, address, contact]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
        #self.ids.products.remove_widget(id_form.parent)

    def add_new_booking(self,arg):

        #products_container = self.ids.products
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Add New Booking',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1),  orientation="vertical")

        metal_label = Label(text="Metal", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

        metal_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                               hint_text="Metal")

        weight_label = Label(text="Weight", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        weight_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter weight")
        rate_label = Label(text="Rate", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        rate_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter Rate")


        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
        btn_add = Button(text="Add Booking", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_booking(metal_text.text,

                                                                weight_text.text,
                                                                rate_text.text,
                                                                ))
        details_label.add_widget(metal_label)

        details_label.add_widget(weight_label)
        details_label.add_widget(rate_label)

        details_label.add_widget(btn_close)

        details_text.add_widget(metal_text)

        details_text.add_widget(weight_text)
        details_text.add_widget(rate_text)

        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)

    def add_booking(self, metal, weight, rate):
        f_weight = "wrong"

        f_rate = "wrong"
        # f_date = "wrong"

        try:
            f_weight = round(float(weight), 4)
            f_rate = round(float(rate), 2)

            # f_date = datetime.strptime(date, '%d-%m-%Y')

        except:
            pass
        if weight == "" or rate == "":
            f_weight = "wrong"

            f_rate = "wrong"

        if metal == "" or f_rate == "wrong" or f_weight == "wrong":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Enter Correct Number \nor Metal[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "insert into book(metal," \
                  "weight,rate,vendor_id,date) " \
                  "values(?,?,?,?,?)"

            value = [metal, weight, rate,self.vendor_id,datetime.now().strftime("%d-%m-%Y")]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_booking(1)
        #self.ids.products.remove_widget(id_form.parent)

    def add_new_delivery(self,arg):

        #products_container = self.ids.products
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Add New Delivery',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")

        metal_label = Label(text="Metal", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

        metal_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                               hint_text="Metal")

        weight_label = Label(text="Weight", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        weight_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter weight")
        rate_label = Label(text="Rate", size_hint_y=.20, color=(0.06, 0.45, .45, 1))
        rate_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                                 hint_text="Enter Rate")


        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
        btn_add = Button(text="Add Delivery", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_delivery(metal_text.text,

                                                                weight_text.text,
                                                                rate_text.text,
                                                                ))
        details_label.add_widget(metal_label)

        details_label.add_widget(weight_label)
        details_label.add_widget(rate_label)

        details_label.add_widget(btn_close)

        details_text.add_widget(metal_text)

        details_text.add_widget(weight_text)
        details_text.add_widget(rate_text)

        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)

    def add_delivery(self, metal, weight, rate):
        f_weight = "wrong"

        f_rate = "wrong"
        #f_date = "wrong"

        try:
            f_weight = round(float(weight), 4)
            f_rate = round(float(rate), 2)

            #f_date = datetime.strptime(date, '%d-%m-%Y')

        except:
            pass
        if weight == "" or rate == "":
            f_weight = "wrong"

            f_rate = "wrong"

        if metal == "" or f_rate == "wrong" or f_weight == "wrong":
            self.notify.add_widget(Label(text="[color=#FF0000][b]Enter Correct Number \nor Metal[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)


        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "insert into delivery(metal," \
                  "weight,rate,vendor_id,date) " \
                  "values(?,?,?,?,?)"

            value = [metal, weight, rate,self.vendor_id,datetime.now().strftime("%d-%m-%Y")]
            mycursor.execute(sql, value)
            mydb.commit()
            sql = "select max(id) from delivery"
            mycursor.execute(sql)
            code = mycursor.fetchall()
            id = code[0][0]
            sql = "insert into payment(delivery_id," \
                  "amount,date,vendor_id) " \
                  "values(?,?,?,?)"
            value = [id, int(round(float(weight),4)*round(float(rate),4)),  datetime.now().strftime("%d-%m-%Y"),self.vendor_id]
            mycursor.execute(sql, value)
            mydb.commit()



            self.popup.dismiss()
            self.get_delivery(1)
        #self.ids.products.remove_widget(id_form.parent)

    def add_new_approval(self,arg):

        #products_container = self.ids.products
        details = BoxLayout(size_hint_y=1, pos_hint={'top': 1})
        # products_container.add_widget(details)
        self.popup = Popup(title='Add New Approval',
                           content=details,
                           size_hint=(.8, .4))

        self.popup.open()

        details_label = BoxLayout(size_hint=(.3,1), orientation="vertical")
        details_text = BoxLayout(size_hint=(.7,1), orientation="vertical")

        item_label = Label(text="Item", size_hint_y=.20, color=(0.06, 0.45, .45, 1), halign="left")

        item_text = TextInput(write_tab=False, multiline=False, padding=[5, 0, 0, 0], size_hint_y=.20,
                               hint_text="Item")

        des_label = Label(text="Description", size_hint_y=.40, color=(0.06, 0.45, .45, 1))
        des_text = TextInput(write_tab=False, multiline=True, padding=[5, 0, 0, 0], size_hint_y=.40,
                                 hint_text="Enter Description")



        btn_close = Button(text="Close", on_release=self.popup.dismiss, size_hint_y=.20, color=(1, 1, 1, 1))
        btn_add = Button(text="Add Approval", size_hint_y=.20, color=(1, 1, 1, 1),
                         on_release=lambda x: self.add_approval(item_text.text,

                                                                des_text.text,

                                                                ))
        details_label.add_widget(item_label)

        details_label.add_widget(des_label)


        details_label.add_widget(btn_close)

        details_text.add_widget(item_text)

        details_text.add_widget(des_text)


        details_text.add_widget(btn_add)

        details.add_widget(details_label)
        details.add_widget(details_text)

    def add_approval(self, item, des):

        if item == ""  or des == "":
            self.notify.add_widget(Label(text="[color=#FF0000][b]All Fields "
                                              "Required[/b][/color]",
                                         markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            mydb = DbConnect().db
            mycursor = mydb.cursor()

            sql = "insert into approval(item," \
                  "description,vendor_id,date) " \
                  "values(?,?,?,?)"

            value = [item, des,self.vendor_id,datetime.now().strftime("%d-%m-%Y")]
            mycursor.execute(sql, value)
            mydb.commit()
            self.popup.dismiss()
            self.get_approval(1)
        #self.ids.products.remove_widget(id_form.parent)


class OperatorApp(App):
    date_c = 0

    # logged_in_user_id = 0

    def build(self):
        return OperatorWindow()


if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()
