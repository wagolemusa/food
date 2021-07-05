from django.urls import path

from .views import (
	products,
	OrderSummaryView,
	CheckoutView,
	# HomeView,
	home,
	about,
	services,
	contact,
	Newproduct,
	post_create,
	add_to_cart,
	remove_from_cart,
	remove_single_item_from_cart,
	PaymentViews,
	Mpesa,
	AddCouponView,
	RequestRefundView,
	list_category,
	callbackurl,
	getOrder,
	
)

app_name = 'shops'
	
urlpatterns = [
	# path('', HomeView.as_view(), name='home'),
	path('', home, name='home'),
	path('about/', about, name='about'),
	path('contact', contact, name='contact'),
	path('new/', Newproduct, name='new'),
	path('services', services, name='services'),
	path('callbackurl', callbackurl, name='callbackurl'),
	path('create/', post_create, name='create'),
	path('category/<int:id>/', list_category, name='list_category'),
	path('product/<int:id>/', products, name='product'),
	path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
	path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('add-to-cart/<int:id>/', add_to_cart, name='add-to-cart'),
	path('remove-from-cart/<int:id>/', remove_from_cart, name='remove-from-cart'),
	path('remove-item-from-cart/<int:id>/', remove_single_item_from_cart,
						 name='remove-single-item-from-cart'),
	path('payment/<payment_option>/', PaymentViews.as_view(), name='payment'),
	path('mpesapay/<payment_option>/', Mpesa.as_view(), name='mpesapay'),
	path('add-coupan/', AddCouponView.as_view(), name='add-coupan'),
	path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
	path('orders/', getOrder, name='orders'),
]
