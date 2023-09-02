from django.contrib import admin
from .models import * 

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'car_model', 'year', 'plate')
    list_filter = ('brand', 'year')
    search_fields = ('brand', 'plate')
@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_date', 'service_type')
    list_filter = ('vehicle', 'maintenance_date')
@admin.register(FundManagement)
class FundManagementAdmin(admin.ModelAdmin):
    list_display = ('label', 'transaction_date', 'account_number', 'total')
    list_filter = ('label', 'transaction_date')

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position')
    list_filter = ('position', 'sex')
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'invoice_type', 'invoice_location')
    list_filter = ('invoice_type', )
@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'designations', 'quantity_or_days', 'unit_price', 'monthly_price')
    list_filter = ('invoice',)


