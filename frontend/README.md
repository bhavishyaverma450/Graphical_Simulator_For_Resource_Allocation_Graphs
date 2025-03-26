# Frontend Documentation: Real-Time RAG Simulator

The frontend application is built using React and provides a user interface for interacting with the Real-Time RAG Simulator. It includes features like graph visualization, deadlock detection, user authentication, and advanced analytics.

---

## Features

### 1. **Authentication**
- **Register**: Create a new user account.
- **Login**: Authenticate using a username and password to access protected routes.
- **Token-Based Authentication**: Secure API requests using JWT tokens.

### 2. **Graph Operations**
- **Add Node**: Add process or resource nodes to the graph.
- **Remove Node**: Remove nodes from the graph.
- **Add Edge**: Add edges between nodes.
- **Remove Edge**: Remove edges between nodes.
- **Drag-and-Drop**: Update node positions interactively with real-time backend synchronization.

### 3. **Graph Visualization**
- **Cytoscape Integration**: Visualize the graph with draggable nodes and real-time updates.
- **Context Menu**: Right-click to delete nodes or edges.
- **Double-Click**: Add new nodes interactively.

### 4. **Analytics**
- **Graph Statistics**: View the number of processes, resources, edges, and deadlocks.
- **Deadlock Detection**: Check for deadlocks and view details of detected cycles.
- **Charts**: Bar and pie charts for visualizing graph statistics and deadlock summaries.

### 5. **Save/Load Graph**
- Save the current graph state to the backend.
- Load a previously saved graph state.

---

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/rag-simulator.git
   cd rag-simulator/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open the application in your browser at `http://localhost:3000`.

---

## Component Overview

### 1. **App.js**
- The main entry point of the application.
- Handles routing and renders components based on the user's authentication status.
- Integrates real-time updates via Socket.IO.

### 2. **GraphCanvas.js**
- Renders the graph using Cytoscape.
- Supports drag-and-drop, double-click to add nodes, and context menus for deleting elements.
- Synchronizes node positions with the backend.

### 3. **GraphStats.js**
- Displays bar and pie charts for graph statistics and deadlock overview using Chart.js.
- Dynamically updates based on graph data and deadlock information.

### 4. **ChartPanel.js**
- Provides additional insights into the graph using React Chart.js components.
- Displays process/resource distribution and edge/deadlock counts.

### 5. **AuthContext.js**
- Provides authentication context for managing user login and logout.
- Handles token storage and decoding.

### 6. **Login.js**
- A form for user login.
- Sends credentials to the backend and stores the JWT token on success.

### 7. **Register.js**
- A form for user registration.
- Allows users to create new accounts.

---

## Styling

- The application uses CSS for styling, with styles defined in `styles.css`.
- Additional styles for specific components are included in their respective files.
- Charts and graphs are styled for a clean and modern look.

---

## API Integration

The frontend communicates with the backend via RESTful APIs and WebSocket (Socket.IO) for real-time updates. Key API endpoints include:
- **Authentication**: `/register`, `/login`
- **Graph Operations**: `/add_node`, `/remove_node`, `/add_edge`, `/remove_edge`
- **Analytics**: `/get_statistics`, `/check_deadlock`, `/get_deadlock_details`
- **Save/Load**: `/save_graph`, `/load_graph`
- **Position Updates**: `/update_position`

---

## Testing

- Unit tests are written using the React Testing Library.
- Run tests with:
  ```bash
  npm test
  ```

---

## Notes

- Ensure the backend server is running at `http://localhost:5000` for the frontend to function correctly.
- Update the API base URL in case the backend is hosted on a different domain or port.

