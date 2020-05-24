from django.urls import path, include
from django.contrib.auth import views as auth_views
from fantasyworld import views


app_name = 'fantasyworld'
urlpatterns = [
	path('', views.index, name='index'),
	path('how-to-play', views.how_to_play,
		name='how_to_play'),
	path('league-categories', views.league_categories, 
		name='league_categories'),

	path('leaguetype/<int:leaguetype_id>/', views.leaguetype_home, 
		name='leaguetype_home'),
	path('leaguetype/create/', views.leaguetype_create,
		name='leaguetype_create'),

	path('leaguetype/<int:leaguetype_id>/league_create/', 
			views.league_create,
			name='league_create'),
	path('<int:pk>/league/', views.LeagueView.as_view(), 
		name='leagues'),
	path('league/<int:league_id>/', views.league_home,
		name='league_home'),
	path('league/<int:league_id>/join/', views.league_join,
		name='league_join'),
	path('league/<int:league_id>/join_private/', views.league_join_private,
		name='league_join_private'),	

	path('league/<int:league_id>/commissioner-tools/', views.commissioner_tools,
		name='commissioner_tools'),

	path('league/buy/<int:league_id>/<int:stock_id>/', views.buy_stock,
		name='buy_stock'),
	path('league/sell/<int:league_id>/<int:stock_id>/', views.sell_stock,
		name='sell_stock'),

	path('league/stock_detail/<int:stock_id>', views.stock_detail,
		name='stock_detail'),

	path('profile/', views.profile_home,
		name='profile'),
	path('team/<int:team_id>/', views.team_home,
		name='team_home'),
	path('team/portfolio/<int:team_id>/', views.team_portfolio,
		name='team_portfolio'),
	path('team/standings/<int:team_id>/', views.team_standings,
		name='team_standings'),
	path('league/team-settings/<int:team_id>/', views.team_settings,
		name='team_settings'),


	path('signup/', views.signup,
		name='signup'),
	path('login', auth_views.LoginView.as_view(), 
		name='login'),
	path('logout', auth_views.LogoutView.as_view(),
		name='logout'),


    path('social-auth/', include('social_django.urls', namespace='social')),
    # Note: the problem with this is that the app_name is set to fantasyworld, thus
    # the namespaces is effectively fantasyworld:social, but the package relies on
    # the namespace being just 'social'
    # could solve by either (1) move all views to the fantasyworld namespace, or
    # (2) creating a new app
    # but this is a whole mess because it means migrating my whole user view/model/flow
    # or (3) editing the package itself
]

