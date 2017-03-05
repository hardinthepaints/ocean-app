/* A group of functions to create a plotly heatmap from oceanography data */


/* Load the formats */
importScript( 'myplotly.formats.js' );
importScript( "plotly-latest.min.js" );

/* import a script with the given filename*/
function importScript( filename ){
    var imported = document.createElement('script');
    imported.src = filename;
    document.head.appendChild(imported);
    
    
}

/* Render a plotly heatmap with one frame of data */
function heatmap( div, json ) {
        
    /* Initial data Data */
    var trace = [
        {
            z: json.salts[0],
            x: json.lonp,
            y: json.latp,            
            type: 'heatmapgl',
            colorscale: 'Jet',
            opacity: 1,
            reversescale: false,
            name:'trace0' 
        }
    ];   

    /* Plot and animate the data */
    Plotly.plot(div, trace, layout,  {scrollZoom: false, staticPlot:true, displayModeBar: false, showLink:false});
    
    return json.salts;

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
    
    /* The 'steps' of the slider */
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
        });
        
        //make a new step for the slider
        _steps.push( {
            label : '' + i,
            method: 'animate',
            args: [["" + i], {
                mode: "immediate",
                transition: {"duration": 0},
                frame: {"duration": 0, "relayout": true, "redraw": false}
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





    
