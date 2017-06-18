import React from 'react';


var Loader = require('react-loader');

var MyLoader = React.createClass({
    render: function () {
        return (
            <Loader loaded={this.props.loaded} scale={3}>
            </Loader>
        );
    }
});

module.exports=MyLoader;