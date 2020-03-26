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