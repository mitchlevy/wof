from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render, redirect


from fantasyworld.models import *
from fantasyworld.forms import BuyStockForm, SellStockForm


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


def buy_stock(request, league_id, stock_id):

	stock = Stock.objects.get(pk=stock_id)
	profile = Profile.objects.get(user=request.user)
	league = League.objects.get(id=league_id)
	league_session = LeagueSession.objects.get(
		league=league,
		is_current_league_session=True)
	team = Team.objects.filter(
		user=profile, 
		league_session=league_session)[0]

	'''check that stock belongs to the right league'''
	try:
		stock_set = stock.stock_set
		if league_session not in stock_set.league_session.all():
			return HttpResponseRedirect(reverse('fantasyworld:league_home',
				args=(league_id,)))

	except Exception as e:
		return HttpResponse(e)


	if request.method == 'POST':
		form = BuyStockForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			buy_or_sell_stock(
				stock=stock, 
				team=team, 
				quantity=quantity,
				bought_stock=True, 
				sold_stock=False)

			return redirect('/team/portfolio/' + str(team.id))
	else:
		form = BuyStockForm()

	return render(request, 'fantasyworld/buy_stock.html',
		context = {'stock': stock,
					'form': form})


def sell_stock(request, league_id, stock_id):

	stock = Stock.objects.get(pk=stock_id)
	profile = Profile.objects.get(user=request.user)
	league = League.objects.get(id=league_id)
	league_session = LeagueSession.objects.get(
		league=league,
		is_current_league_session=True)
	team = Team.objects.filter(
		user=profile, 
		league_session=league_session)[0]

	'''check that stock belongs to the right league'''
	try:
		stock_set = stock.stock_set
		if league_session not in stock_set.league_session.all():
			return HttpResponseRedirect(reverse('fantasyworld:league_home',
				args=(league_id,)))
	except Exception:
		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(league_id,)))


	if request.method == 'POST':
		form = SellStockForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			buy_or_sell_stock(
				stock=stock, 
				team=team, 
				quantity=quantity,
				bought_stock=False, 
				sold_stock=True)
			return redirect('/team/portfolio/' + str(team.id))
	else:
		form = SellStockForm()

	return render(request, 'fantasyworld/sell_stock.html',
		context = {'stock': stock,
					'current_stock_quantity': team.get_current_stock_quantity(stock),
					'form': form})



def stock_detail(request, stock_id):
	stock = Stock.objects.get(pk=stock_id)

	return render(request, 'fantasyworld/stock_detail.html',
		context = {'stock': stock})
