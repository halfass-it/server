from flask import Blueprint, jsonify, request

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/")
def index():
  return ""


@app_routes.route("/recv")
def recv():
    # Access JSON data from the request body
    data = request.json
    print(f"sending <<{data}>> to {request.remote_addr}")
    res = jsonify(data)
    return res

@app_routes.route("/send", methods=['POST'])
def send():
    # Assuming you're trying to print data from a request
    print(f"receiving {request.args} from {request.remote_addr}")
    print(request.json)
    print(f"sending <<{jsonify({"ack": "true"})}>> to {request.remote_addr}")