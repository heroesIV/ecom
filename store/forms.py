from django import forms
from .models import *

class shippingForm(forms.ModelForm):
	class Meta:

		model 	= ShippingAddress
		fields 	= '__all__'
