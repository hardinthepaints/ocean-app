import {Button, ButtonGroup, ButtonToolbar} from 'react-bootstrap'
import React, {PropTypes} from 'react';

import colors from '../../containers/Colors.json'

const VAR_SALT = "salt"
const VAR_TEMP = "temp"

function MyButtonGroup(props){
    const {onClick, currentVariable} = props
    return(
        <div className="Wrap">
            <ButtonToolbar>
                <ButtonGroup   bsSize="large">
                    <Button className={"SmallGrayFont"} onClick={()=>onClick(VAR_SALT)} active={currentVariable===VAR_SALT}>Salt</Button>{' '}
                    <Button className={"SmallGrayFont"} onClick={()=>onClick(VAR_TEMP)} active={currentVariable===VAR_TEMP}>Temp</Button>{' '}
                    {/*<Button className={"SmallGrayFont"} onClick={()=>onClick(2)} active={mode===2}>Right</Button>*/}
                </ButtonGroup>
            </ButtonToolbar>
        </div>
    );

}

module.exports = MyButtonGroup