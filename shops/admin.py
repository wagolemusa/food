from django.contrib import admin

# Register your models here.
from .models import (Item, OrderItem, Order, 
								BillingAddress,Mpesapay,Coupon,
								Refund, Category, Contact, OrderDetails)

class CategoryAdmin(admin.ModelAdmin):
	list_display = [
			'name'
	]


def make_refund_accepted(modeladmin, request, queryset):
	queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update order to refund granted'

class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 
									'ordered',
									'being_delivered',
									'received_requested',
									'refund_requested',
									'refund_granted',
									'billing_address',
									'coupon'
									]

	list_display_links = [
		'user',
		'billing_address',
		'coupon'
	]

	list_filter = [ 'ordered',
									'being_delivered',
									'received_requested',
									'refund_requested',
									'refund_granted'
								]
	search_fields = [
		'user__username',
		'ref_code'
	]

	actions = [make_refund_accepted]

class ContactAdmin(admin.ModelAdmin):
	list_display = [
		"full_name",
		"phone",
		"email",
		"timestamp",
	]

class MpesapayAdmin(admin.ModelAdmin):
	list_display = [
		"user",
		"amount",
		"phone",
		"cash",
		"timestamp",
	]

class OrderItemAdmin(admin.ModelAdmin):
	list_display = [
		 "user",
		 "item",
		 "quantity",
		 "timestamp"
	]

class DetailedOrderAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'data',
		'time',
		'content',
		'timestamp',
	]

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Mpesapay, MpesapayAdmin)
admin.site.register(OrderDetails)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)

