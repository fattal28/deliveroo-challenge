import json
import math
import requests as req
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

auth = "db37117c-679d-41ae-b7cc-2c010daea9ed"
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


def get_restaurant(id):
    response = req.get(
        "https://roo-api-sandbox.deliveroo.net/restaurants/{}".format(id),
        params={},
        headers={"content-type": "application/json", "api-key": auth},
    )
    json_data = json.loads(response.text)
    return json_data


def is_restuarant_closed(id):
    restaurant = get_restaurant(id)
    return restaurant["status"] == "CLOSED"


def get_restaurant_lat_long(id):
    restaurant = get_restaurant(id)
    loc = restaurant["location"]
    return (float(loc["lat"]), float(loc["long"]))


def get_orders():
    response = req.get(
        "https://roo-api-sandbox.deliveroo.net/orders",
        params={},
        headers={"content-type": "application/json", "api-key": auth},
    )
    json_data = json.loads(response.text)
    return json_data


def get_riders():
    response = req.get(
        "https://roo-api-sandbox.deliveroo.net/riders",
        params={},
        headers={"content-type": "application/json", "api-key": auth},
    )
    json_data = json.loads(response.text)
    return json_data


def get_rider(id):
    response = req.get(
        "https://roo-api-sandbox.deliveroo.net/riders/{}".format(id),
        params={},
        headers={"content-type": "application/json", "api-key": auth},
    )
    json_data = json.loads(response.text)
    return json_data


def get_rider_lat_long(id):
    rider = get_rider(id)
    loc = rider["location"]
    return (float(loc["lat"]), float(loc["long"]))


def shortest_path(order, rider):
    return float(
        "{0:.5f}".format(((order[0] - rider[0]) ** 2 + (order[1] - rider[1])) ** 0.5)
    )


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def pairings(orders, riders):
    usable_riders = riders
    pairings = []
    for order in orders:
        smallest = {"d": 1000}
        orderll = get_restaurant_lat_long(order["restaurant_id"])
        i = 0
        while i < len(usable_riders):
            rider = usable_riders[i]
            loc = rider["location"]
            latlong = (float(loc["lat"]), float(loc["long"]))

            d = calculateDistance(latlong[0], latlong[1], orderll[0], orderll[1])
            if d < smallest["d"]:
                smallest = rider
                usable_riders.remove(rider)
                smallest["d"] = d
                break
            i += 1
        pairings.append([order, orderll, smallest])
    return pairings


if __name__ == "__main__":
    orders = get_orders()
    riders = get_riders()

    pairs = pairings(orders, riders)[0:10]
    for pair in pairs:

        print(pair)

    # app.run()

