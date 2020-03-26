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


class Stock(models.Model):
	'''
	This is a stock model
	It has a few properties, such as
		- a price
	It does a few things, such as
		- pay a dividend
		-
	'''
	league_session = models.ForeignKey(LeagueSession, on_delete = models.CASCADE)
	name = models.CharField(max_length=100,  default="Untitled")
	price = models.FloatField()
	transactions = models.ManyToManyField(Team, through = 'StockTransaction',
		default=None)


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




