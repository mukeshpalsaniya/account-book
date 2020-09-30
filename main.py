from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from signin.signin import SigninWindow

#from till_operator.till_operator import OperatorWindow

Builder.load_string("""

<MainWindow>:
    id:main_win
    ScreenManager:
        id:scrn_mngr_main
        Screen:
            id: scrn_si
            name: "scrn_si"
        Screen:
            id: scrn_admin
            name: "scrn_admin"
        Screen:
            id: scrn_op
            name:"scrn_op"

        """)


class MainWindow(BoxLayout):
    #admin_widget = AdminWindow()
    signin_widget = SigninWindow()
    #operator_widget = OperatorWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        #self.ids.scrn_admin.add_widget(self.admin_widget)
        #self.ids.scrn_op.add_widget(self.operator_widget)



class MainApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    MainApp().run()