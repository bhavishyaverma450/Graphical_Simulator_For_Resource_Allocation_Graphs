# Backend Documentation: `app.py`

The `app.py` file serves as the backend for the Real-Time RAG Simulator. It provides RESTful APIs and real-time communication using Flask, Flask-SocketIO, and NetworkX.

---

## Features

### 1. **Authentication**
- **Register**: Allows users to register with a username and password.
- **Login**: Provides a JWT token for authenticated access to protected routes.

### 2. **Graph Operations**
- **Add Node**: Add a process or resource node to the graph.
- **Remove Node**: Remove a node from the graph.
- **Add Edge**: Add an edge between two nodes.
- **Remove Edge**: Remove an edge between two nodes.
- **Save Graph**: Save the current graph state to a file.
- **Load Graph**: Load the graph state from a file.

### 3. **Analytics**
- **Graph Statistics**: Retrieve statistics such as the number of processes, resources, edges, and deadlocks.
- **Deadlock Detection**: Check for deadlocks and retrieve details of detected cycles.

### 4. **Real-Time Updates**
- **Socket.IO**: Broadcast graph updates to all connected clients in real-time.

---

## API Endpoints

### Authentication
- `POST /register`: Register a new user.
- `POST /login`: Log in and receive a JWT token.

### Graph Operations
- `POST /add_node`: Add a new node to the graph (requires JWT).
- `POST /remove_node`: Remove a node from the graph (requires JWT).
- `POST /add_edge`: Add a new edge to the graph (requires JWT).
- `POST /remove_edge`: Remove an edge from the graph (requires JWT).
- `POST /save_graph`: Save the current graph state to a file.
- `GET /load_graph`: Load the graph state from a file.
- `GET /get_graph`: Retrieve the current graph state.

### Analytics
- `GET /get_statistics`: Retrieve graph statistics.
- `GET /get_deadlock_details`: Retrieve details of detected deadlocks.
- `GET /check_deadlock`: Check if the graph contains deadlocks.

### Node Position
- `POST /update_position`: Update the position of a node in the graph.

---

## Real-Time Communication

### Socket.IO Events
- **`connect`**: Triggered when a client connects. Sends the current graph state to the client.
- **`disconnect`**: Triggered when a client disconnects.
- **`graph_update`**: Broadcasted to all clients when the graph is updated.

---

## Helper Functions

### `save_graph()`
Saves the current graph state to a JSON file (`rag_graph.json`).

### `broadcast_graph_update()`
Broadcasts the current graph state to all connected clients via Socket.IO.

---

## Notes
- Replace the in-memory user storage (`users` dictionary) with a database for production use.
- Ensure the `JWT_SECRET_KEY` is securely stored in production environments.
- Use HTTPS for secure communication in production.

