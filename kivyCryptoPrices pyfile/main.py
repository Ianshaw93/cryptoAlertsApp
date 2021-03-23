from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty #links properties from kivy file to python code
#from kivy.uix.popup import Popup
#from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

#import py file with functions for crypto API
import CoinGecko


# Set the app size
Window.size = (500, 700)

time_date, price = GetMarketChart()

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)      # this is only for if kivy code goes in the py file

        self.orientation = 'horizontal'

        bad_graph_btn = Button(text="bad graph")
        bad_graph_btn.bind(on_release=self.bad_handle_plot)

        self.add_widget(bad_graph_btn)

        # tickers to show on the plot
        self.tickers_on_plot = ['bitcoin'] 

        # red, yellow, purple, light blue, green | line colors for plot
        self.plot_colors = [[1, 1, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1], [0.5, .75, .9, 1], [0, 1, 0.3, 1]]

        # holds y values for the plot
        self.plot_price = price

        # x-axis of plot
        self.plot_dates = time_date

    def bad_handle_plot(self, instance):
        #create a pop out window for alerts window
        mainview = ModalView(size_hint=(0.75, 0.75))
        Grid = GridLayout(rows = 2, cols = 1, padding=[15, 15, 15, 30])  # left, top, right, bot

        # create box for pricing graph
        rightbox = BoxLayout(orientation="vertical", size_hint_y=0.5, size_hint_x=.6)

        # will contain the alarms below graph
        alarm_box2 = BoxLayout(orientation="vertical", size_hint_x=1, size_hint_y=.5)
        alarm_box2.add_widget(Label(text="alarms", size_hint_x=1))
        alarm_box2.add_widget(Button(text = "alarms", size_hint_x=1))

        # make the actual plot
        rightbox.add_widget(CoinGecko.make_plot(self.plot_price, self.plot_dates, self.tickers_on_plot,
                    self.plot_colors))

        # box.add_widget(alarm_box)
        Grid.add_widget(rightbox)
        Grid.add_widget(alarm_box2)


        mainview.add_widget(Grid)

        mainview.open()

class CryptoApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    CryptoApp().run()

