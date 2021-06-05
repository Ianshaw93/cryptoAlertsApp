import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from database import DataBase

import os
import coin_gecko
from coin_gecko import get_market_chart
import parsedatabase
from coin_gecko import get_crypto_fiat_price

# kivy.require("1.10.1")

# Set the app size
Window.size = (500, 700)
time_date, price = get_market_chart()

# class AlertRecycleView(RecycleView):
#     def __init__(self, **kwargs):
#         super(AlertRecycleView, self).__init__(**kwargs)
#         self.data = [45, 23, 11, 8]

# class AlertRecycleView(RecycleView):
#     def __init__(self, **kwargs):
#         super(AlertRecycleView, self).__init__(**kwargs)
#         self.data = [45, 23, 11, 8]


# This class is an improved version of Label
# Kivy does not provide scrollable label, so we need to create one
class ScrollableLabel(ScrollView): # no self required to send to this class
    text = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow more than one widget to be added
        # Therefore, one layout with two widgets inside it
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)
        # Two widgets needed - Label for alert history and 'artificial' widget below
        self.alert_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()
        self.layout.add_widget(self.alert_history)
        self.layout.add_widget(self.scroll_to_point)

    # add new item to alerts log
    def update_alert_history(self, alarm_figure):
        # First add new line and alert price figure to log
        self.alert_history.text += os.linesep + "$" + str(alarm_figure)
        self.layout.height = self.alert_history.texture_size[1] + 15
        self.alert_history.height = self.alert_history.texture_size[1]
        self.alert_history.text_size = (self.alert_history.width * 0.98, None)
        self.scroll_to(self.scroll_to_point)

# Home page with selection of crypto currencies i.e. coins
class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.user_price = None
        self.orientation = 'vertical'
        self.current_coin = ['']
        self.graph_period = 1
        self.alerts_log = []
        self.output_content = []
        self.alert_symbol_log = []
        self.alerts_log_scroll = None
        self.new_alerts_scrollable_label = None
        self.new_alerts_scrollable_label = None
        self.coin_alerts_less_than = {}
        self.coin_alerts_more_than = {}
        self.alert_symbol = ""
        popup_message = ""
        self.popup_message = popup_message
        # later in dev the coin names will be read from API
        bitcoin_page_button = Button(text='Bitcoin')
        cardano_page_button = Button(text='Cardano')
        ethereum_page_button = Button(text='Ethereum')
        # add bind to coin functions to set currency to the particular coin,
        # this is then used in the graph function via Coin gecko function
        bitcoin_page_button.bind(on_release=self.bitcoin_alerts)
        cardano_page_button.bind(on_release=self.cardano_alerts)
        ethereum_page_button.bind(on_release=self.ethereum_alerts)
        self.add_widget(bitcoin_page_button)
        self.add_widget(cardano_page_button)
        self.add_widget(ethereum_page_button)
        # tickers to show on the plot
        self.tickers_on_plot = self.current_coin
        # red, yellow, purple, light blue, green | line colors for plot
        self.plot_colors = [[1, 1, 0, 1],
                            [1, 0, 0, 1],
                            [1, 0, 1, 1],
                            [0.5, .75, .9, 1],
                            [0, 1, 0.3, 1]
        ]

    # class for particular coin pages -
    # allows user to set alerts and review price
    def coin_page(self):
        mainview = ModalView(size_hint=(0.75, 0.75))
        grid = GridLayout(
                rows=2, cols=1,
                padding=[10, 15, 10, 30]  # left, top, right, bottom
        )
        # Area to contain price graphs located at the top half of the screen.
        graph_box = BoxLayout(
                orientation="vertical",
                size_hint_y=0.5, size_hint_x=.6
        )
        # Will contain the alerts below graph - once user sets them
        alarm_box = GridLayout(
                cols=2,
                size_hint_x=1, size_hint_y=.5
        )
        # First row of alerts box contains current price.
        self.current_price = coin_gecko.get_crypto_fiat_price(
                cryptoCurrency=self.current_coin
        )
        live_price_text = 'The current price is $' \
                          + str(self.current_price)
        live_price_label = Label(text="", size_hint_x=.5)
        dummy_label = Label(text=live_price_text, size_hint_x=.5)
        alarm_box.add_widget(live_price_label)
        alarm_box.add_widget(dummy_label)
        # Second row of alerts box contains alerts input box
        set_alarm_label = Label(text='Set Target Price: ', size_hint_x=0.5)
        self.alarm_textinput = TextInput(
                multiline=False, size_hint_x=0.5
        )
        # method actioned to check text input
        self.alarm_textinput.bind(text=self.on_text)
        alarm_box.add_widget(set_alarm_label)
        alarm_box.add_widget(self.alarm_textinput)
        # Third row of alerts box to contain buttons to set alerts
        alarm_button_less_than = Button(text="<", size_hint_x=1)
        alarm_button_more_than = Button(text=">", size_hint_x=1)
        alarm_box.add_widget(alarm_button_less_than)
        alarm_box.add_widget(alarm_button_more_than)
        # methods called on press of third row buttons, and then alerts added to log
        alarm_button_less_than.bind(on_release=self.alert_callback_less_than)
        alarm_button_more_than.bind(on_release=self.alert_callback_more_than)
        # Fourth row of alerts box will contain the alerts log.
        # self.scroll_label = ScrollableLabel(size_hint_x=1) #shown as self.history in sentdex tutorial
        # how to use self for input/label while not using self for old alerts
        # existing alerts
        scrollable_label = ScrollableLabel(size_hint_x=1) # existing alerts
        alarm_box.add_widget(scrollable_label)
        # new alerts
        self.new_alerts_scrollable_label = ScrollableLabel(size_hint_x=1)
        alarm_box.add_widget(self.new_alerts_scrollable_label)
        self.price_chart()
        # Fourth row of alerts box continued
        graph_tabs = TabbedPanel(pos_hint={'center_x': .5, 'center_y': 1})
        graph_tabs.default_tab_text = '24hr'
        graph_tabs.default_tab.bind = self.one_day_chart()
        graph_tabs.default_tab_content = self.graph
        # graph title
        seven_days_tab = TabbedPanelHeader(text='7 days')
        seven_days_tab.bind = self.seven_day_chart()
        seven_days_tab.content = self.graph
        graph_tabs.add_widget(seven_days_tab)
        # make the actual plots
        graph_box.add_widget(graph_tabs)
        grid.add_widget(graph_box)
        grid.add_widget(alarm_box)
        # grid.add_widget(scrollable_label)
        mainview.add_widget(grid)
        mainview.open()
        parsedatabase.check_alerts(scrollable_label)


    def price_chart(self):
        self.plot_dates, self.plot_price = coin_gecko.get_market_chart(
                cryptoCurrency=self.current_coin, fiatCurrency='usd',
                chart_period=self.graph_period
        )
        self.graph = coin_gecko.make_plot(
                self.plot_price, self.plot_dates, self.tickers_on_plot,
                self.plot_colors, xlabel=self.current_coin.capitalize()
        )

    def one_day_chart(self):
        self.graph_period = 1
        print(self.graph_period)
        self.price_chart()

    def seven_day_chart(self):
        self.graph_period = 7
        print(self.graph_period)
        self.price_chart()

    def bitcoin_alerts(self, event):
        self.current_coin = 'bitcoin'
        self.coin_page()
        # parsedatabase.check_alerts()

    def cardano_alerts(self, event):
        self.current_coin = 'cardano'
        self.coin_page()

    def ethereum_alerts(self, event):
        self.current_coin = 'ethereum'
        self.coin_page()

    def alert_callback_less_than(self, event):
        self.alert_symbol = 'l'
        self.add_item()

    def alert_callback_more_than(self, event):
        self.alert_symbol = 'm'
        self.add_item()

    @staticmethod
    def alert_popup(popup_message):
        print('popup activated')
        # add popup when target criteria met -
        # perhaps change to email notification in the future
        content = GridLayout(cols=1, padding=10) # not being added after going to parsepage??
        content.add_widget(Label(text=popup_message))
        # content.add_widget(Label(
        #         text='Price is ' + self.alert_symbol
        #         + ' $' + str(self.user_price)
        # ))
        # popup = Popup(
        #         title=self.current_coin.capitalize()
        #         + ' Price Alert',
        #         size_hint=(0.5, 0.3), content=content
        # )
        popup = Popup(size_hint=(0.8, 0.3), content=content)
        popup.open()

    def add_item(self, *args):
        if self.alarm_textinput.text != "":
            price_target = self.alarm_textinput.text
            coin = self.current_coin
            symbol = self.alert_symbol
            db.add_alert(coin, symbol, price_target)
            # add other formatted constraints - only valid numbers etc
            # Get text and clear input box
            # alarm figure similar to message = self.new_message.text # in sentdex tutorial
            alarm_figure = self.alarm_textinput.text
            # clear text inputbox
            self.reset()
            self.new_alerts_scrollable_label.update_alert_history(alarm_figure)
            # need to send scrollable_label into method??
            # scrollable_label.update_alert_history(alarm_figure) # was self.scroll_label
            self.output_content.append(alarm_figure)
            self.alert_symbol_log.append(self.alert_symbol)

            # scrollable_label.text += alarm_figure
            self.new_alerts_scrollable_label.text += alarm_figure
            print(self.output_content, self.alert_symbol_log)
        else: print("not working")

    def reset(self):
        self.alarm_textinput.text = ""


    def on_text(self, value, second_value):
        try:
            self.user_price = int(second_value)
        except:
            print(second_value)  # just for debugging

db = DataBase("alerts.txt")

class CryptoApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    CryptoApp().run()

