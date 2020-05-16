import os
import fantasyworld.models as m
import pandas

from django.core.exceptions import ObjectDoesNotExist


'''Settings that will need to be adjusted to work on the cloud'''
nfl_lines_folder = '/Users/mitchelllevy/Desktop/_Misc/Google Drive/Projects/FantasyLife/data/NFL_Lines'
nfl_lines_csv = 'NFL_Lines.Current.csv'
nfl_lines_league_id = 13


def populate_nfl_lines():
	f1 = open(os.path.join(nfl_lines_folder, nfl_lines_csv))
	text = f1.read()
	f1.close()

	team_lines_dict = {}
	for team_line in text.split('\n')[1:]:
		team, line = team_line.split(',')
		team_lines_dict[team] = line


	teams = team_lines_dict.keys()
	league = m.League.objects.get(id=nfl_lines_league_id)
	league_session = m.LeagueSession.objects.get(
		league=league, 
		is_current_league_session=True)

	stocks = m.Stock.objects.filter(league_session = league_session)

	for team in teams:
		try:
			team_stock = stocks.get(name = team)
			team_stock.price = team_lines_dict[team]
			team_stock.save()

		except ObjectDoesNotExist:
			team_stock = m.Stock(
				league_session = league_session,
				name = team,
				price = team_lines_dict[team])
			team_stock.save()

def run():
	populate_nfl_lines()

