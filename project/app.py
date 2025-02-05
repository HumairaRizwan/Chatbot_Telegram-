from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route('/', methods= ['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    #print(source_currency, amount, target_currency)
    cf = fetch_conv_factor(source_currency, target_currency)
    finalamount = amount * cf
    finalamount = round(finalamount,2)

    response = {'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, finalamount, target_currency)}
    return jsonify(response)

def fetch_conv_factor(source, target):
    url = "https://v6.exchangerate-api.com/v6/4f01638b1f8bbfc987c8fce0/pair/{}/{}".format(source, target)
    response = requests.get(url)
    response = response.json()#convert to json
    crate = response.get("conversion_rate", "Error fetching rate")
    #return response['{}_{}'.format(source,target)]
    return crate

if __name__ == "__main__":
    app.run(debug = True)
