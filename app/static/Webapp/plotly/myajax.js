

/* import a script with the given filename*/
function importScript( filename ){
    var imported = document.createElement('script');
    imported.src = filename;
    document.head.appendChild(imported);
    
}

/* import jquery */
importScript( "jquery-3.1.1.min.js" );


/* Download a range of data frames using an ajax request */
function downloadData( url, args ){
            
    /* args as they pertain to the server
     * end: the last frame to return, (not inclusive)
     * start: the first frame to return (inclusive)
     * first: Boolean whether or not this is the first call
     * callback: the name of the javascript function to call when this request is answered
    */
    
    /* Default args */
    var template = {callback:"hm.handleJSON", end:1, start:0};
    
    for (var attrname in args) { template[attrname] = args[attrname]; }
        
    var callback = template.callback;
    delete template.callback
    
    console.log( template )
            
    /* make asynchronous call */
    /* 'JSON Padded' Cross-origin Ajax request to the server */
    $.ajax({
        url: url,
        dataType: "jsonp",
        data: template,
        jsonpCallback: callback,
    });
        
}