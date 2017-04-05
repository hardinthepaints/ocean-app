

function printSpeed( content_length, timeElapsed ){
    var size = "size: " + (content_length/(Math.pow(2,20))).toFixed(3) + " mb"
    var time = "download time elapsed:" + (timeElapsed/1000).toFixed(5) + " s"
    var speed = "speed: " + ((content_length/(Math.pow(2,20)))/(timeElapsed/1000)).toFixed(3) + " mb/s"
    
    console.log( "DOWNLOADED DATA:\n" + size + ",\n" + time + ",\n" + speed)
    

}
function downloadData( url, args, username="xman", password="el33tnoob" ){
    
    /* args as they pertain to the server
     * 'callback': the string name of the javascript function to call when this request is answered
    */
    
    /* Default args */
    var template = {callback:"hm.handleJSON"};
    
    /* Overwrite defaults if other values are provided.*/
    for (var attrname in args) { template[attrname] = args[attrname]; }
        
    var callback = template.callback;
    delete template.callback
    
    var start = performance.now();
                
    /* make asynchronous call */
    /* JSON Cross-origin Ajax request to the server */
    $.ajax({
        url: url,
        dataType: "json",
        data: template,
        success: (data, textStatus, jqXHR) => {
            printSpeed( jqXHR.getResponseHeader("Content-Length"), performance.now()-start );
            callback(data);
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
        },
    });   
    
}
