import { combineReducers } from 'redux';

import {
    PLAYPAUSE_PRESS,
    SCRUBBER,
    RANGE,
    SPEED_SLIDER,
    SET_CURRENT,
    RECEIVE_DATA,
    MODE_TOGGLE,
    COLOR_RANGE,
    ARROW,
    VARIABLE_SELECT
} from './actions'

function getCorrectFrame( frame, range ){
    frame = Math.max( frame, range[0] );
    frame = Math.min( frame, range[1]);
    return frame;

}

function currentFrame( state, action ){

    switch (action.type) {
        case RANGE:
            return getCorrectFrame( state.currentFrame, action.range );

        case SCRUBBER:
            return getCorrectFrame( action.frame, state.range );

        case ARROW:
        case SET_CURRENT:
            return getCorrectFrame( action.frame, state.range );

        default:
            return state.currentFrame;
    }
}

function animationRequestID( animationRequestID=null, action ){
    switch (action.type){
        case SET_CURRENT:
            return action.animationRequestID;
        default:
            return animationRequestID;
    }

}


function isPlaying( isPlaying, action ){

    switch (action.type){
        case PLAYPAUSE_PRESS:
            return !isPlaying
        case SCRUBBER:
            return false;
        case RECEIVE_DATA:
            return false;
        case COLOR_RANGE:
            return isPlaying;
        case ARROW:
            return false;
        default:
            return isPlaying

    }
}

function frames( state = [], action ){
    /* action = {hours, date}*/
    switch (action.type){
        case RECEIVE_DATA:
            return action.json;
        default:
            return state

    }
}

function range( state = [0,100], action){
    switch(action.type){
        case RANGE:
            return action.range
        case SCRUBBER:
            return [Math.min(state[0], action.frame), Math.max(state[1], action.frame)]
        case RECEIVE_DATA:
            return [ state[0], action.json.length -1 ];
        default:
            return state;
    }
}

function speed( state = 5, action){
    switch(action.type){
        case SPEED_SLIDER:
            return action.speed;
        default:
            return state;
    }
}

function colorRange(state, action){
    switch (action.type){
        case COLOR_RANGE:
            return action.range
        default:
            return state;
    }
}

/**currentVariable
 *which variable is currently being displayed
 */
function currentVariable(variable, action) {
    switch(action.type){
        case VARIABLE_SELECT:
            return action.variable;
        default:
            return variable;
    }
}

function ui(state={currentFrame:3, isPlaying:false, speed:70, range:[0,50], colorRange:[10,33], currentVariable:"salt"}, action ){

    return {
        currentFrame:currentFrame( state, action ),
        range:range(state.range, action),
        speed:speed(state.speed, action),
        isPlaying:isPlaying(state.isPlaying, action),
        animationRequestID:animationRequestID(state.animationRequestID, action),
        colorRange:colorRange(state.colorRange, action),
        currentVariable:currentVariable(state.currentVariable, action)
    }

}

const rootReducer = combineReducers({
    ui,
    frames,
})

export default rootReducer;
