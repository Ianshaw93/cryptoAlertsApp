import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from kivy_garden.graph import Graph, MeshLinePlot   # plot handling

cg = CoinGeckoAPI() #setting up the client
cg.get_coins_list()

#print(cg.get_price(ids='bitcoin', vs_currencies='gbp'))

def GetCryptoFiatPrice(cryptoCurrency='bitcoin',  fiatCurrency = 'usd'):
    cryptoFiatPrice = cg.get_price(ids=cryptoCurrency, vs_currencies=fiatCurrency, output_format='pandas')
    # print(cryptoFiatPrice)
    cryptoFiatPrice = (cryptoFiatPrice[cryptoCurrency][fiatCurrency])
    # currency, price = zip(*cryptoFiatPrice.items())
    # print (price)
    return (cryptoFiatPrice)

def GetHistoricalCryptoPrice(cryptoCurrency='bitcoin', relevant_date='10-11-2020'):
    data = cg.get_coin_history_by_id(id=cryptoCurrency, date=relevant_date, localization='false')
    print(data)
    return data


def GetCoinMarketsVsFiat(fiatCurrency='usd'):
    coin_market = cg.get_coins_markets(vs_currency=fiatCurrency)
    #print(coin_market)
    df_market=pd.DataFrame(coin_market, columns=['id','current_price', 'high_24h', 'low_24h'])
    df_market.set_index('id', inplace=True)
    print(df_market)
    return coin_market

def GetMarketChart(cryptoCurrency='bitcoin',  fiatCurrency = 'usd'):
    MarketChart = cg.get_coin_market_chart_by_id(id=cryptoCurrency, vs_currency=fiatCurrency, days = 1, interval ='hourly', output_format='pandas')
    #print(MarketChart)
    #print(MarketChart['prices'])
    MarketChartPrices = MarketChart['prices']
    time_stamp, price = zip(*MarketChartPrices)
    # #time_date = datetime(*time_stamp[0:6])
    # print(time_stamp)
    # time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_stamp)
    time_date = pd.to_datetime(time_stamp, unit='ms')
    #print(time_date)
    #time_x_axis = time_datemdates.DateFormatter("%H:%M")
    # if days >= 7:
    #     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m')) #for when the dataframe is 7 days or more
    # else:
    #     plt.gca().xaxis.set_major_formatter(strftime())
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    # #plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%y'))
    # plt.plot(time_date, price)
    # #x_axis = set(datetime.datetime.strptime((d,'%m/%d/%Y').date() for d in time_date))
    # plt.title((cryptoCurrency) + '/' + (fiatCurrency) + ' 24hr chart')
    # plt.ylabel("$ USD")
    # plt.xlabel("Date")
    # plt.show()
    return time_date, price


def make_plot(plot_price, plot_dates, tickers_on_plot, plot_colors):
    x = list(range(1, (len(plot_price)+1)))
    y = plot_price
    #future write logic for ticks, if more than 10k price use 500 for ticks major
    plot = None
    # make the graph
    graph = Graph(xlabel = 'Bitcoin 24hr price', x_ticks_major = 1, y_ticks_minor = 100, y_ticks_major = 1000,
                  y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                  xmin=min(x), xmax=max(x), ymin=min(y), ymax=max(y))

    for i in range(0, len(tickers_on_plot)):
        plot = MeshLinePlot(color=plot_colors[i])

        plot.points = [(i, j) for i, j in zip(x, (y))]

        graph.add_plot(plot)
    return graph
