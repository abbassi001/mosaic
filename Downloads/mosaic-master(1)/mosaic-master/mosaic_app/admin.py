from typing import Dict, List, Optional
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.urls.resolvers import URLPattern
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Q
from .models import * 
from .forms import *

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'car_model', 'year', 'plate')
    # list_filter = ('brand', 'year')
    search_fields = ('brand', 'plate')
    
@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_date', 'service_type')
    # list_filter = ('vehicle', 'maintenance_date')
    
    
@admin.register(FundManagement)
class FundManagementAdmin(admin.ModelAdmin):
    list_display = ('label', 'account_number', 'action')
    # list_filter = ('label', 'transaction_date')
    
    def action(self, obj):
        link = "<a class='btn btn-info' href='%s/details'>Details</a>"%obj.id
        return format_html(link)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:fundmanagement_id>/details/", self.admin_site.admin_view(self.details), name="fundmanagement-details"),
        ]
        return custom_urls + urls
    
    def details(self, request, fundmanagement_id, *args, **kwargs):
        model = FundManagement
        template_name = "admin/mosaic_app/fundmanagement/details.html"
        fundmanagement = get_object_or_404(FundManagement, id=fundmanagement_id)
        items = fundmanagement.items.all()
        fundItemFormset = FundItemFormset(request.POST or None, queryset=items)
        
        if request.GET.get("mode") == "print":
            context = {
                "fundmanagement": fundmanagement,
            }
            return render(request, "admin/mosaic_app/fundmanagement/print.html", context=context)
        
        if request.method == 'POST':
            if fundItemFormset.is_valid():
                instances = fundItemFormset.save(commit=False)
                for instance in instances:
                    instance.fundmanagement = fundmanagement 
                    instance.save()
                return redirect("admin:fundmanagement-details", fundmanagement_id)
            
        context = dict(
            self.admin_site.each_context(request),
            opts = model._meta,
            add = self.has_add_permission(request),
            change = self.has_change_permission(request),
            app_label = "mosaic_app",
            fundmanagement = fundmanagement,
            fundItemFormset = fundItemFormset,
            has_add_permission = self.has_add_permission(request),
            app_list = self.admin_site.get_app_list(request)
        )
        
        return render(request, template_name=template_name, context=context)
    
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        my_chats = Chat.objects.filter(participants__id=request.user.id)
        extra_context['chats'] = my_chats
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("new-chat", self.admin_site.admin_view(self.new_chat), name="new-chat"),
            path("chatting/<str:reference_code>", self.admin_site.admin_view(self.chatting), name="chatting"),
        ]
        return custom_urls + urls
    
    def new_chat(self, request, *args, **kwargs):
        model = Chat
        template_name = "admin/mosaic_app/chat/new-chat.html"
        
        my_chats = Chat.objects.filter(participants__id=request.user.id)
        removed_users = []
        for mc in my_chats:
            if mc.participants.count() == 2:
                for usr in mc.participants.all():
                    if usr != request.user:
                        removed_users.append(usr.id)
                        
        users = User.objects.filter(~Q(id=request.user.id)).filter(~Q(id__in=removed_users))
                
        if request.GET.get("start_chat") == 'true' and request.GET.get("uid"):
            user = User.objects.filter(id=request.GET.get("uid")).first()
            if user:
                chat = Chat()
                chat.title = "%s"%user
                chat.save()
                chat.participants.add(user, request.user)
                return redirect('admin:chatting', chat.reference_code)
                    
        context = dict(
            self.admin_site.each_context(request),
            opts = model._meta,
            add = self.has_add_permission(request),
            change = self.has_change_permission(request),
            app_label = "mosaic_app",
            users = users,
            has_add_permission = self.has_add_permission(request),
            app_list = self.admin_site.get_app_list(request)
        )
        
        return render(request, template_name=template_name, context=context)
    
    def chatting(self, request, reference_code, *args, **kwargs):
        model = Chat
        template_name = "admin/mosaic_app/chat/chatting.html"
        chats = Chat.objects.filter(participants__id=request.user.id)
        
        chat = get_object_or_404(Chat, reference_code=reference_code)
        
        if request.method == "POST":
            chat.histories.create(sender=request.user, message=request.POST.get("message"))
            return redirect("admin:chatting", chat.reference_code)
                
        context = dict(
            self.admin_site.each_context(request),
            opts = model._meta,
            add = self.has_add_permission(request),
            change = self.has_change_permission(request),
            app_label = "mosaic_app",
            chat = chat,
            chats = chats,
            has_add_permission = self.has_add_permission(request),
            app_list = self.admin_site.get_app_list(request)
        )
        
        return render(request, template_name=template_name, context=context)
    
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position')
    # list_filter = ('position', 'sex')
    
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra=2 
    readonly_fields=['monthly_price']

    
@admin.register(Invoice) 
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_type', 'invoice_location', 'status', 'action')
    list_filter = ('status', )
        
    def action(self, obj):
        link = "<a class='btn btn-info' href='%s/details'>Details</a>"%obj.id
        return format_html(link)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:invoice_id>/details/", self.admin_site.admin_view(self.details), name="invoice-details"),
        ]
        return custom_urls + urls
    
    def details(self, request, invoice_id, *args, **kwargs):
        model = Chat
        template_name = "admin/mosaic_app/invoice/details.html"
        invoice = get_object_or_404(Invoice, id=invoice_id)
        items = InvoiceItem.objects.filter(invoice=invoice)
        invoiceItemFactory = InvoiceItemFormset(request.POST or None, queryset=items)
        
        if request.GET.get("mode") == "print":
            context = {
                "invoice": invoice,
            }
            return render(request, "admin/mosaic_app/invoice/print.html", context=context)
        
        if request.method == 'POST':
            if invoiceItemFactory.is_valid():
                instances = invoiceItemFactory.save(commit=False)
                for instance in instances:
                    instance.invoice = invoice  # Assign the invoice to each item
                    instance.save()
                return redirect("admin:invoice-details", invoice.id)
            
        context = dict(
            self.admin_site.each_context(request),
            opts = model._meta,
            add = self.has_add_permission(request),
            change = self.has_change_permission(request),
            app_label = "mosaic_app",
            invoice = invoice,
            invoiceItemFactory = invoiceItemFactory,
            has_add_permission = self.has_add_permission(request),
            app_list = self.admin_site.get_app_list(request)
        )
        
        return render(request, template_name=template_name, context=context)
    

@admin.register(ArchivedDocument)
class ArchivedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'upload_date', 'document_type', 'is_confidential')
    list_filter = ('document_type', 'is_confidential')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('upload_date',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
                    
        return super().save_model(request, obj, form, change)
