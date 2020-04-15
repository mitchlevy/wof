import datetime

from django import forms

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
	