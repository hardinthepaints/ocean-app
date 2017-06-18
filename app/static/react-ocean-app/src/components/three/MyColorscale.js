import * as THREE from 'three';

import colors from '../../containers/Colors.json'
const {maxSaltColor} = colors;

function createColorscale() {
    
    const colorScaler = function(value){
        
        const purple = new THREE.Color(maxSaltColor)
        purple.multiplyScalar(value)
        
        //console.log(purple)
        return purple.getHex();
    }
    
    return colorScaler;
   
}

module.exports = createColorscale