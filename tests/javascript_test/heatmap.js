


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

    
    console.log(salt[0].length * salt.length);
    console.log(lonp[0].length * latp.length);

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
          t: 200,
          r: 200,
          b: 200,
          l: 200
        },
        yaxis: axisTemplate,
        xaxis: Object.assign({}, axisTemplate, {title:'longitude'}),

        showlegend: false,
        width: 800,
        height: 800,
        autosize: false
    };
    
    Plotly.newPlot(div, data, layout);
}

