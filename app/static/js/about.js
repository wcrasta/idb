'use strict';
import ReactDOM from 'react-dom'
import React from 'react'
import ExampleApplication from './ExampleApplication'

class Kaivan extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
    	imgSrc: '../static/images/kaivan.jpeg'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/flash.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/kaivan.jpeg'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}

ReactDOM.render(
  <Kaivan/>, document.getElementById('kaivan-image')
);

class Kaden extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       imgSrc: '../static/images/kaden.png'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/batman.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/kaden.png'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}


ReactDOM.render(
  <Kaden/>, document.getElementById('kaden-image')
);

class Zihao extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       imgSrc: '../static/images/zihao.png'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/superman.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/zihao.png'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}


ReactDOM.render(
  <Zihao/>, document.getElementById('zihao-image')
);

class Warren extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       imgSrc: '../static/images/warren.png'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/aquaman.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/warren.png'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}


ReactDOM.render(
  <Warren/>, document.getElementById('warren-image')
);

class Colin extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       imgSrc: '../static/images/colin.png'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/cyborg.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/colin.png'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}


ReactDOM.render(
  <Colin/>, document.getElementById('colin-image')
);

class Anurag extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       imgSrc: '../static/images/anurag.png'
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
  }

  handleMouseOver() {
    this.setState({
      imgSrc: '../static/images/greenLantern.jpg'
    });
  }

  handleMouseOut() {
    this.setState({
      imgSrc: '../static/images/anurag.png'
    });
  }

  render() {
    return (
      <div>
        <img onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.imgSrc}/>
      </div>
    );
  }

}


ReactDOM.render(
  <Anurag/>, document.getElementById('anurag-image')
);