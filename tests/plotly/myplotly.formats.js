/* Plotly axis style */
const axisTemplate = {
    autorange: true,
    type:"linear",
    showgrid: true,
    zeroline: false,
    gridwidth: 2,
    linecolor: 'black',
    showticklabels: true,
    ticks: '',
    title: 'latitude',
    fixedrange:true,
};

/* json data for the play and pause buttons */


const updatemenus = [{
    "x": 0.1,
    "y": 0,
    "yanchor": "top",
    "xanchor": "center",
    "showactive": false,
    "direction": "right",
    "type": "buttons",
    "pad": {"t": 100, "r": 10},
    "buttons": [{
      "method": "animate",
      "args": [null, {
        "fromcurrent": true,
        "mode": "immediate",
        "transition": {
          "duration": 30,
        },
        "frame": {
          "duration": 30,
          "redraw":false,
          "relayout":false,
          
        }
      }],
      "label": "Play"
    }, {
      "method": "animate",
      "args": [
        [null],
        {
          "mode": "immediate",
          "transition": {
            "duration": 0
          },
          "frame": {
            "duration": 0,
            "redraw": false
          }
        }
      ],
      "label": "Pause"
    }]
}]
    
/* Layout of trace */
const layout = {
    title: 'Salinity',
    margin: {
      t: 100,
      r: 100,
      b: 100,
      l: 100
    },   
    yaxis: axisTemplate,
    xaxis: Object.assign({}, axisTemplate, {title:'longitude'}),

    showlegend: false,
    width: 700,
    height: 700,
    autosize: false,
    dragmode: "select",
};