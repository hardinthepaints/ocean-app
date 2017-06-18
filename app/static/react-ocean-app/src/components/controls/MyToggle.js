/* Wrapper for react bootstrap toggle */

import React, { Component, PropTypes } from 'react';

import Toggle from 'react-bootstrap-toggle';

/* import the css styling for the toggle supplied by bootstrap */
import 'react-bootstrap-toggle/dist/bootstrap2-toggle.css'

const PAUSE = React.createElement("strong",{},"| |");
const PLAY =  React.createElement("x",{},"\u25B6");

class MyToggle extends Component {
  
  render() {
    
    return (
      
      <Toggle
        onClick={this.props.onClick}
        on={ this.props.active ? this.props.active : PAUSE }
        off={ this.props.inactive ? this.props.inactive : PLAY }
        size={"lg"}
        active={this.props.value}


      />

        
    );
  
        {}
  
  }

}

MyToggle.PropTypes = {
  onClick:PropTypes.func.isRequired,
  value:PropTypes.bool.isRequired
}

module.exports = MyToggle;
