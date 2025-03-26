// frontend/src/GraphStats.js
import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const GraphStats = ({ graphData, deadlockInfo }) => {
  const barChartRef = useRef(null);
  const pieChartRef = useRef(null);

  useEffect(() => {
    if (graphData.nodes.length > 0) {
      // Destroy previous charts if they exist
      if (barChartRef.current) {
        barChartRef.current.destroy();
      }
      if (pieChartRef.current) {
        pieChartRef.current.destroy();
      }

      // Data for Bar Chart (Processes & Resources)
      const processCount = graphData.nodes.filter(
        (node) => node[1].type === "process"
      ).length;
      const resourceCount = graphData.nodes.filter(
        (node) => node[1].type === "resource"
      ).length;

      // Bar Chart for Node Count
      const barCtx = document.getElementById("barChart").getContext("2d");
      barChartRef.current = new Chart(barCtx, {
        type: "bar",
        data: {
          labels: ["Processes", "Resources", "Edges"],
          datasets: [
            {
              label: "Graph Elements",
              data: [processCount, resourceCount, graphData.edges.length],
              backgroundColor: ["#4caf50", "#2196f3", "#ff9800"],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
          },
        },
      });

      // Pie Chart for Deadlock Summary
      const deadlockDetected = deadlockInfo?.deadlock ? 1 : 0;
      const noDeadlock = deadlockInfo?.deadlock ? 0 : 1;
      const pieCtx = document.getElementById("pieChart").getContext("2d");
      pieChartRef.current = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: ["Deadlock Detected", "No Deadlock"],
          datasets: [
            {
              data: [deadlockDetected, noDeadlock],
              backgroundColor: ["#f44336", "#4caf50"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" },
          },
        },
      });
    }
  }, [graphData, deadlockInfo]);

  return (
    <div className="chart-container">
      <h3>📊 Graph Statistics</h3>
      <div className="chart-wrapper">
        <canvas id="barChart" width="400" height="200"></canvas>
      </div>
      <h3>⚠️ Deadlock Overview</h3>
      <div className="chart-wrapper">
        <canvas id="pieChart" width="400" height="200"></canvas>
      </div>
    </div>
  );
};

export default GraphStats;
