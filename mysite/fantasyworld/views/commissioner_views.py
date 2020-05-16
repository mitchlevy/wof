from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render, redirect


from fantasyworld.models import *
from fantasyworld.forms import *


def commissioner_tools(request, league_id):
	'''
	First, check to ensure user is logged in and commissioner,
		and redirect user if not
	'''
	user = request.user
	if user.is_authenticated:
		try:
			team = Team.objects.get(league_session=LeagueSession.objects.get(
				league = League.objects.get(pk=league_id)),
				user=Profile.objects.get(user=user))
			user_is_commissioner = team.is_commissioner
			users_team_id = team.id

		except Exception as e:
			raise Http404(e)


	else:
		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(league_id,)))

	if not user_is_commissioner:
		return HttpResponseRedirect(reverse('fantasyworld:league_home',
			args=(league_id,)))
	'''
	'''

	if request.method == 'POST':
		form = CommissionerToolsForm(request.POST)
		if form.is_valid():
			league_name = form.cleaned_data['league_name']

			if len(league_name) > 0:
				league = League.objects.get(pk=league_id)
				league.name = league_name
				league.save()

			return HttpResponseRedirect(reverse('fantasyworld:league_home',
				args=(league_id,)))
	else:
		form = CommissionerToolsForm()	


	return render(request, 'fantasyworld/commissioner_tools.html',
		context = {'form': form,
					'league_id': league_id,
					'users_team_id': users_team_id})