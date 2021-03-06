#!/usr/bin/env python3

import alpaca_trade_api as tradeapi
import requests
import time
from ta.trend import macd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import sys
from os import path
import pandas as pd
import json
import os

def alpaca_profile(args):
    # Sets text file with base_url, api_key_id, api_secret
    data = {}
    if sys.argv[1] == '--info':
        if path.exists('.alpaca_profile.txt'):
            json_file = open('.alpaca_profile.txt', 'r')
            data = json.load(json_file)
            for key, value in data.items():
                print(key, " is ", value)
            if not 'base-url' in data:
                print('Add base-url to alpaca_profile.')
            if not 'api-key' in data:
                print('Add api-key to alpaca_profile.')
            if not 'secret_key' in data:
                print('Add secret-key to alpaca_profile.')
        else:
            print('Add base-url, api-key, and secret-key.')
    elif len(sys.argv) != 4:
        raise IOError('Must be entered: trading_bot -s type setting')
    if sys.argv[1] == '-s':
        if sys.argv[2] == 'base-url':
            if path.exists('.alpaca_profile.txt'):
                read = open('.alpaca_profile.txt', 'r')
                data = json.load(read)
            data['base-url'] = sys.argv[3]
            f = open(".alpaca_profile.txt","w")
            f.write(json.dumps(data))
            f.close()
        elif sys.argv[2] == 'api-key':
            if path.exists('.alpaca_profile.txt'):
                read = open('.alpaca_profile.txt', 'r')
                data = json.load(read)
            data['api-key'] = sys.argv[3]                
            f = open(".alpaca_profile.txt","w")
            f.write(json.dumps(data))
            f.close()
        elif sys.argv[2] == 'secret-key':
            if path.exists('.alpaca_profile.txt'):
                read = open('.alpaca_profile.txt', 'r')
                data = json.load(read)
            data['secret-key'] = sys.argv[3]
            f = open(".alpaca_profile.txt","w")
            f.write(json.dumps(data))
            f.close()    
        else:
            print('You can only set base-url, api-key, or secret-key')


# Helper function for creating array of chars from string
def split(word): 
    return [char for char in word] 

def run_bot(args):
    # Initialize flags
    # risk
    r = None
    # default_stop
    d = None
    # min_share_price
    n = None
    # max_share_price
    x = None
    # min_last_dv
    l = None
    # verbose for debugging
    verbose = True


    # Check to make sure parameters are correct, meets minimum amount
#    if(len(sys.argv) < 4):
#        raise IOError("trading_bot -flags <base_url> <api_key_id> <api_secret_key> ") 
    # Checks if there is flags
    j = 1
    if(len(sys.argv) != 4):
        for i in range(1,len(sys.argv)):
            chars = split(sys.argv[i])
            if chars[0] is '-':
                j = i + 2
                if chars[1] is 'r':
                    r = sys.argv[i+1]
                elif chars[1] is 'd':
                    d = sys.argv[i+1]
                elif chars[1] is 'n':
                    n = sys.argv[i+1]
                elif chars[1] is 'x':
                    x = sys.argv[i+1]
                elif chars[1] is 'l':
                    l = sys.argv[i+1]
                elif chars[1] is 'v':
                    verbose = True
                    j = i + 1

    # Replace these with your API connection info from preset info
    f = open('.alpaca_profile.txt', 'r')
    data = json.load(f)
    base_url = data['base-url']
    api_key_id = data['api-key']
    api_secret = data['secret-key']
    if verbose:
        print('API connection info is set.')

    api = tradeapi.REST(
        base_url   = base_url,
        key_id     = api_key_id,
        secret_key = api_secret
    )

    session = requests.session()

    # Initialize parameters
    min_share_price = 0
    max_share_price = 0
    min_last_dv     = 0
    default_stop    = 0
    risk            = 0

    # We only consider stocks with per-share prices inside this range
    if n is None:
        min_share_price = 2.0
        if verbose:
            print('The minimum share price is set to the default, ', min_share_price)
    else: 
        min_share_price = float(n)
        if verbose:
            print('The minimum share price is custom, ', min_share_price)
    if x is None:
        max_share_price = 13.0
        if verbose:
            print('The maximum share price is set to the default, ', max_share_price)
    else:
        max_share_price = float(x)
        if verbose:
            print('The maximum share price is custom, ', max_share_price)
    # Minimum previous-day dollar volume for a stock we might consider
    if l is None:
        min_last_dv     = 500000
        if verbose:
            print('The minimum previous-day dollar volume for a stock is set to the default, ', min_last_dv)
    else:
        min_last_dv     = float(l)
        if verbose:
            print('The minimum previous-day dollar volume for a stock is custom, ', min_last_dv)
    # Stop limit to default to
    if d is None:
        default_stop    = .95
        if verbose:
            print('The stop limit is set to the default, ', default_stop)
    else: 
        default_stop    = float(d)
        if verbose:
            print('The stop limit is set custom, ', default_stop)
    # How much of our portfolio to allocate to any one position
    if r is None:
        risk            = 0.01
        if verbose:
            print('The percent of portfolio to allocate to one position is set to the default, ', risk)
    else:
        risk            = float(r)
        if verbose:
            print('The percent of portfolio to allocate to one position is set custom, ', risk)


    def get_1000m_history_data(symbols):
        print('Getting historical data...')
        minute_history = {}
        c = 0
        for symbol in symbols:
            minute_history[symbol] = api.polygon.historic_agg(
                size="minute", symbol=symbol, limit=1000
            ).df
            c += 1
            print('{}/{}'.format(c, len(symbols)))
        print('Success.')
        return minute_history


    def get_tickers():
        print('Getting current ticker data...')
        tickers = api.polygon.all_tickers()
        print('Success.')
        assets = api.list_assets()
        symbols = [asset.symbol for asset in assets if asset.tradable]
        return [ticker for ticker in tickers if (
            ticker.ticker in symbols and
            ticker.lastTrade['p'] >= min_share_price and
            ticker.lastTrade['p'] <= max_share_price and
            ticker.prevDay['v'] * ticker.lastTrade['p'] > min_last_dv and
            ticker.todaysChangePerc >= 3.5
        )]


    def find_stop(current_value, minute_history, now):
        series = minute_history['low'][-100:] \
                    .dropna().resample('5min').min()
        series = series[now.floor('1D'):]
        diff = np.diff(series.values)
        low_index = np.where((diff[:-1] <= 0) & (diff[1:] > 0))[0] + 1
        if len(low_index) > 0:
            return series[low_index[-1]] - 0.01
        return current_value * default_stop


    def run(tickers, market_open_dt, market_close_dt):
        # Establish streaming connection
        conn = tradeapi.StreamConn(base_url=base_url, key_id=api_key_id, secret_key=api_secret)

        # Update initial state with information from tickers
        volume_today = {}
        prev_closes = {}
        for ticker in tickers:
            symbol = ticker.ticker
            prev_closes[symbol] = ticker.prevDay['c']
            volume_today[symbol] = ticker.day['v']

        symbols = [ticker.ticker for ticker in tickers]
        print('Tracking {} symbols.'.format(len(symbols)))
        minute_history = get_1000m_history_data(symbols)

        portfolio_value = float(api.get_account().portfolio_value)

        open_orders = {}
        positions = {}

        # Cancel any existing open orders on watched symbols
        existing_orders = api.list_orders(limit=500)
        for order in existing_orders:
            if order.symbol in symbols:
                api.cancel_order(order.id)

        stop_prices = {}
        latest_cost_basis = {}

        # Track any positions bought during previous executions
        existing_positions = api.list_positions()
        for position in existing_positions:
            if position.symbol in symbols:
                positions[position.symbol] = float(position.qty)
                # Recalculate cost basis and stop price
                latest_cost_basis[position.symbol] = float(position.cost_basis)
                stop_prices[position.symbol] = (
                    float(position.cost_basis) * default_stop
                )

        # Keep track of what we're buying/selling
        target_prices = {}
        partial_fills = {}

        # Use trade updates to keep track of our portfolio
        @conn.on(r'trade_update')
        async def handle_trade_update(conn, channel, data):
            symbol = data.order['symbol']
            last_order = open_orders.get(symbol)
            if last_order is not None:
                event = data.event
                if event == 'partial_fill':
                    qty = int(data.order['filled_qty'])
                    if data.order['side'] == 'sell':
                        qty = qty * -1
                    positions[symbol] = (
                        positions.get(symbol, 0) - partial_fills.get(symbol, 0)
                    )
                    partial_fills[symbol] = qty
                    positions[symbol] += qty
                    open_orders[symbol] = data.order
                elif event == 'fill':
                    qty = int(data.order['filled_qty'])
                    if data.order['side'] == 'sell':
                        qty = qty * -1
                    positions[symbol] = (
                        positions.get(symbol, 0) - partial_fills.get(symbol, 0)
                    )
                    partial_fills[symbol] = 0
                    positions[symbol] += qty
                    open_orders[symbol] = None
                elif event == 'canceled' or event == 'rejected':
                    partial_fills[symbol] = 0
                    open_orders[symbol] = Noneta

        @conn.on(r'A$')
        async def handle_second_bar(conn, channel, data):
            symbol = data.symbol

            # First, aggregate 1s bars for up-to-date MACD calculations
            ts = data.start
            ts -= timedelta(seconds=ts.second, microseconds=ts.microsecond)
            try:
                current = minute_history[data.symbol].loc[ts]
            except KeyError:
                current = None
            new_data = []
            if current is None:
                new_data = [
                    data.open,
                    data.high,
                    data.low,
                    data.close,
                    data.volume
                ]
            else:
                new_data = [
                    current.open,
                    data.high if data.high > current.high else current.high,
                    data.low if data.low < current.low else current.low,
                    data.close,
                    current.volume + data.volume
                ]
            minute_history[symbol].loc[ts] = new_data

            # Next, check for existing orders for the stock
            existing_order = open_orders.get(symbol)
            if existing_order is not None:
                # Make sure the order's not too old
                submission_ts = existing_order.submitted_at.astimezone(
                    timezone('America/New_York')
                )
                order_lifetime = ts - submission_ts
                if order_lifetime.seconds // 60 > 1:
                    # Cancel it so we can try again for a fill
                    api.cancel_order(existing_order.id)
                return

            # Now we check to see if it might be time to buy or sell
            since_market_open = ts - market_open_dt
            until_market_close = market_close_dt - ts
            if (
                since_market_open.seconds // 60 > 15 and
                since_market_open.seconds // 60 < 60
            ):
                # Check for buy signals

                # See if we've already bought in first
                position = positions.get(symbol, 0)
                if position > 0:
                    return

                # See how high the price went during the first 15 minutes
                lbound = market_open_dt
                ubound = lbound + timedelta(minutes=15)
                high_15m = 0
                try:
                    high_15m = minute_history[symbol][lbound:ubound]['high'].max()
                except Exception as e:
                    # Because we're aggregating on the fly, sometimes the datetime
                    # index can get messy until it's healed by the minute bars
                    return

                # Get the change since yesterday's market close
                daily_pct_change = (
                    (data.close - prev_closes[symbol]) / prev_closes[symbol]
                )
                if (
                    daily_pct_change > .04 and
                    data.close > high_15m and
                    volume_today[symbol] > 30000
                ):
                    # check for a positive, increasing MACD
                    hist = macd(
                        minute_history[symbol]['close'].dropna(),
                        n_fast=12,
                        n_slow=26
                    )
                    if (
                        hist[-1] < 0 or
                        not (hist[-3] < hist[-2] < hist[-1])
                    ):
                        return
                    hist = macd(
                        minute_history[symbol]['close'].dropna(),
                        n_fast=40,
                        n_slow=60
                    )
                    if hist[-1] < 0 or np.diff(hist)[-1] < 0:
                        return

                    # Stock has passed all checks; figure out how much to buy
                    stop_price = find_stop(
                        data.close, minute_history[symbol], ts
                    )
                    stop_prices[symbol] = stop_price
                    target_prices[symbol] = data.close + (
                        (data.close - stop_price) * 3
                    )
                    shares_to_buy = portfolio_value * risk // (
                        data.close - stop_price
                    )
                    if shares_to_buy == 0:
                        shares_to_buy = 1
                    shares_to_buy -= positions.get(symbol, 0)
                    if shares_to_buy <= 0:
                        return

                    print('Submitting buy for {} shares of {} at {}'.format(
                        shares_to_buy, symbol, data.close
                    ))
                    try:
                        o = api.submit_order(
                            symbol=symbol, qty=str(shares_to_buy), side='buy',
                            type='limit', time_in_force='day',
                            limit_price=str(data.close)
                        )
                        open_orders[symbol] = o
                        latest_cost_basis[symbol] = data.close
                    except Exception as e:
                        print(e)
                    return
            if(
                since_market_open.seconds // 60 >= 24 and
                until_market_close.seconds // 60 > 15
            ):
                # Check for liquidation signals

                # We can't liquidate if there's no position
                position = positions.get(symbol, 0)
                if position == 0:
                    return

                # Sell for a loss if it's fallen below our stop price
                # Sell for a loss if it's below our cost basis and MACD < 0
                # Sell for a profit if it's above our target price
                hist = macd(
                    minute_history[symbol]['close'].dropna(),
                    n_fast=13,
                    n_slow=21
                )
                if (
                    data.close <= stop_prices[symbol] or
                    (data.close >= target_prices[symbol] and hist[-1] <= 0) or
                    (data.close <= latest_cost_basis[symbol] and hist[-1] <= 0)
                ):
                    print('Submitting sell for {} shares of {} at {}'.format(
                        position, symbol, data.close
                    ))
                    try:
                        o = api.submit_order(
                            symbol=symbol, qty=str(position), side='sell',
                            type='limit', time_in_force='day',
                            limit_price=str(data.close)
                        )
                        open_orders[symbol] = o
                        latest_cost_basis[symbol] = data.close
                    except Exception as e:
                        print(e)
                return
            elif (
                until_market_close.seconds // 60 <= 15
            ):
                # Liquidate remaining positions on watched symbols at market
                try:
                    position = api.get_position(symbol)
                except Exception as e:
                    # Exception here indicates that we have no position
                    return
                print('Trading over, liquidating remaining position in {}'.format(
                    symbol)
                )
                api.submit_order(
                    symbol=symbol, qty=position.qty, side='sell',
                    type='market', time_in_force='day'
                )
                symbols.remove(symbol)
                if len(symbols) <= 0:
                    conn.close()
                conn.deregister([
                    'A.{}'.format(symbol),
                    'AM.{}'.format(symbol)
                ])

        # Replace aggregated 1s bars with incoming 1m bars
        @conn.on(r'AM$')
        async def handle_minute_bar(conn, channel, data):
            ts = data.start
            ts -= timedelta(microseconds=ts.microsecond)
            minute_history[data.symbol].loc[ts] = [
                data.open,
                data.high,
                data.low,
                data.close,
                data.volume
            ]
            volume_today[data.symbol] += data.volume

        channels = ['trade_updates']
        for symbol in symbols:
            symbol_channels = ['A.{}'.format(symbol), 'AM.{}'.format(symbol)]
            channels += symbol_channels
        print('Watching {} symbols.'.format(len(symbols)))
        run_ws(conn, channels)


    # Handle failed websocket connections by reconnecting
    def run_ws(conn, channels):
        try:
            conn.run(channels)
        except Exception as e:
            print(e)
            conn.close()
            run_ws(conn, channels)


    if __name__ == "__main__":
        # Get when the market opens or opened today
        nyc = timezone('America/New_York')
        today = datetime.today().astimezone(nyc)
        today_str = datetime.today().astimezone(nyc).strftime('%Y-%m-%d')
        calendar = api.get_calendar(start=today_str, end=today_str)[0]
        market_open = today.replace(
            hour=calendar.open.hour,
            minute=calendar.open.minute,
            second=0
        )
        market_open = market_open.astimezone(nyc)
        market_close = today.replace(
            hour=calendar.close.hour,
            minute=calendar.close.minute,
            second=0
        )
        market_close = market_close.astimezone(nyc)

        # Wait until just before we might want to trade
        current_dt = datetime.today().astimezone(nyc)
        since_market_open = current_dt - market_open
        while since_market_open.seconds // 60 <= 14:
            time.sleep(1)
            since_market_open = current_dt - market_open

        run(get_tickers(), market_open, market_close)

if __name__=='__main__':
    run = True
    flags = ['-s', '--info']
    if sys.argv[1] in flags:
        alpaca_profile(sys.argv)
    else:
        if path.exists('.alpaca_profile.txt'):
            f = open('.alpaca_profile.txt', 'r')
            d = json.load(f)
            print(d)
            if not 'base-url' in d:
                print('Add base-url to Alpaca profile.')
                run = False
            if not 'api-key' in d:
                print('Add api-key to Alpaca profile')
                run = False
            if not 'secret-key' in d:
                print('Add secret-key to Alpaca profile')
                run = False
            if run:
                run_bot(sys.argv)
        else:
            print('Input the following info for Alpaca info:')
            print('<base-url>')
            print('<api-key>')
            print('<secret-key>')
