/* A wrapper class for the Plotly chart 'heatmapgl'.
Based off of the animation examples from the plotly.js websites */


/* import a script with the given filename*/
function importScript( filename ){
    var imported = document.createElement('script');
    imported.src = filename;
    document.head.appendChild(imported);
    
}

class MyHeatmap{
    
    constructor( div, json ){
        
        /* Load the formats */
        importScript( 'myplotly.formats.js' );
        importScript( "plotly-latest.min.js" );
        
        this.div = div;
        
        this.renderHeatmap( div, json );     
    }
    
    renderHeatmap( div, json ){
        /* Initial data Data */
        var trace = [
            {
                z: json.salts[0],
                 /* x: json.lonp,
                y: json.latp, */
                
                /* xtype:"scaled",
                ytype:"scaled", */
                hoverinfo:"z+text",            
                type: 'heatmapgl',
                colorscale: 'Jet',
                opacity: 1,
                reversescale: false,
                name:'trace0',
                connectgaps: false,
                zsmooth:"fast",
            }
        ];
        
        layout.width = json.ratio * layout.height;
        layout.margin = {
                t: 100,
                r: 100 * json.ratio,
                b: 100,
                l: 100 * json.ratio,
            }
    
        /* Plot and animate the data */
        Plotly.plot(div, trace, layout,  {scrollZoom: false, staticPlot:false, displayModeBar: false, showLink:false});
        
        if ( json.salts.length > 1) {
            this.addFrames( json.salts );
            this.play()
            
        }
    }
    
    play(){
        
        /* Begin with initial animation */
        Plotly.animate(this.div, null, updatemenus[0]['buttons'][0]['args'][1]);
    }
    
    addFrames( salts ){
        
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
                }],
                traces: [0],
            });
            
            //make a new step for the slider
            
            var step = {
                label : '' + i,
                method: 'animate',
                args: [["" + i], {
                    mode: "next",
                    transition: {"duration": 30},
                    frame: {"duration": 30, "redraw": false}
                    },
                ]
                
            }
            
            _steps.push( step )
        }
        
        _sliders[0].steps = _steps;
        
        /* Relayout to insert the sliders */
        Plotly.relayout( this.div, {sliders:_sliders, updatemenus : updatemenus})
        
        /* Add and animate frames */
        Plotly.addFrames( this.div, frames );
            
    }
    
    
}
