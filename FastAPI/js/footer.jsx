import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

class Footer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  };

  render() {
    return (
      <footer className="bg-dark text-white mt-5 p-5" id="main-footer">
        <div className="container">
          <div className="row">
            <div className="col">
              <p className="lead text-center">
                Copyright &copy; <span id="year"></span> Elo Rating Calculations
              </p>
            </div>
          </div>
        </div>
      </footer>
    );
  };
};

Footer.proptypes = {};
const Foot = document.getElementById('footer');
if (Foot)
{
  ReactDOM.render(
    <Footer/>, Foot
  );
}
