

/* import a script with the given filename*/
function importScript( filename ){
    var imported = document.createElement('script');
    imported.src = filename;
    document.head.appendChild(imported);
    
}

/* import jquery */
//console.log( "imported jquery" )

//importScript( "jquery-3.1.1.min.js" );


function downloadData( url, args, username="xman", password="el33tnoob" ){
    
    /* args as they pertain to the server
     * 'end': the last frame to return, (not inclusive)
     * 'start': the first frame to return (inclusive)
     * 'first': Boolean whether or not this is the first call
     * 'callback': the string name of the javascript function to call when this request is answered
     * example: var args = { start : 0, end : 30, first : true, callback: 'handleJSON' }
            //request the first 30 frames, this is the first request, and callback to handleJSON()
     * 
    */
    
    /* Default args */
    var template = {callback:"hm.handleJSON"};
    
    for (var attrname in args) { template[attrname] = args[attrname]; }
        
    var callback = template.callback;
    delete template.callback
                
    /* make asynchronous call */
    /* JSON Cross-origin Ajax request to the server */
    $.ajax({
        url: url,
        dataType: "json",
        data: template,
        success: callback,
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
    });   
    
}
