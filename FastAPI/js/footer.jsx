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
      <footer className="bg-dark text-white pt-4 p-2" id="main-footer">
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
