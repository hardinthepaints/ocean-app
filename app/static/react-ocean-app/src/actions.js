import fetch from 'isomorphic-fetch'

/*
 *Actions
 */

export const REQUEST_DATA = "REQUEST_DATA";
export const RECEIVE_DATA = "RECEIVE_DATA";
export const RECEIVE_FAILURE = "RECEIVE_FAILURE"
export const SET_CURRENT = "SET_CURRENT";
export const PLAYPAUSE_PRESS = "PLAYPAUSE_PRESS";
export const SCRUBBER = "SCRUBBER";
export const RANGE = "RANGE"
export const SPEED_SLIDER = "SPEED_SLIDER"
export const COLOR_RANGE = "COLOR_RANGE"
export const ARROW = "ARROW"
export const VARIABLE_SELECT ="VARIABLE_SELECT"



/* Async action creators */

function checkStatus(response){
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

function fetchData(url = "http://localhost:5000/oceanapp/v1.0/json", username="xman", password="el33tnoob" ){

    const init ={
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                "Authorization": "Basic " + btoa(username + ":" + password)
            },
    }


    return dispatch => {
        dispatch( requestData() );
        return fetch( url, init )
            .then(checkStatus)
            .then( response => response.json() )
            .then(json => dispatch( receiveData(json)))
            /* .catch((err) => dispatch( receiveFailure()) ); */

    }
}

function receiveFailure(){
    return {
        type:RECEIVE_FAILURE
    }
}

function shouldFetchData(frames){
    return frames === null || frames.length ===0
}


/* Synchronous action creators */
export function fetchDataIfNeeded() {

    return (dispatch, getState) => {

        if (shouldFetchData(getState().frames)) {
            return dispatch( fetchData() )
        }

    }
}

export function requestData(){
    return {
        type : REQUEST_DATA,
    }
}

export function receiveData(json){
    return {
        json : json,
        type : RECEIVE_DATA,
    }
}

export function playPausePress(){
    return {
        type : PLAYPAUSE_PRESS,
    }
}

export function setCurrentFrame( frame, animationRequestID = null ){
    return {
        type : SET_CURRENT,
        animationRequestID : animationRequestID,
        frame : frame,
    }
}

export function scrubber( frame, range ){
    return {
        type : SCRUBBER,
        frame : frame,
    }
}

export function range( range ){

    return {
        type : RANGE,
        range : range,
    }
}

export function speedSlider( speed ){
    return {
        type : SPEED_SLIDER,
        speed : speed
    }
}

export function colorRange(range){
    return {
        type:COLOR_RANGE,
        range:range
    }
}

export function arrow(frame){
    return {
        type : ARROW,
        frame:frame
    }
}

/**modeSelect
 *  change the dataset
 */
export function variableSelect(variable){
    return {
        type:VARIABLE_SELECT,
        variable
    }
}
