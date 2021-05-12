# cryptoAlertsApp
Crypto Currency Price Alerts App with the GUI created using Kivy and information gathered using the Coingecko API.

This app is still in development.

Users will be able to view current prices and market charts for cryptocurrencies and add alerts for when price is higher/lower than user defined price.  A notification is sent to the user on their device when target criteria is met.

# App so Far
From the main screen users will be able to navigate to any of the crytocurrency pages.  A video demo of the Bitcoin page is shown in the link directly below:

Video demo of Bitcoin page: https://user-images.githubusercontent.com/76686112/112745618-b7bc2700-8fa1-11eb-8623-0170ce87ad82.mp4

Screen grab of Bitcoin page with 60000 entered by user for test.

![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FIanshaw93%2FD8IBW_gntw.png?alt=media&token=c844a036-821f-415e-bb71-1a780aade1d2)


For the test the user selects the less than button and the screen grab below shows the corresponding alert notification that the market price is less than the target price.

![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FIanshaw93%2FOF2iZNm8qi.png?alt=media&token=233dc919-852b-4cb1-822b-de34bd7bf153)

Since this video the app has advanced, now the user can select 24hr or 7 day chart for the coin; and the alerts are shown at the bottom of the screen, see photo below for Cardano.

![image](https://user-images.githubusercontent.com/76686112/118045487-dfa7f400-b36f-11eb-9f5b-e2f26b0fe71c.png)

![image](https://user-images.githubusercontent.com/76686112/118045691-28f84380-b370-11eb-8239-a022047a3889.png)


The prices are stored in a database and a notification is shown to the user when the alert condition is reached for any of the alerts.

# Future Features
The database will be hosted remotely to allow notifications to be sent 24/7 to user; main menu will show the 24 hr chart,current price for each coin and whether the user has any alarms configured for that particular coin. 

# What I Learned

* How to extract data using an API
* How to call a separate python file and it's functions into a python file
* Creating graphs in matplotlib and then converting for kivy
* Writing to and reading from a database
* How to use source code through the declaration and usages
