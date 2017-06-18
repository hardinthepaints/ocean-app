import React, { Component, PropTypes  } from 'react';

import ReactBootstrapSlider from 'react-bootstrap-slider';

import 'bootstrap-slider/dist/css/bootstrap-slider.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';



import './MySlider.css'
class MySlider extends Component {
    
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
            
            <ReactBootstrapSlider
            
                data-slider-rangeHighlights={[
                    { "start": 0, "end": 30 },
                ]}
                change={(result) => this.props.onChange(result.target.value)}
                /* onBeforeChange={this.props.onChange} */
                /* slideStop={this.props.onChange} */
                
                {...this.props}
                /* value={this.props.value}
                min={this.props.min}
                max={this.props.max} */
                handle={"square"}
                selection={"before"}
                
            />
        );
      
    }
}

MySlider.propTypes = {
    onChange:PropTypes.func.isRequired,
    value:PropTypes.oneOfType( [ PropTypes.array.isRequired, PropTypes.number.isRequired ] ),
    min:PropTypes.number.isRequired,
    max:PropTypes.number.isRequired,
}

export default MySlider;
