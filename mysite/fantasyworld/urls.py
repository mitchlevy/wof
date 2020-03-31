from django.urls import path, include
from django.contrib.auth import views as auth_views
from fantasyworld import views


app_name = 'fantasyworld'
urlpatterns = [
	path('', views.index, name='index'),

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

	path('league/buy/<int:stock_id>/', views.buy_stock,
		name='buy_stock'),
	path('league/sell/<int:stock_id>/', views.sell_stock,
		name='sell_stock'),

	path('profile/', views.profile_home,
		name='profile'),
	path('team/<int:team_id>/', views.team_home,
		name='team_home'),

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

