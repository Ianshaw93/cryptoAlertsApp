from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty #links properties from kivy file to python code
#from kivy.uix.popup import Popup
#from kivy.uix.label import Label
from kivy.uix.widget import Widget
#from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window

#from database import Database

# Set the app size
Window.size = (500, 700)

#Designate the .kv design file
Builder.load_file('crypto.kv')

class MyLayout(Widget):
    print('25')
    def clear(self):
        print('24,000')
        self.ids.price.text = " jdkljfkldj"


class CryptoApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    CryptoApp().run()