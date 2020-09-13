import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

class Table extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Activity: this.props.activity,
      Season: this.props.season,
      Teams: [],
    };
  };

  componentDidMount() {
    fetch('/api/season/'.concat(this.state.Season).concat('/teams'))
    .then(response => response.json())
    .then(data => {
      this.setState({ Teams: data });
    });
  };

  render() {
    return (
      <section id="teams">
        <div class="container col-11">
          <div class="row">
            <div class="col">
              <div class="card">
                <table class="table table-striped">
                  <thead class="thead-dark">
                    <tr>
                      <th>Name</th>
                      <th>Elo</th>
                      <th>Glicko</th>
                      <th>Side 1</th>
                      <th>Side 2</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.Teams.map(Team => (
                      <tr>
                        <td>{Team['name']}</td>
                        <td>{Team['elo']}</td>
                        <td>{Team['glicko']}</td>
                        <td>{Team['side_1']}</td>
                        <td>{Team['side_2']}</td>
                      </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
};
Table.propTypes = {
  activity: PropTypes.number.isRequired,
  season: PropTypes.number.isRequired,
};
const Tab = document.getElementById('table');
if (Tab)
{
  ReactDOM.render(
    <Table activity={document.getElementById('activity').innerHTML} season={document.getElementById('season').innerHTML}/>, Tab
  );
}
