from typing import Dict, List, Optional
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.urls.resolvers import URLPattern
from django.contrib.auth.models import User
from django.db.models import Q
from .models import * 

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
    list_display = ('label', 'transaction_date', 'account_number', 'total')
    # list_filter = ('label', 'transaction_date')
    

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
            print(mc.participants)
            if mc.participants.count() == 2:
                for usr in mc.participants.all():
                    if usr != request.user:
                        removed_users.append(usr.id)
                        print(usr)
                        
        users = User.objects.filter(~Q(id=request.user.id)).filter(~Q(id__in=removed_users))
                
        if request.GET.get("start_chat") == 'true' and request.GET.get("uid"):
            user = User.objects.filter(id=request.GET.get("uid")).first()
            if user:
                chat = Chat()
                chat.title = "%s"%user
                chat.save()
                chat.participants.add(user, request.user)
                print(chat.participants)
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
        
        for c in chats:
            print(c.participants.all())
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
    
class ItemInline(admin.TabularInline):
    model = Item
    extra=2 
    readonly_fields=['monthly_price']

    
@admin.register(Invoice) 
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'invoice_type', 'invoice_location')
    # list_filter = ('invoice_type', )
    
    inlines=[ItemInline]
    



