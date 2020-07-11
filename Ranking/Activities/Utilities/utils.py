"""
Abstract library for processing elo results (v2)

"""

# TODO:
# Get date related functionality working
# Get DB working

import math
import psycopg2
from datetime import date
from configparser import ConfigParser

def parseDB(filename='db.config', section='postgresql'):
    """ Create a connection to a database

    Args:
        filename (string): The file containing the credentials
        section (string): The section in the file

    Returns:
        The arguments for initializing a pyscopg2 database
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found')
    return db

def get_all_seasons():
    """ Gets all the seasons """
    conn = psycopg2.connect(**parseDB('configs/local/db.config'))
    cur = conn.cursor()
    cur.execute('SELECT name FROM season')
    return cur.fetchall()

class Team:
    """ Class to store information about a team"""
    def __init__(self, elo=1500.00, glicko=350.00, glicko_time=0,
                 side_1=0.00, side_2=0.00, id=-1):
        """ Initialize the teams information

        Args:
            elo (float): The teams starting elo
            glicko (float): The teams starting glicko
            glicko_time (float): Rounds since that team has played a game
            side_1 (float): Elo change as a result of side 1
            side_2 (float): Elo change as a result of side 2
            id (int): The teams id in the database
        """
        self.elo = elo
        self.elo_round = self.elo
        self.glicko = glicko
        self.glick_round = self.glicko
        self.glick_time = glicko_time
        self.history = {}
        self.side_1 = side_1
        self.side_2 = side_2
        self.id = id

    def round(self, result, rounds, opp_elo, opp_name):
        """ Processes one rounds worth of results

        Args:
            result (double): Number of points earned by the team
            rounds (double): Maximum possible number of points
            opp_elo (double): The elo of your opponent
            opp_name (string): Opponents name
        """
        # First update the glicko based on inactivity
        if self.glick_time != 0:
            self.glicko = min(
                math.sqrt(self.glicko*self.glicko + 34.6*34.6*self.glick_time),
                350)
            self.glick_time = 0

        # Updates the elo
        q = math.log1p(10)/400
        g = 1/math.sqrt(1+(3*q*q*self.glicko*self.glicko)/(math.pi**2))
        e = 1+math.pow(10, g*(self.elo_round-opp_elo)/(-400))
        e = 1/(e)

        d2 = 1/(q*q*g*g*e*(1-e))
        a = (q/(1/(self.glicko*self.glicko)+1/(d2)))
        b = g*(result-rounds*e)
        val = a*b
        self.elo_round = self.elo_round + val
        self.history[opp_name] = {'score': result/rounds, 'elo_change': val, 'glicko': self.glicko}

        # Updates the glicko based on the round
        self.glick_round = math.sqrt(1/(
            1/(self.glick_round*self.glick_round)+1/d2))

    def increment_time_period(self):
        """ Increment the time period by one"""
        self.glick_time += 1

    def end_time_period(self):
        """ Sync the new glicko and elo with ones frozen from before the time
            period started
        """
        self.glicko = self.glick_round
        self.elo = self.elo_round

class Tournament:
    """ An object to simulate a single tournament.
        A tournament lasts one time period or fewer"""
    def __init__(self, event_date):
        """
        Args:
            event_date (date): First day the event occured
        """
        self.rounds = []
        self.date = event_date

    def create_round(self, team1, team2, res, round):
        """ A single matchup in a single round

        Args:
            team1 (Team): The first team in the round
            team2 (Team): The second team in the round
            res (double): The number of points won by team one
            round (double): The number of rounds played
        """
        self.rounds.append({
            'team_1': team1,
            'team_2': team2,
            'result': res,
            'rounds': round
        })


class Season:
    """ A season is a collection of tournaments"""
    def __init__(self, activity, name, season_start, glicko_increment, default_glicko=350.00):
        """
        Args:
            activity (string): The activity the season is a part of
            name (string): Name of the season
            season_start (date): The start date of the season
            glicko_increment (int): The number of days after which to increment glicko_time
            default_glicko (float): Default glicko to use
        """
        self.teams = {}
        self.tournaments = {}
        self.conn = psycopg2.connect(**parseDB('configs/local/db.config'))
        self.activity = activity
        self.name = name
        self.cur = self.conn.cursor()
        self.season_starts = season_start
        self.glicko_increment = glicko_increment
        self.default_glicko = default_glicko

        # Get the activity id
        self.cur.execute(f'''SELECT id FROM activity WHERE name = %s''', (self.activity, ))
        id = self.cur.fetchone()
        if id:
            self.activity_id = id[0]
        else:
            self.cur.execute(f'''INSERT INTO activity(name) VALUES(%s)
                              RETURNING id''', (self.activity, ))
            self.activity_id = self.cur.fetchone()[0]

        # See if the season exists
        self.cur.execute(f'''SELECT id FROM season WHERE name = %s''', (self.name, ))
        id = self.cur.fetchone()
        if id:
            self.id = id[0]
        else:
            self.cur.execute(f'''INSERT INTO season(name, activity_id) VALUES(%s,%s)
                              RETURNING id''',
                             (self.name, self.activity_id))
            self.id = self.cur.fetchone()[0]
        self.conn.commit()

        # Load Teams
        # Load Tournaments
        # Load Rounds

    def calculate_elo(self, tournament_name):
        """ Calculate the elo score change for a desired tournament

        Args:
            tournament_name (string): Name of the tournament
        """
        for round in self.tournaments.get(tournament_name).rounds:
            # Create a team if one does not exist for each competitor
            for i in ['team_1', 'team_2']:
                if round[i] not in self.teams:
                    self.teams[round[i]] = Team(glicko=self.default_glicko)

            # Calculate elo changes
            self.teams[round['team_1']].round(
                round['result'], round['rounds'],
                self.teams[round['team_2']].elo, round['team_2'])
            self.teams[round['team_2']].round(
                math.fabs(round['rounds']-round['result']), round['rounds'],
                self.teams[round['team_1']].elo, round['team_1'])

        for team in self.teams.values():
            team.end_time_period()

    def glicko(self):
        """ Increment the time period for all teams"""
        for team in self.teams.values():
            team.increment_time_period()

    def create_tournament(self, tournament_name):
        """ Create a new tournament

        Args:
            tournament_name (string): Insert a new tournament
        """
        self.tournaments[tournament_name] = Tournament(None)

    def create_round(self, team1, team2, result, rounds, tournament_name):
        """ Creates a new round

        Args:
            team1 (Team): The first team in the round
            team2 (Team): The second team in the round
            result (Double): Points won by team1
            rounds (Double): Total number of rounds
            tournament_name (String): Name of the tournament
        """
        self.tournaments[tournament_name].create_round(team1, team2, result, rounds)

    def __del__(self):
        """ Persist the changes into the database"""

        # Persist Teams
        for team_name, team in self.teams.items():
            if team.id != -1:
                self.cur.execute(f'''
                    UPDATE team SET elo=%s, glicko=%s, glicko_time=%s, side_1=%s, side_2=%s
                    WHERE id=%s''',
                    (team.elo, team.glicko, team.glick_time, team.side_1, team.side_2, team.id))
            else:
                self.cur.execute(f'''
                    INSERT INTO team(name, elo, glicko, glicko_time, side_1, side_2, activity, season)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                    (team_name, team.elo, team.glicko, team.glick_time, team.side_1, team.side_2, self.activity_id, self.id))
                self.cur.execute(f'''
                    INSERT INTO season_team(season_id, team_id)
                    VALUES(%s, %s)''', (self.id, self.cur.fetchone()[0]))
        self.conn.commit()

        # Persist Tournaments and Rounds
        for tournament_name, tournament in self.tournaments.items():
            self.cur.execute(f'''
                INSERT INTO tournament(season_id, name) VALUES(%s, %s) RETURNING id''',
                (self.id, tournament_name))

            # Persist the Rounds
            # self.cur.execute(f'''
            #     INSERT INTO round(tournament_id, )''')
        self.conn.commit()

# EOF
