import json, config
from flask import Flask, request
app = Flask(__name__)

from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


@app.route('/webhook', methods=['POST'])
def webhook():

    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return { 
            "code": "error",
            "message": "Access Denied."
        }
    
    print(data['ticker'])
    print(data['bar'])

    side = data['strategy']['order_action'].upper()
    order_response = order(side, 0.05, "LTCUSDT")
    print(order_response)

    if order_response:
        print('order succuss')
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")
        return {
            "code": "error",
            "message": "order failed"
        }


@app.route('/test', methods=['POST'])
def test():
    print(request.data)

    json_data = json.loads(request.data)
    return{
        "code": "success",
        "message": json_data
    }