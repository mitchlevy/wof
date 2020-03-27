from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic


from .models import *
from .forms import BuyStockForm, SellStockForm

def get_or_create_profile(user):
	try:
		profile = Profile.objects.filter(user=user)[0]
	except IndexError:
		profile = Profile(user=user)
		profile.save()	
	return profile


def buy_or_sell_stock(stock, team, quantity, 
						bought_stock, sold_stock):
	'''create and save the transaction'''
	price = stock.price
	if sold_stock:
		max_sale_quantity = team.get_current_stock_quantity(stock)
		if quantity > max_sale_quantity:
			quantity = max_sale_quantity
	if bought_stock:
		max_purchase_quantity = team.budget / price
		if quantity > max_purchase_quantity:
			quantity = max_purchase_quantity

	transaction = StockTransaction(team=team, stock=stock,
									price=price, quantity=quantity,
									bought_stock=bought_stock, 
									sold_stock=sold_stock)
	transaction.save()

	'''update the team's budget'''
	if bought_stock:
		team.budget -= price*quantity
	elif sold_stock:
		team.budget += price*quantity
	team.save()


def index(request):
	leaguetype_list = LeagueType.objects.order_by('id')
	context = {
		'leaguetype_list': leaguetype_list
		}
	
	return render(request, 'fantasyworld/index.html', context)

'''
Views corresponding to particular types of leagues
'''
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

		profile = get_or_create_profile(user)

		'''only one team per user per league'''
		if Team.objects.filter(user=profile, league_session = current_league_session).count() <1:
			team = Team.objects.create(user= profile,
										league_session = current_league_session)
			team.set_team_name()
			team.save()

		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(league_id,)))

	else:
		return redirect('/fantasyworld/login')


class LeagueView(generic.ListView):
	model = League
	template_name = 'fantasyworld/league_detail.html'


def profile_home(request):
	user = request.user
	if user.is_authenticated:
		profile = get_or_create_profile(user)
		teams = Team.objects.filter(user=profile)

		team_league_dict = {}
		for team in teams:
			league = team.league_session.league
			team_league_dict[team] = league

		return render(request, 'fantasyworld/profile.html',
			context = {'team_league_dict': team_league_dict})
	else:
		return redirect('/fantasyworld/login')


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


def buy_stock(request, stock_id):

	stock = Stock.objects.get(pk=stock_id)
	profile = Profile.objects.get(user=request.user)
	team = Team.objects.filter(user=profile, league_session=stock.league_session)[0]

	if request.method == 'POST':
		form = BuyStockForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			buy_or_sell_stock(stock=stock, team=team, quantity=quantity,
				bought_stock=True, sold_stock=False)

			return redirect('/fantasyworld/team/' + str(team.id))
	else:
		form = BuyStockForm()

	return render(request, 'fantasyworld/buy_stock.html',
		context = {'stock': stock,
					'form': form})


def sell_stock(request, stock_id):

	stock = Stock.objects.get(pk=stock_id)
	profile = Profile.objects.get(user=request.user)
	team = Team.objects.filter(user=profile, league_session=stock.league_session)[0]

	if request.method == 'POST':
		form = SellStockForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			buy_or_sell_stock(stock=stock, team=team, quantity=quantity,
				bought_stock=False, sold_stock=True)
			return redirect('/fantasyworld/team/' + str(team.id))
	else:
		form = SellStockForm()

	return render(request, 'fantasyworld/sell_stock.html',
		context = {'stock': stock,
					'current_stock_quantity': team.get_current_stock_quantity(stock),
					'form': form})

'''
Users Views
'''


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('/fantasyworld')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = Profile(user=user)
            profile.save()
            return redirect('/fantasyworld')
        else:
            return render(request, 'fantasyworld/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'fantasyworld/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/fantasyworld')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/fantasyworld')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'fantasyworld/signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'fantasyworld/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/fantasyworld')
