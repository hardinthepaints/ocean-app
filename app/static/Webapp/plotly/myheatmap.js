/* A wrapper class for the Plotly chart 'heatmapgl'.
Based off of the animation examples from the plotly.js websites
*/

class MyHeatmap{
    
    constructor( div, height ){
        
        /* Bind functions which will be accessed outside of variable */
        this.initHeatmap = this.initHeatmap.bind( this )
        this.addFrames = this.addFrames.bind( this )
        this.bindEventListeners = this.bindEventListeners.bind( this )
        this.play = this.play.bind( this )



        /* define sliders */    
        this.sliders = [{
            pad: {t: 30},
            currentvalue: {
                xanchor: 'right', prefix: 'frame: ',font: {color: '#888',size: 20}
            },
            
        }];
    
        /* The id of the div which will contain the heatmap */
        this.div = div;
        
        /* set the height */
        layout.height = height;
        
    }
    
    /* Initially plot the map with one frame of data */
    initHeatmap( json ){
        
        
        console.time("initHeatmap")
        var z = json[0].z;
        
        /* Initial data Data */
        var trace = [
            {
                z: z,
                /* x: json.lonp,
                y: json.latp, */
                hoverinfo:"z+text",            
                type: 'heatmapgl',
                colorscale: 'Jet',
                opacity: 1.0,
                reversescale: false,
                name:'trace0',
                connectgaps: false,
                zsmooth:"fast",
                zauto:false,
                /* zmin:15,
                zmax:33,  */
            }
        ];
        
        /* set the width */
        layout.width = json.ratio * layout.height;
        layout.margin = {
                t: 100,
                r: 100 * json.ratio,
                b: 100,
                l: 100 * json.ratio,
        }
        
        /* Initinally plot an empty heatmap */
        Plotly.plot(this.div, trace, layout,  {scrollZoom: false, staticPlot:false, displayModeBar: false, showLink:false});
        
        console.timeEnd("initHeatmap")
        
        console.time("addFrames")
        this.addFrames( json.slice(1) )
        console.timeEnd("addFrames")

        
        /* Bind the event listeners */
        this.bindEventListeners();
        
    }
           
    /* Play through the frames */
    play(){
        
        frames = Array.apply(null, Array(71)).map(function (_, i) {return i;});

        
        /* Begin with initial animation */
        Plotly.animate(this.div, frames, updatemenus[0]['buttons'][0]['args'][1]);
    }
    
    /* Add frames to the plot and animate */
    addFrames( json ){
                    
        /* Make the frames to animate */        
        var processedFrames = [];
        
        //Object.keys( json.frames ).map( function( key, index ){
        json.map( function( frame, key ){
          
            processedFrames.push( {
                name: "" + key,
                data: [{
                    z: frame.z,
                }],
                traces: [0],
            } );
        });
        
        /* Add and animate frames */
        Plotly.addFrames( this.div, processedFrames );
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
        
        function loop(data) {
            console.log("animated " + stringify( plotData ));
            console.log( "this:" + Object.keys( this ) );
        }
        
        /* No data provided */
        myPlot.on('plotly_animated', this.play);
        
        myPlot.on('plotly_redraw', function(){
            console.log("redraw");
        });
        
        myPlot.on('plotly_afterplot', function(){
            console.log("afterplot");
        });
    }
    
    
}
