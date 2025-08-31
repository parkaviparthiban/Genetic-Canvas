// DNA Visualizer using D3.js
document.addEventListener("DOMContentLoaded", function () {
  const sequence = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTA"; // Replace with dynamic input
  const container = d3.select("#dna-visualization");

  const width = 800;
  const height = 100;
  const nucleotideColors = {
    A: "#3498db",
    T: "#e74c3c",
    G: "#2ecc71",
    C: "#f1c40f"
  };

  const svg = container.append("svg")
    .attr("width", width)
    .attr("height", height);

  const xScale = d3.scaleLinear()
    .domain([0, sequence.length])
    .range([0, width]);

  svg.selectAll("rect")
    .data(sequence.split(""))
    .enter()
    .append("rect")
    .attr("x", (d, i) => xScale(i))
    .attr("y", 20)
    .attr("width", 20)
    .attr("height", 40)
    .attr("fill", d => nucleotideColors[d] || "#bdc3c7")
    .append("title")
    .text((d, i) => `Position ${i + 1}: ${d}`);
});