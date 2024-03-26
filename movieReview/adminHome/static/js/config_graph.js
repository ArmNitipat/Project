const config = {
    type: 'line',
    data: data,
    options: {
      responsive: true,
      interaction: {
        intersect: false,
        axis: 'x'
      },
      plugins: {
        title: {
          display: true,
          text: (ctx) => 'Step ' + ctx.chart.data.datasets[0].stepped + ' Interpolation',
        }
      }
    }
  };
// Path: movieReview/adminHome/static/js/config_graph.js