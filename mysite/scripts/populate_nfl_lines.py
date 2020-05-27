import os
import fantasyworld.models as m
import pandas

from django.core.exceptions import ObjectDoesNotExist


'''Settings that will need to be adjusted to work on the cloud'''

pc_nfl_lines_folder = '/Users/mitchelllevy/Desktop/_Misc/Google Drive/Projects/FantasyLife/django_v1/mysite/fantasyworld/data'
pc_nfl_lines_league_id = 13
pc_nfl_lines_leaguetype_id = 7
pc_nfl_lines_stockset_id = 7

heroku_nfl_lines_folder = '/app/fantasyworld/data'
heroku_nfl_lines_league_id = 2
heroku_nfl_lines_leaguetype_id = 3
heroku_nfl_lines_stockset_id = 1

nfl_lines_csv = 'NFL_Lines.Current.csv'
nfl_lines_league_id = 13


def populate_nfl_lines():

	'''
	Adapt to whether script is running on heroku or locally
	'''
	cwd = os.getcwd()
	if cwd == '/app':
		nfl_lines_folder = heroku_nfl_lines_folder
		nfl_lines_stockset_id = heroku_nfl_lines_stockset_id

	else:
		nfl_lines_folder = pc_nfl_lines_folder
		nfl_lines_stockset_id = pc_nfl_lines_stockset_id

	stock_set = m.StockSet.objects.get(pk=nfl_lines_stockset_id)
	stocks = m.Stock.objects.filter(stock_set = stock_set)

	'''read in NFL Lines data'''
	f1 = open(os.path.join(nfl_lines_folder, nfl_lines_csv))
	text = f1.read()
	f1.close()
	
	nfl_team_lines_dict = {}
	for nfl_team_line in text.split('\n')[1:]:
		nfl_team, line = nfl_team_line.split(',')
		nfl_team_lines_dict[nfl_team] = line

	nfl_teams = nfl_team_lines_dict.keys()
	

	'''update stocks to correspond to new data'''
	for nfl_team in nfl_teams:
		try:
			nfl_team_stock = stocks.get(name = nfl_team)
			nfl_team_stock.price = nfl_team_lines_dict[nfl_team]
			nfl_team_stock.save()

		except ObjectDoesNotExist:
			nfl_team_stock = m.Stock(
				stock_set = stock_set,
				name = nfl_team,
				price = nfl_team_lines_dict[nfl_team])
			nfl_team_stock.save()

def run():
	populate_nfl_lines()

