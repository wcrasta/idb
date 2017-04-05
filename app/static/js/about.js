'use strict';
import ReactDOM from 'react-dom'
import React from 'react'
import ExampleApplication from './ExampleApplication'

var body = (<ExampleApplication/>);

ReactDOM.render(
  body,
  document.getElementById('change-image')
);
