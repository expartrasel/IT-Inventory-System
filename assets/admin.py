import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from .models import Category, SubCategory, Product, Outlet, OutletStock, Transfer, TransferHistory

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    writer = csv.writer(response)
    
    fields = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(fields)
    
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    
    return response

export_as_csv.short_description = "Export Selected as CSV (Excel)"

class StockStatusFilter(admin.SimpleListFilter):
    title = 'Filter by Stock'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('stock_out', 'Stock Out'),
            ('low_stock', 'Low Stock'),
            ('over_stock', 'Over Stock'),
            ('available', 'Available'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'stock_out':
            return queryset.filter(quantity=0)
        if self.value() == 'low_stock':
            return queryset.filter(quantity__gt=0, quantity__lte=5)
        if self.value() == 'over_stock':
            return queryset.filter(quantity__gt=200)
        if self.value() == 'available':
            return queryset.filter(quantity__gt=5, quantity__lte=200)
        return queryset

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'content_type', 'user', 'action_time')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Outlet)

@admin.register(OutletStock)
class OutletStockAdmin(admin.ModelAdmin):
    list_display = ('outlet', 'product', 'quantity', 'display_outlet_status')
    list_filter = ('outlet', 'product')
    search_fields = ('product__name', 'outlet__name')

    def display_outlet_status(self, obj):
        if obj.quantity == 0:
            color = 'red'
            label = 'Out of Stock'
        elif obj.quantity <= 5:
            color = 'orange'
            label = 'Low Stock'
        else:
            color = 'green'
            label = 'Available'
        
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            label
        )

    display_outlet_status.short_description = 'Outlet Status'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'quantity', 'display_stock_status', 'added_date')
    list_filter = (StockStatusFilter, 'category', 'added_date') 
    date_hierarchy = 'added_date'
    actions = [export_as_csv] 
    search_fields = ('name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'subcategory'),
            'description': 'Enter the primary details of the product here.'
        }),
        ('Stock Details', {
            'fields': ('quantity',),
            'description': 'Enter the current available stock in the warehouse.'
        }),
    )

    def display_stock_status(self, obj):
        status = obj.stock_status
        if status == "Stock Out":
            color = "red"
        elif status == "Low Stock":
            color = "orange"
        elif status == "Over Stock":
            color = "#007bff"
        else:
            color = "green"
            
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            status,
        )
    
    display_stock_status.short_description = 'Stock Status'

admin.site.register(Product, ProductAdmin)

class TransferAdmin(admin.ModelAdmin):
    list_display = ('product', 'from_outlet', 'to_outlet', 'quantity_transferred', 'transfer_date')
    list_filter = ('from_outlet', 'to_outlet', 'transfer_date')
    date_hierarchy = 'transfer_date'
    actions = [export_as_csv] 

    fieldsets = (
        ('Route Information', {
            'fields': ('product', 'from_outlet', 'to_outlet', 'quantity_transferred'),
            'description': 'Select source, destination and quantity.'
        }),
        ('Logistics & Tracking', {
            'fields': ('challan_number', 'transferred_by', 'received_by', 'courier_name'),
            'description': 'Details of authorization and transport.'
        }),
    )
    
admin.site.register(Transfer, TransferAdmin)

class TransferHistoryAdmin(admin.ModelAdmin):
    list_display = ('transfer_date', 'product', 'from_outlet', 'to_outlet', 'quantity_transferred', 'challan_number', 'received_by')
    search_fields = ('challan_number', 'transferred_by', 'received_by', 'product__name')
    list_filter = ('from_outlet', 'to_outlet', 'transfer_date')
    date_hierarchy = 'transfer_date'
    actions = [export_as_csv] 
    
    def has_add_permission(self, request): return False

admin.site.register(TransferHistory, TransferHistoryAdmin)

def custom_get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    if not app_dict:
        return []

    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    ordering = {
        "Categories": 1,
        "Sub Categories": 2,
        "Products": 3,
        "Transfers": 4,
        "Transfer History": 5,
        "Outlet Stocks": 6,
        "Log entries": 7,
        "Outlets": 8
    }

    for app in app_list:
        app['models'].sort(key=lambda x: ordering.get(x['name'], 999))
    return app_list

admin.site.site_header = "NexMart Admin Portal"
admin.site.site_title = "NexMart Admin"
admin.site.index_title = "Welcome to NexMart Inventory System"

admin.AdminSite.get_app_list = custom_get_app_list