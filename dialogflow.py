try:
    import urllib
    import json
    import os
    from flask import (Flask,request, make_response)
except Exception as e:
    print("Erro ao realizar o import de modulos. {}".format(e))

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        req = request.get_json(silent=True, force=True)
        res = processRequest(req)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def processRequest(req):
    query_response = req["queryResult"]
    print(query_response)
    text = query_response.get('queryText', None)
    parameters = query_response.get('parameters', None)
    res = get_data()
    return res

def get_data():
    speech = "Debora "
    return {
        "fulfillmentText": speech,
    }