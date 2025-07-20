from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'First name', 'Last name', 'Email', 'Address', 'Postal code', 'City', 'Paid', 'Created', 'Updated'])
        for order in queryset:
            writer.writerow([order.id, order.first_name, order.last_name, order.email, order.address, order.postal_code, order.city, order.paid, order.created, order.updated])
        return response
    export_to_csv.short_description = 'Export to CSV'
