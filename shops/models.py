from django import forms
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.

# def upload_location(instance, filename):
# 	return "%s/%s" %(instance.id, filename)

class Category(models.Model):
	name = models.CharField(max_length=250)
	
	def __str__(self):
		return self.name

	def get_category_absolete_url(self):
		return reverse('shops:list_category', args=[self.id])



CATEGORY_CHOICES = (
	('S',  'Shirts'),
	('SW', 'Sport weare'),
	('OW', 'Outwear')
)

LABEL_CHOICES = (
	('P', 'On its Way'),
	('S', 'Delivered'),
	('D', 'Canceled')
)

ADDRESS_CHOICES = (
	('B', 'Billing'),
	('S', 'Shipping')
)

class Item(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE,
                    related_name="category_set")
	title = models.CharField(max_length=100)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	image = models.ImageField()
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	def __str__(self):
		return self.title

	def get_absolete_url(self):
		return reverse("shops:product", kwargs={
				'id': self.id
			})

	def get_add_to_cart_url(self):
		return reverse("shops:add-to-cart", kwargs={
			'id': self.id
			})

	def get_remove_from_cart_url(self):
		return reverse("shops:remove-from-cart", kwargs={
			'id':self.id
			})

class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
													on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)
	quantity = models.IntegerField(default=1)
	status = models.CharField(default='pending', max_length=15)
	ordered = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	def __str__(self):
		return "%s %s" %(self.quantity, self.item.title)
	
	# Total quantity price
	def get_total_item_price(self):
		return self.quantity * self.item.price

	# Discount on Items
	def get_discount_item_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_discount_item_price()

	# Function return the final total price
	def get_final_price(self):
		if self.item.discount_price:
			return self.get_discount_item_price()
		return self.get_total_item_price()

class OrderDetails(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
													on_delete=models.CASCADE)
	dates = models.CharField(blank=True, max_length=100)
	time = models.CharField(blank=True, max_length=100)
	items = models.ManyToManyField(OrderItem, blank=True)
	content = models.CharField(blank=True, max_length=500)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.user.username

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
													on_delete=models.CASCADE)
	ref_code = models.CharField(max_length=20)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField(auto_now=False, auto_now_add=True)
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey(
		'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
	mpesa_pay = models.ForeignKey(
		'Mpesapay', on_delete=models.SET_NULL, blank=True, null=True)
	coupon = models.ForeignKey(
		'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
	order_details = models.ForeignKey(
		'OrderDetails', on_delete=models.SET_NULL, blank=True, null=True)
	being_delivered = models.BooleanField(default=False)
	received_requested = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)
	# timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	'''
	1. Item added to cart
	2. Adding a billing address
	(Failed checkout)
	3. payment
		(Preprocessing, processing, packing, etc)
	4. Being delivered
	5. Received
	6. Refunds
	'''

	def __str__(self):
		return self.user.username

	# Function get the final tatol 
	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		if self.coupon:
			total -= self.coupon.amount
		return total

class BillingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
														on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100)
	apartment_address = models.CharField(max_length=100)
	phone = models.BigIntegerField(blank=True, null=True)
	address = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.user.username

		
class Mpesapay(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
													on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.FloatField()
	phone = models.BigIntegerField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	cash = models.CharField(default='notpayed', max_length=15)

	def __str__(self):
		return self.user.username


class Coupon(models.Model):
	code = models.CharField(max_length=15)
	amount = models.FloatField()

	def __str__(self):
		return self.code 

class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField()
	accepted = models.BooleanField(default=False)
	email = models.EmailField(max_length=100)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	def __str__(self):
		return "%s" %(self.pk)

# Image 
class Images(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE,)
	image = models.ImageField(
		null=True,
		blank=True)

	def __str__(self):
		return self.post.title + "Image"

class Contact(models.Model):
	full_name = models.CharField(max_length=120)
	phone  = models.IntegerField()
	email = models.CharField(max_length=150)
	subject = models.CharField(max_length=200)
	message = models.TextField(max_length=500)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.full_name

	def __str__(self):
		return self.full_name


		