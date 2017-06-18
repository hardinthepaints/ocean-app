import React, {PropTypes, Component} from 'react';
import ReactDOM from 'react-dom'
import React3 from 'react-three-renderer';
import * as THREE from 'three';
import KeyHandler, {KEYUP } from 'react-key-handler';
import createColorscale from './MyColorscale'
import OrbitControls from './OrbitControls';
import MyMarker from './MyMarker'
import getPlaneFaces from './threeHelperFunctions'


import colors from '../../containers/Colors.json'
const landColor = new THREE.Color(colors.landColor);
const {markerColor} = colors;

class MyThree extends Component {


  constructor(props, context) {
        super(props, context);
        // construct the position vector here, because if we use 'new' within render,
        // React will think that things have changed when they have not.
        this.cameraPosition = new THREE.Vector3(0, 0, 300);
        this.lightPosition = new THREE.Vector3(100, 100, 300)


        this.colorscale = createColorscale()

        this.cachedFaces = {}

        this.state = {
            ...this.state,
            wireframe:false,
            groupRotation: new THREE.Euler(0, 0, 0),
            markerPosition:new THREE.Vector3(0, 0, 0)
        };


        //this.cameraPosition = new THREE.Vector3(0, 150, 500);
        this.planePosition = new THREE.Vector3(0, 0, 0);
        this.gridPosition = new THREE.Vector3(-0.5, 0, 1);

        this.targetRotationYOnMouseDown = 0;

        this.mouseX = 0;
        this.mouseXOnMouseDown = 0;
        this.targetRotationY = 0;

        //load a font
        var fontloader = new THREE.FontLoader();
        fontloader.load(
          './alex_brush_regular.js',
          (font) => {
            console.log("done loading font")
            console.log(font);
            this.font = font;
          }

        );



    }


    componentDidMount(){

        const container = this.refs.container;

        const {currentFrame, frames} = this.props

        const controls = new OrbitControls(this.refs.camera, ReactDOM.findDOMNode(this.refs.container))

        this.setState({
            controls:controls,

        });

        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        container.addEventListener( 'mousemove', this.onMouseMove, false );


        controls.rotateSpeed = 1.0;
        controls.zoomSpeed = 1.2;

        /* Initial draw */
        const plane = this.refs.plane
        this.assignColors(plane.faces, this.props)
        plane.colorsNeedUpdate = true
    }
    onMouseMove = ( event )=> {
    	// calculate mouse position in normalized device coordinates
    	// (-1 to +1) for both components

    	this.mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
    	this.mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;

    }

    /** componentWillReceiveProps
     *    occurs when a component receives new props
     */
    componentWillReceiveProps( nextProps ){
        const {currentFrame, frames, colorRange, currentVariable } = nextProps

          /* Reference the plane */
        const plane = this.refs.plane

        if ( frames.length > this.props.frames.length ||
            (frames.length > 0 &&
                (currentFrame !== this.props.currentFrame ||
                colorRange !== this.props.colorRange ||
                currentVariable !== this.props.currentVariable)
            )
        ) {
            /* Assign new colors to the plane */
            this.assignColors( plane.faces, nextProps )
            plane.colorsNeedUpdate = true

        }
    }

    /* given a value, Return a color in hex form */
    getColor =( value )=>{

        const {colorRange} = this.props;

        value = value - colorRange[0]
        value = value / (colorRange[1] - colorRange[0])
        value = Math.min( Math.max(0, value), 1)

        return this.colorscale(value )
    }

    /* Build a key for use in caching */
    buildFrameKey = ( currentFrame, colorRange, currentVariable ) => {
        return currentFrame + "_" + colorRange[0] + "_" + colorRange[1] + "_" + currentVariable
    }

    /* Cache an array of colors */
    cacheFace =(framekey,colors)=> {
        this.cachedFaces[framekey] = colors;

    }


    /**
     *Raycast the mouse position to find where it intersects with the plane.
     *Use that location to determine where the marker should be
    *
    */
    highlightMouseOver = (raycaster, mouse, camera, mesh) => {

      	// update the picking ray with the camera and mouse position
    	raycaster.setFromCamera( mouse, camera );

    	// calculate objects intersecting the picking ray
    	var intersects = raycaster.intersectObject( mesh );

        var point;
        if (intersects.length > 0) {
            point = intersects[0].point.round();

            /* Center the marker on the squares so it lines up perfectly with one quadrant of the data */
            point.z = .5
            point.x += .5

            this.setState({markerPosition:point});
        }
    }

    /**paintPlaneGeometry
    *   z values
    *   colors - if provided, then will not calculate them
    *   planeGeometryFaces - the array of faces to be painted
    */
    paintPlaneGeometry = ( zValues, colors, planeGeometryFaces ) => {
        var colorsProvided = false;
        var findColor;
        if (colors != null){
            colorsProvided=true;
            findColor = (currentFace) =>{
                return colors[currentFace/2];
            }
        } else {
            colors = new Array(zValues.length);
            findColor = (currentFace) => {
                var value = zValues[currentFace/2];
                var hex = (value !== null) ? this.getColor(value) : landColor.getHex();

                //store in cache
                colors[currentFace/2] = hex;
                return hex;
            }
        }

        var hexColor;
        for (var currentFace = 0; currentFace < zValues.length*2; currentFace+=2){
                hexColor = findColor(currentFace);
                for (var j = 0; j<2; j++){
                    planeGeometryFaces[currentFace+j].color.setHex( hexColor );
                }

        }

        return colors;
    }

    /* Assign colors based on the values in the props (z and colorRange) to the faces in the plane.
    *   cache the result of the calculation so it only has to be done once
    *   Also, the colors can be precalculated and cached if plane is null
    *   this method will only work if the plane is a geometry (not buffer)
    */
    assignColors = ( planeGeometryFaces, props ) => {
        const { colorRange, frames, currentFrame, currentVariable } = props

        var frameKey = this.buildFrameKey(currentFrame, colorRange, currentVariable  )

        const z = frames[currentFrame][currentVariable];

        var colors = null;
        if ( frameKey in this.cachedFaces ) {
            colors = this.cachedFaces[frameKey];
            this.paintPlaneGeometry(z, colors, planeGeometryFaces);
        } else {
            colors = this.paintPlaneGeometry(z, colors, planeGeometryFaces);
            this.cacheFace(frameKey, colors);
        }

    }

    /* Called when the three.js components decides it is time to animate */
    onAnimate=()=> {
        const camera = this.refs.camera
        const mesh = this.refs.mesh

        const plane = this.refs.plane

        /* Animate the marker */
        if(this.raycaster) this.highlightMouseOver(this.raycaster, this.mouse, camera, mesh)
        const {controls} = this.state
        if (controls) controls.update()

    }

    /**toggleWireframe
     *    change the state of this component to show wireframe in the three.js component
     */
    toggleWireframe = () => {
        this.setState({
            wireframe:!this.state.wireframe
        })
    }

    getTextLabel = () =>{
      return (
        <mesh
          position={this.state.markerPosition}

          >
          <textGeometry
            text={"label text"}
            font={this.font}
            size={300}
          />
        </mesh>
      );
    }

    render() {

        const {width,height,frames,currentVariable, isPlaying} = this.props;

        const {groupRotation,wireframe} = this.state;

        const z = frames[0][currentVariable];

        return (
            <div ref = "container">
                <KeyHandler keyEventName={KEYUP} keyValue={"w"} onKeyHandle={this.toggleWireframe}/>
                <React3
                    mainCamera="camera" // this points to the perspectiveCamera below
                    width={width}
                    height={height}
                    forceManualRender={false}
                    onManualRenderTriggerCreated={this.setTrigger}
                    onAnimate={this.onAnimate}
                >
                   <scene ref="scene">
                        <perspectiveCamera
                            ref="camera"
                            name="camera"
                            fov={75}
                            aspect={width / height}
                            near={0.1}
                            far={1000}
                            position={this.cameraPosition}
                            lookAt={this.planePosition}
                        />

                        <MyMarker position={this.state.markerPosition} wireframe={wireframe} color={markerColor}/>

                        {
                          (this.font !== undefined) ? this.getTextLabel() : false
                        }
                        <mesh
                            ref={"mesh"}
                            rotation={this.groupRotation}
                            position={this.planePosition}
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
                        <pointLight
                            position={this.lightPosition}
                       />
                   </scene>
               </React3>
           </div>

        );



    }
}

MyThree.propTypes = {
    frames:PropTypes.array.isRequired,
    currentFrame:PropTypes.oneOfType( [ PropTypes.string.isRequired, PropTypes.number.isRequired ] ),
    height:PropTypes.number.isRequired,
    width:PropTypes.number.isRequired,
    colorRange:PropTypes.array.isRequired,
    isPlaying:PropTypes.bool.isRequired,
    currentVariable:PropTypes.string.isRequired

}

export default MyThree;
