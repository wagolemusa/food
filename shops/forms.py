from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Item, Images, Contact, OrderDetails

PAYMENT_CHOICES = (
	('S', 'Stripe'),
	# ('P', 'PayPal'),
	('M', 'M-pesa')

)

class CheckoutForm(forms.Form):
	address = forms.CharField(required=False, widget=forms.TextInput(attrs={
		'class': 'form-control'
		}))

	phone = forms.CharField(required=False, widget=forms.NumberInput(attrs={
		'class': 'form-control'
		}))
	description = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control'
		}))
	# same_shipping_address = forms.BooleanField(required=False)
	# save_info = forms.BooleanField(required=False	)
	payment_option = forms.ChoiceField(
		widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Promo code',
		'aria-label': 'Recipient\'s username',
		'aria-describedby': 'basic-addon2'
		}))

class RefundForm(forms.Form):
	ref_code = forms.CharField()
	message = forms.CharField(widget=forms.Textarea(attrs={
		'rows': 4
		}))
	email = forms.EmailField()


class PostForms(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control'
		}))
	price = forms.CharField(widget=forms.NumberInput(attrs={
		'class':'form-control'
		}))
	description = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control'
		}))
	
	class Meta:
		model = Item
		fields = [
			"category",
			"title",
			"price",
			"description",
			"image",
	

		]
class ImageForms(forms.ModelForm):
	image = forms.ImageField(label='Image')

	class Meta:
		model = Images
		fields = ('image',)


class CantactForms(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control'
		}))
	phone = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control'
	}))

	email = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control'
		}))
	subject = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control'
		}))
	message = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control'
		}))

	class Meta:
		model = Contact
		fields = [
			"full_name",
			"phone",
			"email",
			"subject",
			"message",
		]

class OrderDetailsForm(forms.ModelForm):
	dates = forms.CharField(widget=forms.DateInput(attrs={
		'class': 'form-control'
		}))
	
	time = forms.CharField(widget=forms.TimeInput(attrs={
		'class': 'form-control'
		}))
	content = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control'
		}))

	class Meta:
		model = OrderDetails
		fields = [
			"dates",
			"time",
			"content"
		]