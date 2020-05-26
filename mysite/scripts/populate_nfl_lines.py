import os
import fantasyworld.models as m
import pandas

from django.core.exceptions import ObjectDoesNotExist


'''Settings that will need to be adjusted to work on the cloud'''

pc_nfl_lines_folder = '/Users/mitchelllevy/Desktop/_Misc/Google Drive/Projects/FantasyLife/django_v1/mysite/fantasyworld/data'
pc_nfl_lines_league_id = 13
pc_nfl_lines_leaguetype_id = 7

heroku_nfl_lines_folder = '/app/fantasyworld/data'
heroku_nfl_lines_league_id = 2
heroku_nfl_lines_leaguetype_id = 3

nfl_lines_csv = 'NFL_Lines.Current.csv'
nfl_lines_league_id = 13


def populate_nfl_lines():

	'''
	Adapt to whether script is running on heroku or locally
	'''
	cwd = os.getcwd()

	if cwd == '/app':
		nfl_lines_folder = heroku_nfl_lines_folder
		nfl_lines_league_id = heroku_nfl_lines_league_id
		nfl_lines_leaguetype_id = heroku_nfl_lines_leaguetype_id
	else:
		nfl_lines_folder = pc_nfl_lines_folder
		nfl_lines_league_id = pc_nfl_lines_league_id
		nfl_lines_leaguetype_id = pc_nfl_lines_leaguetype_id

	f1 = open(os.path.join(nfl_lines_folder, nfl_lines_csv))
	text = f1.read()
	f1.close()

	team_lines_dict = {}
	for team_line in text.split('\n')[1:]:
		team, line = team_line.split(',')
		team_lines_dict[team] = line


	teams = team_lines_dict.keys()

	league_type = m.LeagueType.objects.get(pk=nfl_lines_leaguetype_id)
	leagues = m.League.objects.filter(league_type=league_type)

	for league in leagues:
		league_session = m.LeagueSession.objects.get(
			league=league, 
			is_current_league_session=True)

		try:
			stock_set = m.StockSet.objects.get(league_session=league_session)	
		except Exception:
			stock_set = m.StockSet(name='NFL Lines', 
				description='2020 NFL Season Win Lines')
			stock_set.save()
			stock_set.league_session.add(league_session)
			stock_set.save()

		stocks = m.Stock.objects.filter(stock_set = stock_set)
		
		for team in teams:
			try:
				team_stock = stocks.get(name = team)
				team_stock.price = team_lines_dict[team]
				team_stock.save()

			except ObjectDoesNotExist:
				team_stock = m.Stock(
					stock_set = stock_set,
					name = team,
					price = team_lines_dict[team])
				team_stock.save()

def run():
	populate_nfl_lines()

