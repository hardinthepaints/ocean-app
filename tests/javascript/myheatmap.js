/* Plotly axis style */
const axisTemplate = {
    autorange: true,
    showgrid: true,
    zeroline: false,
    gridwidth: 2,
    linecolor: 'black',
    showticklabels: true,
    ticks: '',
    title: 'latitude'
};

const trans = {
    transition: {
        duration: 300,
        easing: "quadratic-in-out"
    },
    frame: {duration: 1000, redraw: true},
    mode:'next',
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
        "transition": {
          "duration": 300,
          "easing": "quadratic-in-out"
        },
        "frame": {
          "duration": 1000,
          "redraw": false
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
    width: 600,
    height: 600,
    autosize: false,
    
};



/* Render a plotly heatmap with one frame of data */
function heatmap( div, json ) {
    
    var parsedJSON = parseJSON( json );
    
    /* Initial data Data */
    var data = [
        {
            z: parsedJSON.salts[0],
            x: parsedJSON.lonp,
            y: parsedJSON.latp,
            
            type: 'heatmap',
            colorscale: 'Jet',
            reversescale: false,            
        }
    ];
    

    /* Plot and animate the data */
    Plotly.plot(div, data, layout,  {scrollZoom: true});
    
    return parsedJSON.salts;
    
}

/* Render plotly heatmap and animate multiple frames of data */
function animatedHeatmap( div, json ) {

    /* Plot and animate the data */
    var salts = heatmap( div, json )
    
    /* Only attempt to animate if there is enough frames*/
    if ( salts.length < 2 ) {
        return
    }
    
        
    frames = [];
    
    /* define slider */    
    var _sliders = [{
        pad: {t: 30},
        currentvalue: {
            xanchor: 'right',
            prefix: 'frame: ',
            font: {
            color: '#888',
            size: 20
            }
        },
    }];
    
    var _steps =[];
                
    /* Make the frames to animate */
    var i;
    for (var i = 0; i < salts.length; i ++){
                
        frames.push({
            name: "" + i,
            data: [{
                z: salts[i],
            }],
            traces: [0],
            layout:{
                title: "Salinity frame " + i,
            },
        });
        
        //make a new step for the slider
        _steps.push( {
            label : '' + i,
            method: 'animate',
            args: [["" + i], {
                mode: "immediate",
                transition: {"duration": 300},
                frame: {"duration": 300, "redraw": true}
            },
        ]
            
        })
        
    }
    
    
    _sliders[0].steps = _steps;
    
    /* Relayout to insert the sliders */
    Plotly.relayout( div, {sliders:_sliders, updatemenus : updatemenus})
    
    /* Add and animate frames */
    Plotly.addFrames( div, frames );

    /* Begin with the first frame */
    //Plotly.animate( div, null, trans );
    
}

/* determine if an object is a javascript array */
function isArray( obj ){
    if (obj.constructor === Array ) {
        return true;
    }
    return false;
}


/* Parse the json data into three arrays which plotly can use */
function parseJSON( json ){
    
    var salts = json.salts;
    var salt = salts[0];
    var latp = [].concat.apply([], json.latp);
    var lonp = [].concat.apply([], json.lonp);
    
    var i;
    for (i = 0; i < salts.length; i ++){
        salts[i] = trimData(salts[i]);
        
    }
    
    return {'salts':salts, 'latp':latp, 'lonp':lonp };
    
    
}

/* Trim the data to fit in the heatmap */
function trimData( data ){
    
    /* Display the data */            
    data = data.slice(0, -1);
    if ( !isArray( data[0] ) ) {
        //do not attempt to trim inner dimension if it does not exist
        //console.log( "data is not 2d array. type: " + data[0].constructor  )
    } else {
        var i;
        for (i = 0; i < data.length; i ++){
            data[i] = data[i].slice(0, -1);
            
        }
    }
    
    /* 'flatten' a 2d array into a 1d */
    return [].concat.apply([], data);
}


    
