from django.forms import ModelForm, Textarea, CheckboxInput

from .models import *

class ProductForm(ModelForm):
	class Meta:

		model 	= Product
		fields 	= ('name','description','price','availability','image')
		widgets = {
            'description': Textarea(attrs={'cols': 21, 'rows': 5}),
            'availability': CheckboxInput(attrs={'style':'width:20px;height:20px;'}),
        }

class CustomerForm(ModelForm):
	class Meta:

		model 	= Customer
		fields 	= '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
	class Meta:

		model 	= Order
		fields	= ('status', 'paid')