import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

class Team extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Team: this.props.team,
      Info: {},
      Rounds: [],
    };
    console.log(this.props);
  };

  componentDidMount() {
    fetch('/api/team/'.concat(this.state.Team))
    .then(response => response.json())
    .then(data => {
      this.setState({ Info: data[0] });
    });

    fetch('/api/team/'.concat(this.state.Team, '/rounds'))
    .then(response => response.json())
    .then(data => {
      this.setState({ Rounds: data });
    });
  };

  render() {
    console.log(this.state);
    return (
      <section id="team">
        <div className="container">
          <div className="row">
            <div className="col">
              <div className="card my-3">
                <div className="card-head">
                  <h2 className='text-center'>
                    <span className='bg-warning px-4 rounded'>{this.state.Info['name']}</span>
                  </h2>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-sm-3 border-right">
                      <span class='font-weight-bold p-1'>Rating</span> {this.state.Info['elo']}
                    </div>
                    <div class="col-sm-3 border-right">
                      <span class='font-weight-bold p-1'>Variance</span> {this.state.Info['glicko']}
                    </div>
                    <div class="col-sm-3 border-right">
                      <span class='font-weight-bold p-1'>Side 1</span> {this.state.Info['side_1']}
                    </div>
                    <div class="col-sm-3">
                      <span class='font-weight-bold p-1'>Side 2</span> {this.state.Info['side_2']}
                    </div>
                  </div>
                  <table className="table table-striped my-4">
                    <thead className="thead-dark">
                      <tr>
                        <th>Team 1</th>
                        <th>Team 2</th>
                        <th>Wins</th>
                        <th>Rounds</th>
                      </tr>
                    </thead>
                    <tbody>
                      {this.state.Rounds.map(Team => (
                        <tr>
                          <td><a href={'/teams/'.concat(Team['team_1'])}>{Team['name1']}</a> ({Team['elo1']})</td>
                          <td><a href={'/teams/'.concat(Team['team_1'])}>{Team['name1']}</a> ({Team['elo2']})</td>
                          <td>{Team['result']}</td>
                          <td>{Team['rounds']}</td>
                        </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  };
};
Team.propTypes = {
  team: PropTypes.string.isRequired,
};
const Tem = document.getElementById('team');
if (Tem)
{
  ReactDOM.render(
    <Team team={document.getElementById('teamId').innerHTML} />, Tem
  );
}
