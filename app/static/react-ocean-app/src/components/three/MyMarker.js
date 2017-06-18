/** Wrapper class for a three boxGeometry which serves a marker in the visualization
 *
 */

import React, {PropTypes} from 'react';

import React3 from 'react-three-renderer';
import * as THREE from 'three';



function MyMarker(props)  {
    
    const {wireframe, position, color} = props;

    return(
        
        <mesh
            position={position}
        >
            <boxGeometry
                width={1}
                height={1}
                depth={1}
            />
            
            <meshPhongMaterial
                wireframe={wireframe}
                vertexColors={THREE.FaceColors}
                color={new THREE.Color(color)}
                emissiveIntensity={20}
            />
        </mesh>                      

        
    );
    
}

PropTypes.MyMarker = {
    wireframe:PropTypes.bool.isRequired,
    position: PropTypes.isRequired,
    color:PropTypes.string.isRequired
}

module.exports = MyMarker;