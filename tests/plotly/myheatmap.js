/* A wrapper class for the Plotly chart 'heatmapgl'.
Based off of the animation examples from the plotly.js websites
Requests data from a server and adds to graph
*/


/* import a script with the given filename*/
function importScript( filename ){
    var imported = document.createElement('script');
    imported.src = filename;
    document.head.appendChild(imported);
    
}

/* Load the formats */
importScript( 'myheatmap.formats.js' );
importScript( "plotly-latest.min.js" );
//importScript( "jquery-3.1.1.min.js" );

class MyHeatmap{
    
    constructor( _div, _url ){
        

        
        /* The id of the div which will contain the heatmap */
        this.div = _div;
        this.url = _url;
        
        this.downloadData( 1 );
    }
    
    downloadData( layers, callback = "hm.renderHeatmap" ){
        
        /* make asynchronous call */
        /* 'JSON Padded' Cross-origin Ajax request to the server */
        $.ajax({
            url: this.url,
            dataType: "jsonp",
            data: { layers: layers},
            jsonpCallback: callback,
        });
        
    }
    
    renderHeatmap( json ){
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
        Plotly.plot(this.div, trace, layout,  {scrollZoom: false, staticPlot:false, displayModeBar: false, showLink:false});

        if ( json.salts.length > 1) {

            this.addFrames( json );
        } else {
            /* download the rest of the data */
            this.downloadData( 40, "hm.addFrames" );
        }
        
        this.bindEventListeners();
        this.play();
    }
    
    /* Bind plotly event listeners*/
    bindEventListeners(){
        
        function stringify( obj ){
            var props = "{"
            if (obj !== null) { 
                for (var propertyname in obj) {
                    props = props + propertyname + ", ";
                }
            }

            return props + "}"         
        }
        
        var myPlot = document.getElementById( this.div )
        var plotData = myPlot.data;
        console.log( stringify( myPlot.data ) );
        
        myPlot.on('plotly_restyle', function(){
            console.log("restyle");
        });
        
        myPlot.on('plotly_relayout', function(data){
            console.log("relayout traces:" );
        });
        
        /* No data provided */
        myPlot.on('plotly_animated', function(  data ){           
            console.log("animated " + stringify( plotData ));
            
        });
        
        myPlot.on('plotly_redraw', function(){
            console.log("redraw");
        });
        
        myPlot.on('plotly_afterplot', function(){
            console.log("afterplot");
        });
    }
    
    play(){
        
        /* Begin with initial animation */
        Plotly.animate(this.div, null, updatemenus[0]['buttons'][0]['args'][1]);
    }
    
    addFrames( json ){
        var salts = json.salts;
        
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
                /* method:'playFrame',
                args : [i] */
                
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
