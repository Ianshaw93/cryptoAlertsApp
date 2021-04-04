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
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

from kivy.uix.recycleview import RecycleView
import time

import coin_gecko
from coin_gecko import get_market_chart
from coin_gecko import get_crypto_fiat_price

# Set the app size
Window.size = (500, 700)
time_date, price = get_market_chart()

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.user_price = None
        self.orientation = 'horizontal'
        self.current_coin = ['']
        self.graph_period = 1
        #later in dev the coin names will be read from API
        bitcoin_page_button = Button(text='Bitcoin')
        #add bind to bitcoin function to set currency to btc,
        #this is then used in the graph function via Coingecko function
        bitcoin_page_button.bind(on_release=self.bitcoin_alerts)
        self.add_widget(bitcoin_page_button)
        # tickers to show on the plot
        self.tickers_on_plot = self.current_coin
        # red, yellow, purple, light blue, green | line colors for plot
        self.plot_colors = [[1, 1, 0, 1],
                            [1, 0, 0, 1],
                            [1, 0, 1, 1],
                            [0.5, .75, .9, 1],
                            [0, 1, 0.3, 1]
        ]
    def coin_page(self):
        mainview = ModalView(size_hint=(0.75, 0.75))
        grid = GridLayout(
                rows = 2, cols = 1,
                padding=[15, 15, 15, 30]  # left, top, right, bottom
        )
        self.alerts_log = []
        self.output_content = []
        # Area to contain price graphs located at the top half of the screen.
        graph_box = BoxLayout(
                orientation="vertical",
                size_hint_y=0.5, size_hint_x=.6
        )
        # Will contain the alerts below graph
        alarm_box = GridLayout(
                cols = 2,
                size_hint_x=1, size_hint_y=.5
        )
        # First row of alerts box to contain current price.
        self.current_price = coin_gecko.get_crypto_fiat_price(
                cryptoCurrency=self.current_coin
        )
        live_price_text = 'The current price is $' \
                          + str(self.current_price)
        live_price_label = Label(text = "", size_hint_x=.5)
        dummy_label = Label(text = live_price_text, size_hint_x=.5)
        alarm_box.add_widget(live_price_label)
        alarm_box.add_widget(dummy_label)
        # Second row of alerts box to contain alerts input box
        set_alarm_label = Label(text = 'Set Target Price: ', size_hint_x = 0.5)
        self.alarm_textinput = TextInput(
                multiline=False, text=" ", size_hint_x=0.5
        )
        self.alarm_textinput.bind(text = self.on_text)
        alarm_box.add_widget(set_alarm_label)
        alarm_box.add_widget(self.alarm_textinput)
        # Third row of alerts box to contain buttons to set alerts
        alarm_button_less_than = Button(text="<", size_hint_x=1)
        alarm_button_more_than = Button(text=">", size_hint_x=1)
        alarm_box.add_widget(alarm_button_less_than)
        alarm_box.add_widget(alarm_button_more_than)
        alarm_button_less_than.bind(on_release=self.add_item)
        alarm_button_more_than.bind(on_release=self.alert_callback_more_than)
        # Fourth row of alerts box will contain the alerts log.
        alerts_log_scroll = RecycleView(do_scroll_x=False, do_scroll_y=True)
        # how to update label to include target price?
        # self.alerts_log.append(self.user_price)
        # alerts_log_scroll.add_widget(Label(text = str(self.alerts_log)))
        alerts_log_scroll.add_widget(Label(text=("")))
        alarm_box.add_widget(alerts_log_scroll)

        self.price_chart()
        graph_tabs = TabbedPanel(pos_hint={'center_x': .5, 'center_y': 1})

        graph_tabs.default_tab_text = '24hr'
        graph_tabs.default_tab.bind = self.one_day_chart()
        graph_tabs.default_tab_content = self.graph
        #graph title
        seven_days_tab = TabbedPanelHeader(text='7 days')
        seven_days_tab.bind = self.seven_day_chart()
        seven_days_tab.content = self.graph

        graph_tabs.add_widget(seven_days_tab)

        # make the actual plots
        graph_box.add_widget(graph_tabs)

        grid.add_widget(graph_box)
        grid.add_widget(alarm_box)

        mainview.add_widget(grid)

        mainview.open()

    def price_chart(self):
        self.plot_dates, self.plot_price = coin_gecko.get_market_chart(
                cryptoCurrency=self.current_coin, fiatCurrency='usd',
                chart_period=self.graph_period
        )
        self.graph = coin_gecko.make_plot(
                self.plot_price, self.plot_dates,
                self.tickers_on_plot, self.plot_colors
        )

    def one_day_chart(self):
        self.graph_period = 1
        print(self.graph_period)
        self.price_chart()

    def seven_day_chart(self):
        self.graph_period = 7
        print(self.graph_period)
        self.price_chart()

    def bitcoin_alerts(self, instance):
        self.current_coin = 'bitcoin'
        self.coin_page()

        #ideally the less than and equal to should be dealt with in one function, not 2 with popup a separate function
    # def alert_callback(self, event, alert_symbol = 'more_than'):
    #     if alert_symbol == 'less_than':
    #         while self.user_price < self.current_price:
    #             time.sleep(10)
    #     else:
    #         while self.user_price > self.current_price:
    #             time.sleep(10)
    #         # self.current_price -= 10000 #for test

    def alert_callback_less_than(self, event):
        self.alert_symbol = 'less than'
        while self.user_price < self.current_price:
                time.sleep(10)
                # self.current_price -= 10000 #for test
        self.alert_popup()

    def alert_callback_more_than(self, event):
        self.alert_symbol = 'more than'
        while self.user_price > self.current_price:
            time.sleep(10)
        self.alert_popup()

    def alert_popup(self):
        #add popup when target criteria met - perhaps change to email in future
        content=GridLayout(cols = 1, padding = 10)
        content.add_widget(Label(
                text='Price is ' + self.alert_symbol
                + ' $'+ str(self.user_price)
        ))
        popup = Popup(
                title = self.current_coin.capitalize()
                + ' Price Alert',
                size_hint=(0.5, 0.3), content=content
        )
        popup.open()

    def add_item(self, event):
        #inputcontent
        if self.alarm_textinput.text != "":
            #add other formatted constraints - only valid numbers etc
            #output content
            formatted = f'\n{self.alarm_textinput.text}'
            self.output_content.append(formatted)
            # self.output_content.update()
            self.alarm_textinput.text = ""
            self.alerts_log_scroll.text = self.output_content

    def on_text(self, value, second_value):
        # print(second_value)
        # self.alerts_log = []
        try:
            self.user_price = int(second_value)
        except:
            print(second_value) #just for debugging
        #later have dictionary of logs for each coin
        # self.alerts_log_scroll.text = str(self.alerts_log)0
        # self.alerts_log.append(self.user_price)
        # return self.alerts_log

class CryptoApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    CryptoApp().run()

