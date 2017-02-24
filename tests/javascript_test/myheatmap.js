


/* Make a plotly heatmap in the given div with the given json data*/
function makeHeatmap( div, json ) {
    
    var salt = json.salt;
    var latp = json.latp;
    var lonp = json.lonp;
    var list = [];
    
    /* Display the data */            
    salt = salt.slice(0, -1);
    var i;
    for (i = 0; i < salt.length; i ++){
        salt[i] = salt[i].slice(0, -1);
        
    }

    /* Data */
    var data = [
        {
            z: [].concat.apply([], salt),
            x: [].concat.apply([], lonp),
            y: [].concat.apply([], latp),
            
            type: 'heatmap',
            colorscale: 'Jet',
            reversescale: false,
            
        }
    ];
    
    var axisTemplate = {
        autorange: true,
        showgrid: true,
        zeroline: false,
        gridwidth: 2,
        linecolor: 'black',
        showticklabels: true,
        ticks: '',
        title: 'latitude'
    };
    
    var layout = {
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
        width: 600,
        height: 600,
        autosize: false
    };
    
    Plotly.newPlot(div, data, layout);
}

