from flask import Flask, Response, request, jsonify
from socks import method

app = Flask(__name__)

drones = ["RDR01", "RDR02", "RDR03"]


@app.route('/')
def hello_world() -> str:
    return 'Hello World!'


@app.route('/drones', methods=['GET'])
def get_drones() -> []:
    return drones


@app.route('/drones/<int:drone_id>', methods=['GET'])
def get_drone(drone_id: int) -> Response:
    if drone_id > len(drones):
        return Response(status=404)
    drone_name: str = drones[drone_id - 1]
    return jsonify(id=drone_id, name=drone_name)


@app.route('/drones', methods=["POST"])
def add_drone():
    # data = request.data
    json = request.json
    if _is_exists(json["name"]):
        return Response(status=409)
    drones.append(json["name"])
    response: Response = jsonify(id=len(drones), name=json["name"])
    response.status = 201
    response.mimetype = "application/json"
    return response

def _is_exists(checked_drone_name) -> bool:
    return checked_drone_name.upper() in (drone_name.upper() for drone_name in drones)


@app.route('/drones/<int:drone_id>', methods=["PUT"])
def update_drone(drone_id: int):
    if drone_id > len(drones):
        return Response(status=404)
    drones[drone_id - 1] = request.json["name"]
    response: Response = jsonify(id=drone_id, name=drones[drone_id - 1])
    response.status = 201
    response.mimetype = "application/json"
    return response


@app.route('/drones/<int:drone_id>', methods=["DELETE"])
def delete_drone(drone_id: int):
    del drones[drone_id - 1]
    return Response("{'Status':'Success'}", status=204, mimetype='application/json')


if __name__ == '__main__':
    app.run()
