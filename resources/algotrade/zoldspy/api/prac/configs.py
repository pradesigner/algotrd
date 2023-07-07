from urllib.parse import urljoin
import json
import requests
import pandas as pd


# general
sl = '/'
scheme = 'https'
datetime_format = 'RFC3339'

# prac
hostapi = 'https://api-fxpractice.oanda.com'
hoststr = 'https://stream-fxpractice.oanda.com'
acct03 = '101-002-9789110-003'
hdprac = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

# paths
accts = '/v3/accounts'


def formurl(*frags):
    '''forms url to base using frags tuple'''
    res = ''
    for frag in frags:
        res += frag
    return res


def accounts():
    '''get all account ids'''
    response = requests.get(
        'https://api-fxpractice.oanda.com/v3/accounts',
        headers=hdprac)
    return json.loads(response.content)


def details():
    '''get account details'''
    response = requests.get(
        'https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003',
        headers=hdprac)
    return json.loads(response.content)


def summary():
    '''gets summary'''
    response = requests.get(
        'https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/summary',
        headers=hdprac)
    return json.loads(response.content)


def instruments():
    '''gets trading instruments'''
    response = requests.get(
        'https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/instruments',
        headers=hdprac)
    return json.loads(response.content)


def get_candles(ins, num, grn):
    '''gets num candles of grn with hml price for ins using aid

    ins = instrument name in XXX_YYY format
    num = number of candles
    grn = granularity or tf S...; M...; H1,4; D; W; M
    '''
    params = (
        ('count', num),
        ('price', 'M'),
        ('granularity', grn),
    )

    response = requests.get(
        f'https://api-fxpractice.oanda.com/v3/instruments/{ins}/candles',
        headers=hdprac,
        params=params)

    # get the content of response
    content = json.loads(response.content)

    # read into df
    df = pd.read_json(json.dumps(content))

    # extract the candles info
    df = pd.io.json.json_normalize(df.candles)

    # convert time column to datetime_format
    df['time'] = pd.to_datetime(df['time'])

    # drop tz part to give just HH:MM:SS
    df['time'] = df['time'].dt.tz_localize(None)

    # rename the columns
    df.rename(columns={
        'mid.o': 'o',
        'mid.l': 'l',
        'mid.c': 'c',
        'mid.h': 'h'}, inplace=True)

    # reorder the columns dropping unnecessary ones
    df = df[['time', 'l', 'o', 'c', 'h', 'volume']]

    return df


'''
https://curl.trillworks.com/

# curl: Get Account list for current auth token
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  "https://api-fxpractice.oanda.com/v3/accounts"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts', headers=headers)


# curl: Get details for Account
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003', headers=headers)


# curl: Get summary for Account
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/summary"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/summary', headers=headers)


# curl: Get All Instrument Details for Account
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/instruments"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/instruments', headers=headers)


# curl: Get EUR/USD Instrument Details for Account
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

params = (
    ('instruments', 'EUR_USD'),
)

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/instruments', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/instruments?instruments=EUR_USD', headers=headers)


# curl: Set the margin rate override for Account to 50:1 ??????
body=$(cat << EOF
{
  "marginRate": "0.02"
}
EOF
)
curl \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  -d "$body" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/configuration"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

data = '$body'

response = requests.patch('http://%3C%3C', headers=headers, data=data)


# curl: Change the alias for Account ??????
body=$(cat << EOF
{
  "alias": "My New Account #2"
}
EOF
)

curl \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  -d "$body" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/configuration"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

data = '$body'

response = requests.patch('http://%3C%3C', headers=headers, data=data)


# curl: Get all changes for Account since Transaction 6358
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7" \
  "https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/changes?sinceTransactionID=6358"
==
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7',
}

params = (
    ('sinceTransactionID', '6358'),
)

response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/changes', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-002-9789110-003/changes?sinceTransactionID=6358', headers=headers)


'''
