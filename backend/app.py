from flask import Flask, jsonify, request
from flask_cors import CORS
import networkx as nx
import json
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Bcrypt and JWT
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# User data storage (Replace with DB in production)
users = {}

# Create an empty directed graph
RAG = nx.DiGraph()

# -------------------- PHASE 4: Save/Load Graph --------------------

# Load graph if available at startup
try:
    with open("rag_graph.json", "r") as f:
        graph_data = json.load(f)
        for node in graph_data["nodes"]:
            RAG.add_node(node[0], **node[1])
        for edge in graph_data["edges"]:
            RAG.add_edge(edge[0], edge[1])
except (FileNotFoundError, json.JSONDecodeError):
    pass


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the RAG Simulator Backend"})


# ------------------ Authentication Routes ------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users[username] = {"password": hashed_password, "role": "user"}
    return jsonify({"message": "User registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    user = users.get(username)
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"username": username, "role": user["role"]})
    return jsonify({"access_token": access_token})


# -------------------- PHASE 1: Add Node --------------------

@app.route("/add_node", methods=["POST"])
@jwt_required()
def add_node():
    data = request.json
    node_type = data["type"]
    node_name = data["name"]

    if not RAG.has_node(node_name):
        RAG.add_node(node_name, type=node_type)
        save_graph()
        broadcast_graph_update()
        return jsonify({"status": "Node added successfully"})
    else:
        return jsonify({"error": "Node already exists"}), 400


# -------------------- PHASE 2: Get Graph --------------------

@app.route("/get_graph", methods=["GET"])
def get_graph():
    graph_data = {
        "nodes": list(RAG.nodes(data=True)),
        "edges": list(RAG.edges())
    }
    return jsonify(graph_data)


# -------------------- PHASE 3: Check Deadlock --------------------

@app.route("/check_deadlock", methods=["GET"])
def check_deadlock():
    cycles = list(nx.simple_cycles(RAG))
    if cycles:
        return jsonify({"deadlock": True, "cycles": cycles})
    return jsonify({"deadlock": False})


# -------------------- PHASE 2: Add/Remove Edge --------------------

@app.route("/add_edge", methods=["POST"])
@jwt_required()
def add_edge():
    data = request.json
    source = data["source"]
    target = data["target"]

    if RAG.has_node(source) and RAG.has_node(target):
        RAG.add_edge(source, target)
        save_graph()
        broadcast_graph_update()
        return jsonify({"status": "Edge added successfully"})
    else:
        return jsonify({"error": "Invalid source or target"}), 400


@app.route("/remove_node", methods=["POST"])
@jwt_required()
def remove_node():
    data = request.json
    node_name = data["name"]

    if RAG.has_node(node_name):
        RAG.remove_node(node_name)
        save_graph()
        broadcast_graph_update()
        return jsonify({"status": "Node removed successfully"})
    else:
        return jsonify({"error": "Node not found"}), 404


@app.route("/remove_edge", methods=["POST"])
@jwt_required()
def remove_edge():
    data = request.json
    source = data["source"]
    target = data["target"]

    if RAG.has_edge(source, target):
        RAG.remove_edge(source, target)
        save_graph()
        broadcast_graph_update()
        return jsonify({"status": "Edge removed successfully"})
    else:
        return jsonify({"error": "Edge not found"}), 404


# -------------------- PHASE 4: Save/Load Graph --------------------

@app.route("/save_graph", methods=["POST"])
def save_graph():
    try:
        graph_data = {
            "nodes": list(RAG.nodes(data=True)),
            "edges": list(RAG.edges())
        }
        with open("rag_graph.json", "w") as f:
            json.dump(graph_data, f)
        return jsonify({"status": "Graph saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/load_graph", methods=["GET"])
def load_graph():
    try:
        with open("rag_graph.json", "r") as f:
            graph_data = json.load(f)

        # Clear the graph and load from file
        RAG.clear()
        for node in graph_data["nodes"]:
            RAG.add_node(node[0], **node[1])
        for edge in graph_data["edges"]:
            RAG.add_edge(edge[0], edge[1])

        return jsonify({"status": "Graph loaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- PHASE 5: Add Analytics & Insights --------------------

@app.route("/get_statistics", methods=["GET"])
def get_statistics():
    """Return statistics about the current graph."""
    num_processes = len([n for n, d in RAG.nodes(data=True) if d.get("type") == "process"])
    num_resources = len([n for n, d in RAG.nodes(data=True) if d.get("type") == "resource"])
    num_edges = RAG.number_of_edges()
    cycles = list(nx.simple_cycles(RAG))

    stats = {
        "num_processes": num_processes,
        "num_resources": num_resources,
        "num_edges": num_edges,
        "deadlock_count": len(cycles),
    }
    return jsonify(stats)


@app.route("/get_deadlock_details", methods=["GET"])
def get_deadlock_details():
    """Return details of detected deadlocks."""
    cycles = list(nx.simple_cycles(RAG))
    if cycles:
        return jsonify({"deadlock": True, "cycle_details": cycles})
    return jsonify({"deadlock": False, "cycle_details": []})


# -------------------- PHASE 6: Update Node Position --------------------

@app.route("/update_position", methods=["POST"])
def update_position():
    data = request.json
    node_id = data.get("id")
    position = data.get("position")

    if not node_id or not position:
        return jsonify({"error": "Invalid data"}), 400

    if RAG.has_node(node_id):
        RAG.nodes[node_id]["position"] = position
        save_graph()
        broadcast_graph_update()
        return jsonify({"status": f"Position of node {node_id} updated"})
    
    return jsonify({"error": "Node not found"}), 404


# -------------------- HELPER FUNCTION: Save Graph --------------------

def save_graph():
    """Save the current graph to a file."""
    graph_data = {
        "nodes": list(RAG.nodes(data=True)),
        "edges": list(RAG.edges())
    }
    with open("rag_graph.json", "w") as f:
        json.dump(graph_data, f)

# Broadcast graph update to all connected clients
def broadcast_graph_update():
    graph_data = {
        "nodes": list(RAG.nodes(data=True)),
        "edges": list(RAG.edges())
    }
    socketio.emit("graph_update", graph_data)

# Real-time Sync: Emit Graph State on Connection
@socketio.on("connect")
def handle_connect():
    graph_data = {
        "nodes": list(RAG.nodes(data=True)),
        "edges": list(RAG.edges())
    }
    emit("graph_update", graph_data)
    print("Client connected")

# Real-time Sync: Disconnect
@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

# -------------------- RUN FLASK SERVER --------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)





