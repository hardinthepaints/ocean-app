import React, { Component, PropTypes  } from 'react';

import { Range } from 'rc-slider';
import './MySlider.css';

require('rc-tooltip/assets/bootstrap.css');




class MyRange extends Component {

    componentDidMount(){
        /* pass an initial value to the call back functions */
        const {value,onChange} = this.props
        onChange(value)
    }
    
    componentDidUpdate(prevProps){
        const {min, max, onChange, value} = this.props;
        if ( min !== prevProps.min || max != prevProps.max) {
            onChange(value)
        }
    }
    render() {
  
        return (
            
             <Range className={"rc-slider"}
                pushable={true}
                onChange={this.props.onChange}
                /* onBeforeChange={this.props.onChange} */
                onAfterChange={this.props.onChange}
                value={this.props.value}
                min={this.props.min}
                max={this.props.max}
             />    
        );
      
    }
}

MyRange.propTypes = {
    onChange:PropTypes.func.isRequired,
    value:PropTypes.array.isRequired,
    min:PropTypes.number.isRequired,
    max:PropTypes.number.isRequired,
}

export default MyRange;
