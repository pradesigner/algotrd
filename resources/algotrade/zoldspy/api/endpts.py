'''
library of oanda api endpoints

useable functions to communicate with oanda api
grouped into following sections:

account
instrument
order
trade
position
transaction
pricing

details provided  within each section
'''


from urllib.parse import urljoin
import os
import json
import requests
import pytz
import pandas as pd
from algo.tfx import pcf_assign

Papi = 'https://api-fxpractice.oanda.com'
Pstr = 'https://stream-fxpractice.oanda.com'
Ptok = '8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7'
Pid3 = '/101-002-9789110-003'
v3ac = '/v3/accounts'
v3in = '/v3/instruments'
ords = '/orders'

# set Prac vs Live parameters
theapi = Papi
thestr = Pstr
thetok = Ptok
theaid = Pid3

acctid = theapi + v3in + theaid

hdr = {  # headers
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + thetok
}


# Accessory functions

def ordertype(ins, entry, vol):
    '''determine ordertype from current and entry price'''
    current = current_price(ins)
    if vol > 0:
        if entry > current:
            the_type = 'STOP'
        elif entry < current:
            the_type = 'LIMIT'
    else:
        if entry > current:
            the_type = 'LIMIT'
        elif entry < current:
            the_type = 'STOP'
    return the_type


def current_price(ins):
    '''gets current price for ins'''
    response = requests.get(
        theapi + v3ac + theaid + f'/pricing?instruments={ins}',
        headers=hdr)
    c = json.loads(response.content)  # contents
    bid = float(c['prices'][0]['closeoutBid'])
    ask = float(c['prices'][0]['closeoutAsk'])
    pri = (bid+ask)/2
    return pri


# Account Endpoints #

def accounts():
    '''The list of authorized Accounts has been provided.'''
    response = requests.get(
        theapi + v3ac,
        headers=hdr)
    return json.loads(response.content)


def details():
    '''The full Account details are provided'''
    response = requests.get(
        acctid,
        headers=hdr
    )
    return json.loads(response.content)


def summary():
    '''The Account summary are provided'''
    response = requests.get(
        acctid + '/summary',
        headers=hdr
    )
    return json.loads(response.content)


def instruments():
    '''The list of tradeable instruments for the Account has been provided.'''
    response = requests.get(
        acctid + '/instruments',
        headers=hdr
    )
    return json.loads(response.content)


def reconfig(key, value):
    '''Set client-configurable portions of an account'''
    response = requests.patch(
        acctid + '/configuration',
        headers=hdr,
        json={key: value}
    )
    return response


def changes(tid):
    '''The Account state and changes are provided since last tid.'''
    par = (
        ('sinceTransactionID', tid),  # tid transactionID
    )
    response = requests.get(
        acctid + '/changes',
        headers=hdr,
        params=par
    )
    return json.loads(response.content)


# Instrument Endpoints #

def candles(ins, num, grn):
    '''gets num candles of grn with hml price for ins using aid

    ins = instrument name in XXX_YYY format
    num = number of candles
    grn = granularity or tf S...; M...; H1,4; D; W; M
    '''
    params = (
        ('count', num),
        ('price', 'M'),
        ('granularity', grn)
    )

    response = requests.get(
        theapi+f'/v3/instruments/{ins}/candles',
        headers=hdr,
        params=params
    )

    # get the content of response
    content = json.loads(response.content)

    # read into df
    df = pd.read_json(json.dumps(content))

    # extract the candles info
    df = pd.io.json.json_normalize(df.candles)

    # convert time column to datetime_format
    df['time'] = pd.to_datetime(df['time'])

    # convert to PST and drop tz part to give just HH:MM:SS
    PST = pytz.timezone('US/Pacific')
    df['time'] = df['time'].dt.tz_convert(PST).dt.tz_localize(None)

    # rename the columns
    df.rename(
        columns={'mid.o': 'open',
                 'mid.l': 'low',
                 'mid.c': 'close',
                 'mid.h': 'high'},
        inplace=True
    )

    # reorder the columns dropping unnecessary ones
    df = df[['time', 'open', 'high', 'low', 'close', 'volume']]

    return df


def orderbook(ins, snapshot=None):
    '''gets order book for ins at snapshot time'''
    pairid = '/{}/orderBook'.format(ins)
    if snapshot is None:
        info = pairid.format(ins)
    else:
        info = pairid+'?time={}'.format(snapshot)
    response = requests.get(
        theapi+v3in+info,
        headers=hdr)
    return json.loads(response.content)


def positionbook(ins, snapshot=None):
    '''gets position book for ins at snapshot Zulu time'''
    pairid = '/{}/positionBook'.format(ins)
    if snapshot is None:
        info = pairid.format(ins)
    else:
        info = pairid+'?time={}'.format(snapshot)
    response = requests.get(
        theapi+v3in+info,
        headers=hdr)
    return json.loads(response.content)


# Order Endpoints #

def order(ins, sl, tp, vol, pr=None):
    '''create a market order
    ins - XXX_YYY
    sl, tp, vol -  numeric
    pr is numeric (entry) or None (for market)
    '''

    if pr is None:  # market order
        tif = 'FOK'
        typ = 'MARKET'
    else:  # entry order
        tif = 'GTC'
        typ = ordertype(ins, pr, vol)

    # convert to string
    sl, tp, vol, pr = (str(itm) for itm in (sl, tp, vol, pr))

    # set up the json variable
    jsonvar = {'order':
               {'instrument': ins,
                'price': pr,
                'units': vol,
                'timeInForce': tif,
                'type': typ,
                'positionFill': 'DEFAULT',
                'stopLossOnFill': {
                    'timeInForce': 'GTC',
                    'price': sl},
                'takeProfitOnFill': {
                    'price': tp}
                }
               }

    # send order request
    response = requests.post(
        theapi+v3ac+Pid3+ords,
        json=jsonvar,
        headers=hdr
    )
    return response
