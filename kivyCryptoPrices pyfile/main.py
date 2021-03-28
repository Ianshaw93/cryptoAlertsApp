from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty #links properties from kivy file to python code
#from kivy.uix.popup import Popup
#from kivy.uix.label import Label
from kivy.uix.widget import Widget
#from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
import time

import CoinGecko
from CoinGecko import GetMarketChart
from CoinGecko import GetCryptoFiatPrice

#from database import Database

# Set the app size
Window.size = (500, 700)

# #Designate the .kv design file
# Builder.load_file('crypto.kv')
time_date, price = GetMarketChart()
# print(time_date)
# print(price)
#print(GetMarketChart())

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)      # this is only for if kivy code goes in the py file
        self.user_price = None #self to use anywhere within programme
        self.orientation = 'horizontal'

        bad_graph_btn = Button(text="bad graph")
        bad_graph_btn.bind(on_release=self.bad_handle_plot)

        # good_graph_btn = Button(text="good graph")
        # good_graph_btn.bind(on_release=self.good_handle_plot)

        self.add_widget(bad_graph_btn)
        # # self.add_widget(good_graph_btn)
        #
        # # self.ticker_list = ['pays', 'pi', 'amd', 'cde', 'x', "msft"]
        #
        # tickers to show on the plot
        self.tickers_on_plot = ['bitcoin'] #get from coin gecko

        # red, yellow, purple, light blue, green | line colors for plot
        self.plot_colors = [[1, 1, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1], [0.5, .75, .9, 1], [0, 1, 0.3, 1]]

        # holds y values for the plot
        self.plot_price = price

        # x-axis of plot
        self.plot_dates = time_date

    def bad_handle_plot(self, instance):
        mainview = ModalView(size_hint=(0.75, 0.75))
        # self.cols = 1
        # self.rows = 2
        # self.clear_widgets()
        Grid = GridLayout(rows = 2, cols = 1, padding=[15, 15, 15, 30])  # left, top, right, bot

        # # make a the left side (will contain a 2 other layouts)
        # alarm_box = BoxLayout(orientation="horizontal", size_hint_x=1, size_hint_y=0.25)
        #
        # # will contain the alarms below graph
        # scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)

        # right side that will be graph - recall I make my own x-axis
        rightbox = BoxLayout(orientation="vertical", size_hint_y=0.5, size_hint_x=.6)

        # x-axis for graph (right side of modalview)
        # rightbotgrid = GridLayout(rows=1, cols=24)

        # make invisible labels for formatting
        # this is an invsible widget just to make things fit
        #rightbotgrid.add_widget(Label(size_hint_x=1 / 13))

        #show live price below chart
        # price_box = BoxLayout(orientation='vertical', size_hint_x=1)
        # self.current_price = CoinGecko.GetCryptoFiatPrice()
        # live_price_text = 'The current price is $' + str(self.current_price)
        # live_price_label = Label(text = live_price_text, size_hint_x=2)
        # price_box.add_widget(live_price_label)

        # will contain the alarms below graph
        alarm_box2 = GridLayout(cols = 2, size_hint_x=1, size_hint_y=.5)
        #first row: price
        self.current_price = CoinGecko.GetCryptoFiatPrice()
        live_price_text = 'The current price is $' + str(self.current_price)
        live_price_label = Label(text = "", size_hint_x=.5)
        dummy_label = Label(text = live_price_text, size_hint_x=.5)
        alarm_box2.add_widget(live_price_label)
        alarm_box2.add_widget(dummy_label)
        #second row: alarm input
        set_alarm_label = Label(text = 'Set Target Price: ', size_hint_x = 0.5)
        alarm_textinput = TextInput(multiline=False, text=" ", size_hint_x=0.5)
        alarm_textinput.bind(text = self.on_text)
        alarm_box2.add_widget(set_alarm_label)
        alarm_box2.add_widget(alarm_textinput)
        #third row: set alert buttons
        alarm_button_less_than = Button(text="<", size_hint_x=1)
        alarm_button_more_than = Button(text=">", size_hint_x=1)
        alarm_box2.add_widget(alarm_button_less_than)
        alarm_box2.add_widget(alarm_button_more_than)
        alarm_button_less_than.bind(on_release=self.alert_callback)
        # alarm_box2.bind(on_release=self.set_alert)



        graph = CoinGecko.make_plot(self.plot_price, self.plot_dates, self.tickers_on_plot,
                  self.plot_colors)

        # make the actual plot
        rightbox.add_widget(graph)



        # add the x-axis
        # rightbox.add_widget(rightbotgrid)
        #rightbox.add_widget(Label(text="Dates", size_hint_y=0.05))

        # alarm_box.add_widget(scroll)
        #alarm_box2.add_widget(scroll2)


        Grid.add_widget(rightbox)
        Grid.add_widget(alarm_box2)


        mainview.add_widget(Grid)

        mainview.open()

        # view.add_widget(graph)
        # view.open()

    # def bitcoinprice(self):
    #     #if bitcoinprice.bind(on_press):
    #     self.ids.price.text = '$' + str(GetCryptoFiatPrice()['bitcoin']['usd']) #dry
    #
    # def dotprice(self):
    #     self.ids.price.text = '$' + str(GetCryptoFiatPrice()['polkadot']['usd'])
    #
    # def adaprice(self):
    #     self.ids.price.text = '$' + str(GetCryptoFiatPrice()['cardano']['usd'])

    def alert_callback(self, event):
        # print(self.user_price)
        # self.current_price = 40000
        # self.current_price = CoinGecko.GetCryptoFiatPrice()
        # print(zip(CoinGecko.GetCryptoFiatPrice()))
        # print((CoinGecko.GetCryptoFiatPrice(['bitcoin']['usd'])))
        while self.user_price < self.current_price:
            time.sleep(10)
            self.current_price -= 10000 #for test
        #add popup
        content=GridLayout(cols = 1, padding = 10)
        content.add_widget(Label(text='Price is less than $'+ str(self.user_price)))
        popup = Popup(title = 'Bitcoin Price Alert',
                      size_hint=(0.5, 0.3), content=content)
        popup.open()

    def on_text(self, value, second_value):
        # print(second_value)

        try:
            self.user_price = int(second_value)
        except:
            print(second_value) #just for debugging



class CryptoApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    CryptoApp().run()

