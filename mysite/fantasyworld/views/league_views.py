from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.template import RequestContext

from fantasyworld.models import *
from fantasyworld.forms import BuyStockForm, SellStockForm


def handler404(request):
	return redirect('/index/')


def index(request):
	leaguetype_list = LeagueType.objects.order_by('id')
	context = {
		'leaguetype_list': leaguetype_list
		}
	
	return render(request, 'fantasyworld/index.html', context)


def leaguetype_home(request, leaguetype_id):
	try:
		leaguetype = LeagueType.objects.get(pk=leaguetype_id)
		leagues = League.objects.filter(league_type=leaguetype)

	except LeagueType.DoesNotExist:
		raise Http404("League Type Does Not Exist")
	return render(request, 'fantasyworld/leaguetype_home.html',
		{'leaguetype': leaguetype, 
		'leagues': leagues,})


def leaguetype_create(request):
	try:
		name = request.POST['leaguetype_name']
		description = request.POST['leaguetype_description']
		new_leaguetype = LeagueType(name=name, description=description)
		new_leaguetype.save()

		return HttpResponseRedirect(reverse('fantasyworld:leaguetype_home', 
			args=(new_leaguetype.id,)))
	except MultiValueDictKeyError:
		return render(request, 'fantasyworld/leaguetype_create.html')


'''
Views corresponding to particular leagues
'''
def league_home(request, league_id):
	try:
		league = League.objects.get(pk=league_id)
	except League.DoesNotExist:
		raise Http404("League Does Not Exist :(")

	try:
		user = request.user		
		if len(Profile.objects.filter(user=user)) == 0:
			prof = Profile(user=user)
			prof.save()

		league_session = LeagueSession.objects.get(league=league,
			is_current_league_session=True)
		teams = Team.objects.filter(league_session=league_session)

		if user.is_authenticated:
			user_in_league = Team.objects.filter(league_session = league_session,
				user=Profile.objects.get(user=user)).exists()

		all_stocks = Stock.objects.filter(league_session=league_session)

		team_portfolio_values = {}
		for team in teams:
			portfolio_value = 0
			for stock in all_stocks:
				quantity = team.get_current_stock_quantity(stock)
				price = stock.price
				portfolio_value += quantity*price
			team_portfolio_values[team] = portfolio_value
			
	except Exception as e:
		raise Http404(e)
		
	return render(request, 'fantasyworld/league_home.html',
		context={'league': league, 
					'user_in_league': user_in_league,
					'team_portfolio_values': team_portfolio_values,
					'all_stocks': all_stocks})


def league_create(request, leaguetype_id):
	try:
		name = request.POST['league_name']

		new_league = League(name=name, 
			league_type=LeagueType.objects.get(pk=leaguetype_id))
		new_league.save()

		new_league_session = LeagueSession(league=new_league)
		new_league_session.save()

		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(new_league.id,)))
	except MultiValueDictKeyError:
		return render(request, 
			'fantasyworld/league_create.html',
			context={'leaguetype_id': leaguetype_id})


def league_join(request, league_id):
	
	'''first, get the league session.
	but if it doesn't exist create one'''
	
	user = request.user
	if user.is_authenticated:
		try:
			league_sessions = LeagueSession.objects.filter(league=league_id)
			current_league_session = [ls for ls in league_sessions 
										if ls.is_current_league_session][0]
		except IndexError:
			new_league_session = LeagueSession(league=League.objects.get(pk=league_id))
			new_league_session.save()
			current_league_session = new_league_session

		profile = Profile.objects.filter(user=user)[0]

		'''only one team per user per league'''
		if Team.objects.filter(user=profile, league_session = current_league_session).count() <1:
			team = Team.objects.create(user= profile,
										league_session = current_league_session)
			team.set_team_name()
			team.save()

		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(league_id,)))

	else:
		return redirect('/login')


class LeagueView(generic.ListView):
	model = League
	template_name = 'fantasyworld/league_detail.html'



def team_home(request, team_id):
	user = request.user
	try:
		team = Team.objects.get(pk=team_id)
	except Team.DoesNotExist:
		raise Http404("Team Does Not Exist :(")

	league_session = team.league_session
	noncash_portfolio_value = 0

	'''get list of all stocks available for purchase/sale'''
	all_stocks = Stock.objects.filter(league_session=league_session)
	teams_stocks = {}
	for stock in all_stocks:
		teams_stocks[stock] = team.get_current_stock_quantity(stock)
		noncash_portfolio_value += teams_stocks[stock] * stock.price

	return render(request, 'fantasyworld/team_home.html',
		context={'team': team,
				'teams_stocks': teams_stocks,
				'noncash_portfolio_value': noncash_portfolio_value})


