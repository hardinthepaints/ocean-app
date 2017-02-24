

function trimData( data ){
    
    /* Display the data */            
    data = data.slice(0, -1);
    var i;
    for (i = 0; i < data.length; i ++){
        data[i] = data[i].slice(0, -1);
        
    }
    
    return [].concat.apply([], data);
}


/* Make a plotly heatmap in the given div with the given json data*/
function makeHeatmap( div, json ) {
    
    var salts = json.salts;
    var salt = salts.pop(30);
    var latp = [].concat.apply([], json.latp);
    var lonp = [].concat.apply([], json.lonp);
    var list = [];
    
    salt = trimData( salt );

    /* Data */
    var data = [
        {
            z: salt,
            x: lonp,
            y: latp,
            
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
    
    
    frames = [];

    Plotly.plot(div, data, layout).then( function (){
            
        /* Make the frames to animate */
        var i;
        for (var i = 0; i < salts.length; i ++){
            frames.push({
                name: "" + i,
                data: [{
                    z: trimData(salts[i]),
                }],
                traces: [0],
                layout:{
                    title: "Salinity frame " + i,
                },
            });
            
            
        }

        Plotly.addFrames(div, frames.reverse());
        
        
        /* Animate through the frames one by one*/
        function animateFrame( frame ) {
            
            var trans = {
                transition: {
                    duration: 25,
                    easing: 'cubic-in-out'
                },
                frame: {duration: 250, redraw: true},
                mode:'next',
            };
            
            /* animate the frame */  
            Plotly.animate(div, [""+ frame], trans ).then(
                function () {
                
                    if ( frame < 38 ) {
                        animateFrame( frame + 1 )
                    } else {
                        
                        animateFrame( 0 )
                    }
                }
        
            );
            
        }
        
        /* Begin with the first frame */
        animateFrame(0);
        
        
        
                
        
            
        
        }                                      
    );
    
}


    
