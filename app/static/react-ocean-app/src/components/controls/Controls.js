import React from 'react';
import { Horizontal } from 'react-stack';

import MySlider from './MySlider'
import MyRange from './MyRange'
import MyToggle from './MyToggle'
import './Controls.css'
import KeyHandler, {KEYDOWN, KEYUP } from 'react-key-handler';
import MyButtonGroup from './MyButtonGroup'
import {Button} from 'react-bootstrap'

/* Logic for how the controls look */
function Controls(props){

    const{isPlaying, currentFrame, range, mapIsOn, colorRange, currentVariable} = props.ui;
    const {dateString} = props;


    return (
        <div className="Left">

            <div className="Wrap">

                {/*Bind space key to this button*/}
                <KeyHandler keyEventName={KEYUP} keyValue={" "} onKeyHandle={props.handleButtonClick}/>
                <KeyHandler keyEventName={KEYUP} keyValue={"Spacebar"} onKeyHandle={props.handleButtonClick}/>

                <MyToggle onClick={props.handleButtonClick} value={isPlaying}/>

            </div>

            {/*data readout*/}
            <div className="Wrap">
                <Horizontal alignItems={'center'} alignContent={'space-around'} >
                    <span className="SmallGrayFont" >{ dateString }</span>
                </Horizontal>
            </div>

            {/* Scrubber */}
            <div className="Wrap">

                <KeyHandler keyEventName={KEYDOWN} keyValue={"ArrowRight"} onKeyHandle={()=>{props.handleArrow(true)}}/>
                <KeyHandler keyEventName={KEYDOWN} keyValue={"ArrowLeft"} onKeyHandle={()=>{props.handleArrow()}}/>

            </div>

            <div className="Wrap">

                <MySlider onChange={props.handleChange} value={currentFrame} min={0} max={props.getMaxFrame()} />
            </div>


            {/* Range slider */}
            <div className="Wrap">
              <MySlider onChange={props.handleRangeChange} value={range} min={0} max={props.getMaxFrame()}  />
            </div>


            {/* Color Slider */}
            <div className="Wrap">
                <Horizontal alignItems={'center'} alignContent={'space-around'} >
                    <span className="SmallGrayFont" >{ "Color Limits" }</span>
                </Horizontal>
                <MySlider onChange={props.handleColorRange} value={colorRange} min={0} max={33}  />
            </div>

            <MyButtonGroup onClick={props.handleVariable} currentVariable={currentVariable}/>

        </div>

    );

}

module.exports = Controls;
