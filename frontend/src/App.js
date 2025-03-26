// frontend/src/App.js
import React, { useState, useEffect, useContext } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import axios from "axios";
import io from "socket.io-client";
import "./styles.css";
import GraphCanvas from "./GraphCanvas"; // Import GraphCanvas
import GraphStats from "./GraphStats"; // Import GraphStats
import Login from "./auth/Login"; // Import Login
import Register from "./auth/Register"; // Import Register
import { AuthContext, AuthProvider } from "./context/AuthContext"; // Import AuthContext

const socket = io("http://localhost:5000");

// Protected Route Component
const ProtectedRoute = ({ element }) => {
  const { user } = useContext(AuthContext);
  return user ? element : <Navigate to="/login" replace />;
};

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [nodeName, setNodeName] = useState("");
  const [nodeType, setNodeType] = useState("process");
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [deadlockInfo, setDeadlockInfo] = useState(null);
  const [error, setError] = useState("");
  const [saveLoadStatus, setSaveLoadStatus] = useState("");
  const [graphStats, setGraphStats] = useState(null); // New state for graph statistics
  const [deadlockDetails, setDeadlockDetails] = useState(null); // New state for deadlock details

  // Sync Graph State from Server on Socket Event
  useEffect(() => {
    socket.on("graph_update", (data) => {
      setGraphData(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Fetch Graph Data from Backend
  const fetchGraphData = async () => {
    try {
      const response = await axios.get("http://localhost:5000/get_graph");
      setGraphData(response.data);
      fetchGraphStats(); // Fetch statistics after graph update
    } catch (error) {
      console.error("Error fetching graph data:", error);
      setError("Unable to connect to the backend. Please check server status.");
    }
  };

  useEffect(() => {
    fetchGraphData();
  }, []);

  // Fetch Graph Statistics
  const fetchGraphStats = async () => {
    try {
      const response = await axios.get("http://localhost:5000/get_statistics");
      setGraphStats(response.data);
    } catch (error) {
      setError("Error fetching graph statistics.");
    }
  };

  // Fetch Deadlock Details
  const fetchDeadlockDetails = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/get_deadlock_details"
      );
      setDeadlockDetails(response.data);
    } catch (error) {
      setError("Error fetching deadlock details.");
    }
  };

  // Add Node
  const addNode = async () => {
    try {
      const token = localStorage.getItem("token");
      await axios.post(
        "http://localhost:5000/add_node",
        { name: nodeName, type: nodeType },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setNodeName("");
    } catch (error) {
      setError("Error adding node. Make sure the name is unique.");
    }
  };

  // Add Edge
  const addEdge = async () => {
    try {
      await axios.post("http://localhost:5000/add_edge", {
        source,
        target,
      });
      setSource("");
      setTarget("");
    } catch (error) {
      setError("Error adding edge. Check node names.");
    }
  };

  // Remove Node
  const removeNode = async () => {
    try {
      await axios.post("http://localhost:5000/remove_node", {
        name: nodeName,
      });
      setNodeName("");
    } catch (error) {
      setError("Error removing node. Node may not exist.");
    }
  };

  // Remove Edge
  const removeEdge = async () => {
    try {
      await axios.post("http://localhost:5000/remove_edge", {
        source,
        target,
      });
      setSource("");
      setTarget("");
    } catch (error) {
      setError("Error removing edge. Edge may not exist.");
    }
  };

  // Check Deadlock
  const checkDeadlock = async () => {
    try {
      const response = await axios.get("http://localhost:5000/check_deadlock");
      setDeadlockInfo(response.data);
    } catch (error) {
      setError("Error checking deadlock.");
    }
  };

  // Save Graph
  const saveGraph = async () => {
    try {
      const response = await axios.post("http://localhost:5000/save_graph");
      setSaveLoadStatus(response.data.status || "Graph saved successfully.");
    } catch (error) {
      setError("Error saving graph.");
    }
  };

  // Load Graph
  const loadGraph = async () => {
    try {
      const response = await axios.get("http://localhost:5000/load_graph");
      setSaveLoadStatus(response.data.status || "Graph loaded successfully.");
      fetchGraphData();
    } catch (error) {
      setError("Error loading graph.");
    }
  };

  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute
                element={
                  <div className="app-container">
                    <h1>⚡ Real-Time RAG Simulator with Authentication ⚡</h1>

                    {/* Error Display */}
                    {error && <p className="error">{error}</p>}
                    {saveLoadStatus && (
                      <p className="status">{saveLoadStatus}</p>
                    )}

                    {/* Add Node */}
                    <div className="form-container">
                      <h3>Add Node (Process/Resource)</h3>
                      <input
                        type="text"
                        value={nodeName}
                        onChange={(e) => setNodeName(e.target.value)}
                        placeholder="Node Name"
                      />
                      <select
                        value={nodeType}
                        onChange={(e) => setNodeType(e.target.value)}
                      >
                        <option value="process">Process</option>
                        <option value="resource">Resource</option>
                      </select>
                      <button onClick={addNode}>Add Node</button>
                      <button onClick={removeNode}>Remove Node</button>
                    </div>

                    {/* Add/Remove Edge */}
                    <div className="form-container">
                      <h3>Add/Remove Edge</h3>
                      <input
                        type="text"
                        value={source}
                        onChange={(e) => setSource(e.target.value)}
                        placeholder="Source"
                      />
                      <input
                        type="text"
                        value={target}
                        onChange={(e) => setTarget(e.target.value)}
                        placeholder="Target"
                      />
                      <button onClick={addEdge}>Add Edge</button>
                      <button onClick={removeEdge}>Remove Edge</button>
                    </div>

                    {/* Graph Visualization */}
                    <div className="graph-container">
                      <h3>Graph Overview</h3>
                      <GraphCanvas graphData={graphData} />
                    </div>

                    {/* Graph Statistics Section */}
                    {graphData.nodes.length > 0 && (
                      <div className="form-container">
                        <GraphStats
                          graphData={graphData}
                          deadlockInfo={deadlockInfo}
                        />
                      </div>
                    )}

                    {/* Save/Load Graph Controls */}
                    <div className="form-container">
                      <h3>Save/Load Graph</h3>
                      <button onClick={saveGraph}>💾 Save Graph</button>
                      <button onClick={loadGraph}>📂 Load Graph</button>
                    </div>
                  </div>
                }
              />
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;











