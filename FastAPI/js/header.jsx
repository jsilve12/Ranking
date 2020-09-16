import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Title: this.props.title,
      Activity_Id: this.props.activity,
      Activity: '',
      Season: this.props.season,
      Seasons: [{ id: this.props.season }],
    };
  };

  componentWillMount() {
    fetch('/api/activity/'.concat(this.state.Activity_Id))
    .then(response => response.json())
    .then(data => {
      this.setState({ Activity: data['name'] });
    });

    fetch('/api/activity/'.concat(this.state.Activity_Id).concat('/season'))
    .then(response => response.json())
    .then(data => {
      this.setState({ Seasons: data });
    });
  };

  render() {
    return (



<section id="Header">
        <div className="container col-11">
          <div className="row">
            <div className="col">
              <h1 className='text-center mt-3 '>{ this.state.Activity } Ratings</h1>
              <div className='col-3-sm form-inline form-group'>
                <label for='season' className='text-right h5 p-2'>Season</label>
                <select
                  value={'/activity/'.concat(this.state.Activity_Id, '/', this.state.Season)}
                  className='form-control'
                  onChange={event => {location = event.target.value;}}>
                    {this.state.Seasons.map(Season => (
                      <option
                        id={'Season '.concat(Season['id'])}
                        value={'/activity/'.concat(this.state.Activity_Id, '/', Season['id'])}>
                          {Season['id']}
                      </option>
                    ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
};
Header.propTypes = {
  activity: PropTypes.string.isRequired,
  season: PropTypes.string.isRequired,
};
const Head = document.getElementById('header');
if (Head)
{
  ReactDOM.render(
    <Header activity={document.getElementById('activity').innerHTML} season={document.getElementById('season').innerHTML}/>, Head
  );
}
