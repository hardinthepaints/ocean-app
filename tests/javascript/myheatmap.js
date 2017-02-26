
/* Load the formats */
var imported = document.createElement('script');
imported.src = 'myheatmap.formats.js';
document.head.appendChild(imported);


/* Render a plotly heatmap with one frame of data */
function heatmap( div, json ) {
    
    var parsedJSON = parseJSON( json );
    
    
    
    /* Initial data Data */
    var trace = [
        {
            z: parsedJSON.salts[0],
            x: parsedJSON.lonp,
            y: parsedJSON.latp,
            
            type: 'heatmap',
            text: Array(parsedJSON.salts[0].length).fill("Rendered with plotly"),
            colorscale: 'Jet',
            opacity: 1,
            reversescale: false,
            name:'trace0' 
        }
    ];
    

    /* Plot and animate the data */
    Plotly.plot(div, trace, layout,  {scrollZoom: true});

    
    
    
    return parsedJSON.salts;
    
}


function flipTraces(){
    console.log("flip traces")
    
    var update = {
        visible: [false, true]
    };
    
    Plotly.moveTraces( "myTraces", 0);
    

    
    Plotly.restyle("myTraces", update, [0, 1])

}

/* Checks whether HTML5 Web Workers are supported in this browser */
function workerSupported(){
    if (typeof(Worker) !== "undefined") {
        //worker is supported!
        return true;
    } else {
        //worker not supported
        return false;
    }
    
}


function addTrace( i, parsedJSON ){
    
    var newData = [{
        x: parsedJSON.lonp,
        y: parsedJSON.latp,
        z:parsedJSON.salts[30],
        
        type: 'heatmap',
        text: Array(parsedJSON.salts[0].length).fill("trace1"),
        colorscale: 'Jet',
        opacity: 1,
        reversescale: false,
        name:'trace1',
        visible:true
    }];
    
    newData[0].z = parsedJSON.salts[i];

    Plotly.addTraces("myTraces", newData, 0)
    i = i +1;
    
    if (i < 39) {
        setTimeout( addTrace( i, parsedJSON ),500);
    }
}

/* Render plotly heatmap and animate multiple frames of data */
function animateHeatmap( div, json ) {

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
            xanchor: 'right', prefix: 'frame: ',font: {color: '#888',size: 20}
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
                text: Array(salts[i].length).fill("Plotly animate()"),
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

    /* Begin with initial animation */
    Plotly.animate(div, null, updatemenus[0]['buttons'][0]['args'][1]);
    
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

/* Trim the data to fit in the heatmap
Makes a 2d array 1 less in each of its dimensions
so if the input is an array 2x4, then the output is a 1X3,
with the last row/column sliced off
*/
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



    
