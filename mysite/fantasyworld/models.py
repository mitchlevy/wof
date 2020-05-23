from django.db import models
from django.contrib.auth.models import User

class GameType(models.Model):
	'''
	This corresponds to different type of games, e.g.,
		periodic head to head matchup
		stock market style game
		etc. etc.
	Not sure what type of info I'll put here vs. in
		LeagueType, but it may prove helpful
	'''
	name = models.CharField(max_length=100)


# Create your models here.
class LeagueType(models.Model):
	'''
	The type of league
	Roughly, this should match to the playerset involved, so for
	example 'Bachelor' would be a type of league.
	Plausibly, though, there may be many iterations of a Bachelor
	league if different people are keeping different scoring sets/rules,
	so 'Bachelor1/2/3 etc.' might be the league type
	'''
	name = models.CharField(max_length=100)
	description = models.CharField(max_length = 500)
	game_type = models.ManyToManyField(GameType)
	stock_types = models.CharField(max_length=1000, null=True)
	how_to_play = models.CharField(max_length=3000, null=True)

	meta_leaguetype = models.ForeignKey('self', blank=True, null=True,
		on_delete = models.SET_NULL, default=None)

	def __str__(self):
		return self.name

class League(models.Model):
	'''
	This is a league

	It has a type. This is the "permanent" version for histories and 
	whatnot, but it has a bunch of offshooting leaguesessions, which 
	correspond to each year/term of a league.  Because those teams can 
	change, year to year, the league itself doesn't have teams

	There are likely other settings for a league (but maybe not?
	possibly all settings belong to either a LeagueType or a LeagueSession)
	'''
	league_type = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
	name = models.CharField(max_length = 100)
	is_public = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Profile(models.Model):
	'''
	This is the extended user model,
	where I store all relevant user information outside
	of the username/password used to create the user class
	'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)


class LeagueSession(models.Model):
	'''
	This corresponds to a league year
	So the league is the masterclass that contains information about the league
		over the years, but each new year (or other time period) gets a new 
		league session
	'''
	league = models.ForeignKey(League, on_delete = models.CASCADE)
	members = models.ManyToManyField(Profile, through='Team', default=None)
	session = models.IntegerField(default=2020)
	is_current_league_session = models.BooleanField(default=True)


class LeagueIncrement(models.Model):
	'''
	This corresponds to the atomic unit of a league
	For a weekly league, this would correspond to a week
	For a daily league, a day
	'''
	league_session = models.ForeignKey(LeagueSession, on_delete=models.CASCADE)
	increment_description = models.CharField(max_length=100)


class Player(models.Model):
	'''
	This is the player model.
	In, for example, a fantasy football league this would correspond
	to football players.
	There's a lot to figure out though.  It might have to be subcategorized,
	along any number of dimensions.  For example, in football, there are
	several positions.  In, say, fantasy bachelor in paradise, people might
	be required to have a certain number of men and women.

	Lots to figure out.
	'''
	league_type = models.ForeignKey(LeagueType, on_delete=models.CASCADE)
	name = models.CharField(max_length = 100)	



class Team(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	league_session = models.ForeignKey(LeagueSession, on_delete=models.CASCADE)
	team_name = models.CharField(max_length=100, default = "Team")

	is_commissioner = models.BooleanField(default=False)
	budget = models.FloatField(default=100)

	def set_team_name(self):
		team_name = self.user.user.username + " Team"
		self.team_name = team_name

	def get_current_stock_quantity(self, stock):
		quantity = 0
		transactions = stock.stocktransaction_set.filter(team=self)
		for transaction in transactions:
			if transaction.bought_stock == True:
				quantity += transaction.quantity
			if transaction.sold_stock == True:
				quantity -= transaction.quantity

		return quantity

	def get_current_cash(self):
		return self.budget

	def get_current_portfolio_value(self):
		portfolio_value = 0
		stock_transaction_set = self.stocktransaction_set.all()
		for stock_transaction in stock_transaction_set:
			stock = stock_transaction.stock
			if stock_transaction.bought_stock:
				quantity = stock_transaction.quantity
			else:
				quantity = (-1)*stock_transaction.quantity

			stock_price = stock.price
			portfolio_value += quantity*stock_price

		return portfolio_value


class StockSet(models.Model):
	'''
	This is a set of stocks, which can be paired with league sessions
	e.g., NFL Season Win Totals
	Might need to eventually build sub/supersetting to get the right level
	of specificity
	'''
	name = models.CharField(max_length=200, default="Default Stock Set")
	description=models.CharField(max_length=1000, null=True)

	league_session = models.ManyToManyField(LeagueSession, default=None)
	superset_stockset = models.ForeignKey('self', blank=True, null=True,
		on_delete = models.SET_NULL, default=None)



class Stock(models.Model):
	'''
	This is a stock model
	It has a few properties, such as
		- a price
	It does a few things, such as
		- pay a dividend
		-
	'''
	stock_set = models.ForeignKey(StockSet, on_delete = models.CASCADE)
	name = models.CharField(max_length=100,  default="Untitled")
	price = models.FloatField()
	transactions = models.ManyToManyField(Team, through = 'StockTransaction',
		default=None)
	description = models.CharField(max_length=1000, null=True)

	stock_type = models.CharField(max_length=100, default='Generic')

	def get_stock_type_choices(self):
		inherited_stock_types = self.league_session.league.league_type.stock_types.split(',')
		stock_types_choices = inherited_stock_types if (inherited_stock_types != ['']) else ['Generic']
		inherited_stock_types = [x.strip() for x in inherited_stock_types]

		return position_choices



class StockTransaction(models.Model):
	'''
	This is a model for 
	'''
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
	price = models.FloatField()
	quantity = models.FloatField()
	bought_stock = models.BooleanField()
	sold_stock = models.BooleanField()
	time = models.DateTimeField(auto_now_add=True)




