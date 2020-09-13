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
    fetch('/api/activity/', { method: 'GET', credentials: 'same-origin' })
    .then(response => response.json())
    .then(data => {
      this.setState({ Activities: data });
    });
  };

  render() {
    return (
      <nav className="navbar navbar-dark bg-dark">
        <div className="container">
          <a href="/1/1" class="navbar-brand bg-success text-dark rounded p-2">Ranking</a>
          <ul className='navbar-nav ml-auto'>
            {this.state.Activities.map(Activity => (
              <li className='nav-item'>
                <a href={'/'.concat(Activity['id']).concat('/1')} className="nav-link text-light">{Activity['name']}</a>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    );
  }
}
Navbar.propTypes = {};
const Nav = document.getElementById('navbar');
if (Nav)
{
  ReactDOM.render(
    <Navbar/>, Nav
  );
}
