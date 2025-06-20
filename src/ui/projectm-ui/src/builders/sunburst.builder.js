import * as d3 from "d3";

function buildDimensions() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const r = 350;

  const dims = { r: r, w: w, h: h };

  return dims;
}

export function buildSunburstSvg(data) {
  const dims = buildDimensions();

  // Specify the chart’s colors and approximate radius (it will be adjusted at the end).
  const color = d3.scaleOrdinal(
    d3.quantize(d3.interpolateRainbow, data.children.length + 1)
  );

  const width = dims.w;
  const height = dims.h;
  const radius = dims.r;

  // Prepare the layout.
  const partition = (data) =>
    d3.partition().size([2 * Math.PI, radius])(
      d3
        .hierarchy(data)
        .sum((d) => d.risk_impact)
        .sort((a, b) => b.value - a.value)
    );

  const arc = d3
    .arc()
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005))
    .padRadius(radius / 2)
    .innerRadius((d) => d.y0)
    .outerRadius((d) => d.y1 - 1);

  const root = partition(data);

  // Create the SVG container.
  const svg = d3
    .create("svg")
    .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`);

  // Add an arc for each element, with a title for tooltips.
  const format = d3.format(",d");
  svg
    .append("g")
    .attr("fill-opacity", 0.6)
    .selectAll("path")
    .data(root.descendants().filter((d) => d.depth))
    .join("path")
    .attr("fill", (d) => {
      while (d.depth > 1) d = d.parent;
      return color(d.data.title);
    })
    .attr("d", arc)
    .append("title")
    .text(
      (d) =>
        `${d
          .ancestors()
          .map((d) => d.data.title)
          .reverse()
          .join("/")}\n${format(d.value)}`
    );

  // Add a label for each element.
  svg
    .append("g")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .attr("font-size", 10)
    .attr("font-family", "sans-serif")
    .selectAll("text")
    .data(
      root
        .descendants()
        .filter((d) => d.depth && ((d.y0 + d.y1) / 2) * (d.x1 - d.x0) > 10)
    )
    .join("text")
    .attr("transform", function (d) {
      const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
      const y = (d.y0 + d.y1) / 2;
      return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
    })
    .attr("dy", "0.35em")
    .text((d) => d.data.title);

  return svg.node();
}
