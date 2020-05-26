import datetime

from django import forms
import fantasyworld.models as m

class BuyStockForm(forms.Form):
	quantity = forms.FloatField(label="Quantity")

	def clean_purchase(self):
		data = self.cleaned


class SellStockForm(forms.Form):
	quantity = forms.FloatField(label="Quantity")

	def clean_purchase(self):
		data = self.cleaned

class CommissionerToolsForm(forms.Form):
	league_name = forms.CharField(label="League Name", 
		max_length=100, 
		required=False)

class TeamSettingsForm(forms.Form):
	team_name = forms.CharField(label="Team Name",
		max_length=100, 
		required=False)
	
class CreateLeagueForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(CreateLeagueForm, self).__init__(*args, **kwargs)
		self.fields['stock sets'] = forms.ModelMultipleChoiceField(
			queryset=m.StockSet.objects.filter(
			league_type__id=self.initial['leaguetype_id']))

	league_name=forms.CharField(label="League Name",
		max_length=100)
	league_is_public=forms.BooleanField(label="League is Public? ",
		required=False)
	league_password=forms.CharField(label="League Password",
		max_length=100,
		help_text="Leave this field blank if you're creating a public league")



class LeagueJoinPrivateForm(forms.Form):
	league_password=forms.CharField(label="Enter League Password",
		max_length=100)