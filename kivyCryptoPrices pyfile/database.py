

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.alerts = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.alerts = {}

        for line in self.file:
            price_target, coin, symbol = line.strip().split(";")
            self.alerts[price_target] = (coin, symbol)

        self.file.close()

    # # no need to retrieve alerts - only check against current price
    # def get_user(self, email):
    #     if coin in self.alerts:
    #         return self.alerts[coin]
    #     else:
    #         return -1
    # add current coin to method
    def add_alert(self, coin, symbol, price_target):
        print(coin, symbol, price_target)
    # if price and symbol together are not in price log for that coin
        if price_target.strip() not in self.alerts:
            # needs to be refined to allow same price but different symbol, and same price for different coins
            self.alerts[price_target.strip()] = (coin.strip(), symbol.strip())
            self.save()
            return 1
        else:
            # elsif where price is present, but symbol/coin are different still add into txt file
            print("Alert exists already")
            return -1


    # def validate(self, email, password):
    #     if self.get_user(email) != -1:
    #         return self.users[email][0] == password
    #     else:
    #         return False


    def save(self):
        with open(self.filename, "w") as f:
            for alert in self.alerts:
                f.write(alert + ";" + self.alerts[alert][0] + ";" + self.alerts[alert][1] + "\n")

    # def alerts(self):
    #     pass