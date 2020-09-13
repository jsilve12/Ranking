import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Activities: [],
    };
  };

  componentDidMount() {
    fetch('/api/activity', { method: 'GET', credentials: 'same-origin' })
    .then(response => response.json())
    .then(data => {
      this.setState({ Activities: data });
    });
  };

  render(){
    return(
      .
    )
  }
}
