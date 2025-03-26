// frontend/src/ChartPanel.js
import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import "chart.js/auto";

const ChartPanel = ({ statistics }) => {
  const pieData = {
    labels: ["Processes", "Resources"],
    datasets: [
      {
        data: [statistics.num_processes || 0, statistics.num_resources || 0],
        backgroundColor: ["#4caf50", "#f44336"],
      },
    ],
  };

  const barData = {
    labels: ["Edges", "Deadlocks"],
    datasets: [
      {
        label: "Count",
        data: [statistics.num_edges || 0, statistics.deadlock_count || 0],
        backgroundColor: ["#36a2eb", "#ff6384"],
      },
    ],
  };

  return (
    <div className="chart-panel">
      <h3>Graph Insights</h3>
      <div className="chart-container">
        <Pie data={pieData} />
        <Bar data={barData} />
      </div>
    </div>
  );
};

export default ChartPanel;
