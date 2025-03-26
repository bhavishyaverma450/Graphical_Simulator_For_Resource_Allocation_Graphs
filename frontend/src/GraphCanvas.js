// frontend/src/GraphCanvas.js
import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import axios from "axios";
import contextMenus from "cytoscape-context-menus";
import "cytoscape-context-menus/cytoscape-context-menus.css";

cytoscape.use(contextMenus);

function GraphCanvas({ graphData }) {
  const cyRef = useRef(null);

  useEffect(() => {
    if (!graphData.nodes || !graphData.edges) {
      console.error("Graph data is empty or invalid.");
      return;
    }

    // Initialize Cytoscape Graph
    cyRef.current = cytoscape({
      container: document.getElementById("cy"),
      elements: [
        // Map nodes from graphData
        ...graphData.nodes.map((node) => ({
          data: { id: node.id, label: node.name, type: node.type },
          position: node.position || { x: Math.random() * 500, y: Math.random() * 500 },
          classes: node.type === "process" ? "process-node" : "resource-node",
        })),
        // Map edges from graphData
        ...graphData.edges.map((edge) => ({
          data: { id: `${edge.source}-${edge.target}`, source: edge.source, target: edge.target },
        })),
      ],
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#4caf50",
            label: "data(label)",
            width: 40,
            height: 40,
            "text-valign": "center",
            "text-halign": "center",
            "text-outline-width": 1,
            "text-outline-color": "#fff",
            color: "#000",
            "font-size": "12px",
          },
        },
        {
          selector: ".process-node",
          style: { "background-color": "#4caf50" },
        },
        {
          selector: ".resource-node",
          style: { "background-color": "#ff9800" },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#ccc",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#ccc",
          },
        },
      ],
      layout: {
        name: "grid",
        fit: true,
      },
    });

    // Enable Drag-and-Drop
    cyRef.current.on("dragfreeon", "node", async (event) => {
      const node = event.target;
      const newPos = node.position();

      // Send updated position to backend
      try {
        await axios.post("http://localhost:5000/update_position", {
          id: node.id(),
          position: newPos,
        });
        console.log(`Node ${node.id()} position updated.`);
      } catch (error) {
        console.error("Error updating node position:", error);
      }
    });

    // Add/Remove Nodes on Double-Click
    cyRef.current.on("dblclick", (event) => {
      const position = event.position;
      const id = `node-${Date.now()}`;
      cyRef.current.add({
        group: "nodes",
        data: { id, label: `New Node ${id}` },
        position,
      });

      console.log("Node added:", id);
    });

    // Context Menu for Deleting Nodes/Edges
    cyRef.current.contextMenus({
      menuItems: [
        {
          id: "delete",
          content: "❌ Delete",
          selector: "node, edge",
          onClick: function (event) {
            const target = event.target;
            target.remove();
            console.log(`Deleted: ${target.id()}`);
          },
        },
      ],
    });

    // Cleanup on Unmount
    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [graphData]);

  return <div id="cy" className="graph-canvas" />;
}

export default GraphCanvas;

