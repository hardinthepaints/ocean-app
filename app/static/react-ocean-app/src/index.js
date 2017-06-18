/* required to use isomorphic-fetch : ensure you have a Promise polyfill */
import 'babel-polyfill'

import React from 'react';
import { render } from 'react-dom';
import Root from './containers/Root'


render(
  <div>
    <Root/>
  </div>,
  document.getElementById('root')
);
    



