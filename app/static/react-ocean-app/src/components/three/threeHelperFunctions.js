import * as THREE from 'three';


function getPlaneFaces(props) {
    const {frames} = props;
    
    
    var width=frames[0].width
    var height=frames[0].height
    var widthSegments=frames[0].width
    var heightSegments=frames[0].height
    
    var plane = new THREE.PlaneGeometry(width, height, widthSegments, heightSegments)
    
    console.log(plane);
    
    return plane.faces;
}

module.exports = getPlaneFaces;


