import React from 'react'

class ExampleApplication extends React.Component {

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

ExampleApplication.propTypes = {
}

ExampleApplication.defaultProps = {
}

export default ExampleApplication;
