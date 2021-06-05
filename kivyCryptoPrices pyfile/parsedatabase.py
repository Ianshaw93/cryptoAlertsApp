import coin_gecko
from main import MainPage
from main import ScrollableLabel
import database as db

def check_alerts(scrollable_label):
    # open txt file
    file = open('alerts.txt', 'r')


    # split line into an array
    for line in file:
        alerts = line.split(";")
        # price_target, coin, symbol = line.strip().split(";")
        # set up the data to extract
        price_target = float(alerts[0])
        coin = alerts[1]
        symbol = alerts[2].strip() # remove the /n from symbol

        # should be moved to a separate method for all processes to be repeated at regular time intervals
        # call coin gecko to get price of coin, not efficient to run every line
        price_current = coin_gecko.get_crypto_fiat_price(
                cryptoCurrency=coin
        )
        
        # send all alerts of a certain coin to the scrollable view on the coin page
        # receive current_coin from main.py in the future
        current_coin = 'bitcoin' # test
        if coin == current_coin:
            scrollable_label.update_alert_history(price_target)
            # SendAlerts(price_target)
            # try calling class not method
            # ScrollableLabel.update_alert_history(self, alarm_figure=price_target)
            # ScrollableLabel.update_alert_history(alarm_figure=price_target)

            print('scroll')

        if symbol == 'l'and price_current < price_target:
            # alert_popup()
            print(f"{coin.capitalize()} price alert! Current price is less than ${str(price_target)}!")
            # how to send pop_up message to popup in main.py?
            popup_message = str(f"{coin.capitalize()} price alert! Current price is less than ${str(price_target)}!")
            MainPage.alert_popup(popup_message)
            # db.remove_alert
            # main_py = main.MainPage(popup_message)
            # main_py.alert_popup()
            # else: print('less than target not reached')
        if symbol == 'm' and price_current > price_target:
            # alert_popup()
            print(f"{coin.capitalize()} price alert! Current price is more than ${str(price_target)}!")
        #     else: print('more than target not reached')

        # print(str(price_target) + 'vs' + str(price_current))  # test

    file.close()

# create an init class & method to send instance to scrollable label
# class SendAlerts():
#     def __init__(self, price_target):
#         # send all alerts of a certain coin to the scrollable view on the coin page
#         # try calling class not method # scrollable_label is instance in this case
#         # scrollable_label = ScrollableLabel() # when the init of class is called
#         scrollable_label.update_alert_history(alarm_figure=price_target)
#         print("it's working")




# check_alerts()
