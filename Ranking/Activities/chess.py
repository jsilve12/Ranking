""" Gets all the information on the lichess4545 league """
import re
import ssl
import sys
from bs4 import BeautifulSoup
from urllib import request, parse, error
from Utilities import Season, Tournament, Team

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
    def __init__(self):
        """ Initializes the league """
        self.season = Season()

    def get_season(self, season_number):
        """ Get a season

        args:
            season_number (int): The season number
        """
        result = request.urlopen(
            f'{LICHESS4545_URL}/team4545/season/{season_number}/pairings',
            context=CTX)
        round_results = BeautifulSoup(result, 'html.parser')

        # Get all team names
        for team in round_results.find_all('a'):
            # Get the round results
            if re.fullmatch('/team4545/season/[0-9]+/round/[0-9]+/pairings/', team.get('href', '')):
                opponents = BeautifulSoup(request.urlopen(
                    f"{LICHESS4545_URL}{team.get('href')}",
                    context=CTX),
                    'html.parser'
                )
                print(team.get('href').split('/')[5])
                print([opponent.get_text().strip() for opponent in opponents.find_all(
                    'a', {'class': 'team-link'}
                )])
                print([fancy_fractions(score.get_text().strip()) for score in opponents.find_all(
                    'th', {'class': 'cell-score'}
                )])

def main():
    chess = Lichess()
    chess.get_season(21)

if __name__ == '__main__':
    main()
