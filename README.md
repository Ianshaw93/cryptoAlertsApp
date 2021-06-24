# cryptoAlertsApp
Crypto Currency Price Alerts App with the GUI created using Kivy and information gathered using the Coingecko API.

This app is still in development.

Users are able to view current prices and market charts for cryptocurrencies and add alerts for when price is higher/lower than user defined price.  A notification is sent to the user on their device when target criteria is met.

# App so Far
From the main screen users will be able to navigate to any of the crytocurrency pages.  A video demo of the Cardano page is shown in the link directly below.  

https://user-images.githubusercontent.com/76686112/121649680-b672a480-ca90-11eb-915a-c842a548c399.mp4

This demo shows previous user set alerts that are met (see screenshot of database).  The database is parsed and alerts that are met are notified to the used. 

![image](https://user-images.githubusercontent.com/76686112/121650164-326cec80-ca91-11eb-9b9f-055988cdcd0d.png)

The prices are stored in a database and a notification is shown to the user when the alert condition is reached for any of the alerts.

# Future Features
The database will be hosted remotely to allow notifications to be sent 24/7 to user; main menu will show the 24 hr chart,current price for each coin and whether the user has any alarms configured for that particular coin. 

# What I Learned

* How to extract data using an API
* How to call a separate python file and it's functions into a python file
* Creating graphs in matplotlib and then converting for kivy
* Writing to and reading from a database
* How to use source code through the declaration and usages
