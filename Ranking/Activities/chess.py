""" Gets all the information on the lichess4545 league """
import re
import ssl
import sys
import json
from bs4 import BeautifulSoup
from urllib import request, parse, error
from Utilities import Season, Tournament, Team, get_all_seasons

# Globals
LICHESS4545_URL = 'https://www.lichess4545.com'

# SSL Certificates
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# Functions
def fancy_fractions(str):
    """ Convert a fancy looking fraction to a float (only works for halfs)

    args:
        str (string): The string to Convert
    """
    if '½' in str:
        if str[:-1]:
            return float(str[:-1]) + 0.5
        else:
            return 0.5
    else:
        return float(str)

# Class for Tracking a 4545 league season
class Lichess:
    def set_season(self, season_number):
        """ Initializes the league

        args:
            season_number (int): The season number
        """
        self.season = Season('Chess', f'Season {season_number}', None, 7, 100)
        self.season_number = season_number

    def get_seasons(self):
        """ Returns a list of seasons that haven't been processed"""
        result = request.urlopen(
            f'{LICHESS4545_URL}/team4545/season/1/summary/',
            context=CTX)
        beautiful_result = BeautifulSoup(result, 'html.parser')
        seasons = [int(season.get_text().strip().split()[1])
                   for season in beautiful_result.find_all(
                   'ul', {'class': 'dropdown-menu'})[-1].find_all('li')[2:]]
        run_seasons = [int(season[0].split()[1]) for season in get_all_seasons()]
        return set(seasons).difference(set(run_seasons))

    def get_season(self):
        """ Get a season"""
        result = request.urlopen(
            f'{LICHESS4545_URL}/team4545/season/{self.season_number}/pairings',
            context=CTX)
        round_results = BeautifulSoup(result, 'html.parser')

        # Get all team names TODO: Fix round ordering
        round_results_ordered = sorted(
            [round_result.get('href', '')
             for round_result in round_results.find_all('a')
             if re.fullmatch('/team4545/season/[0-9]+/round/[0-9]+/pairings/',
                             round_result.get('href', ''))],
            key=lambda x: int(x.split('/')[5]))
        for team in round_results_ordered:
            # Get the round results
            opponents = BeautifulSoup(request.urlopen(
                f"{LICHESS4545_URL}{team}",
                context=CTX),
                'html.parser'
            )
            # Collect the round results
            tournament_name = f"Round {team.split('/')[5]}"
            if tournament_name in self.season.tournaments:
                continue
            self.season.create_tournament(tournament_name)
            team_names = [opponent.get_text().strip()
                          for opponent in opponents.find_all('a', {'class': 'team-link'}
                          )]
            results = [fancy_fractions(score.get_text().strip())
                       for score in opponents.find_all('th', {'class': 'cell-score'}
                       )]
            # Insert the round results into the season
            for i in range(int(len(team_names)/2)):
                self.season.create_round(
                    team_names[2*i],
                    team_names[2*i+1],
                    results[2*i],
                    results[2*i] + results[2*i+1],
                    tournament_name
                )
            self.season.calculate_elo(tournament_name)
            self.season.glicko()
        results = [(team_name, team.elo, team.history) for team_name, team in self.season.teams.items()]
        results = sorted(results, key=lambda x: x[1])[::-1]
        # json.dump(results, open('results.txt', 'w'), indent=4)

def main():
    # Get the season numbers
    chess = Lichess()
    seasons = chess.get_seasons()
    for season in [1]: #seasons:
        chess.set_season(season)
        chess.get_season()

if __name__ == '__main__':
    main()
