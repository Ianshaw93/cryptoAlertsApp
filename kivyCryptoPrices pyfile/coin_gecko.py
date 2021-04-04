import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from kivy_garden.graph import Graph, MeshLinePlot   # plot handling

cg = CoinGeckoAPI() #setting up the client
cg.get_coins_list()


def get_crypto_fiat_price(cryptoCurrency='bitcoin',  fiatCurrency = 'usd'):
    crypto_fiat_price = cg.get_price(
        ids=cryptoCurrency,
        vs_currencies=fiatCurrency,
        output_format='pandas'
    )
    # print(cryptoFiatPrice)
    crypto_fiat_price = (crypto_fiat_price[cryptoCurrency][fiatCurrency])
    # currency, price = zip(*cryptoFiatPrice.items())
    # print (price)
    return (crypto_fiat_price)


def get_historical_crypto_price(cryptoCurrency = 'bitcoin',
                                relevant_date = '10-11-2020'):
    data = cg.get_coin_history_by_id(
        id = cryptoCurrency,
        date = relevant_date,
        localization ='false'
    )
    print(data)
    return data


def get_coin_markets_vs_fiat(fiatCurrency='usd'):
    coin_market = cg.get_coins_markets(vs_currency=fiatCurrency)
    #print(coin_market)
    df_market=pd.DataFrame(
        coin_market,
        columns=['id','current_price', 'high_24h', 'low_24h']
    )
    df_market.set_index('id', inplace=True)
    print(df_market)
    return coin_market


def get_market_chart(cryptoCurrency='bitcoin',
                     fiatCurrency = 'usd',
                     chart_period = 1):
    market_chart = cg.get_coin_market_chart_by_id(
        id=cryptoCurrency,
        vs_currency=fiatCurrency,
        days = chart_period,
        interval ='hourly',
        output_format='pandas'
    )
    market_chart_prices = market_chart['prices']
    time_stamp, price = zip(*market_chart_prices)
    time_date = pd.to_datetime(time_stamp, unit='ms')
    return time_date, price


def make_plot(plot_price, plot_dates, tickers_on_plot, plot_colors):
    x = list(range(1, (len(plot_price)+1)))
    y = plot_price
    #future write logic for ticks, if more than 10k price use 500 for ticks major
    plot = None
    # make the graph - ticks should be related to the price/change in price over time range
    # (xlabel = self.current_coin.capitalize() + self.graph_period +' day price'
    # how to get self and parameters from main.py into coin gecko?
    graph = Graph(
        xlabel = 'Bitcoin 1 day price', x_ticks_major = 1,
        y_ticks_minor = 100, y_ticks_major = 1000,
        y_grid_label=True, x_grid_label=True,
        padding=10, x_grid=True, y_grid=True,
        xmin=min(x), xmax=max(x), ymin=min(y), ymax=max(y)
    )

    for i in range(0, len(tickers_on_plot)):
        plot = MeshLinePlot(color=plot_colors[i])
        plot.points = [(i, j) for i, j in zip(x, (y))]
        graph.add_plot(plot)
    return graph
