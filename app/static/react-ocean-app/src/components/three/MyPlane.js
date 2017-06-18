import React3 from 'react-three-renderer';
import * as THREE from 'three';

import React, {PropTypes, Component} from 'react';


class MyPlane extends Component{
    
    render(){
    
    const {frames, wireframe, position, rotation} = this.props;
    
        return(
            <mesh
                ref={"mesh"}
                rotation={rotation}
                position={position}
            >
                <planeGeometry
                    width={frames[0].width}
                    height={frames[0].height}
                    widthSegments={frames[0].width}
                    heightSegments={frames[0].height}
                    ref={"plane"}
    
                />
    
                <meshPhongMaterial
                    wireframe={wireframe}
                    vertexColors={THREE.FaceColors}
                />
            </mesh>
        );
    }
    
}

module.exports = MyPlane;