import random, string
from typing import Iterable, Optional
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

class Vehicle(models.Model):
    """
    Represents individual vehicles with attributes such as make,
    model, year of manufacture, mileage, color, and related insurance details
    The plate VIN (Vehicle Identification Number) and insurance policy number are unique for each vehicle entry. 
     The model also defines a string representation for better readability in the admin interface and other places.
    """
    picture=models.FileField(_("Picture"), upload_to='vehicle',null=True)
    brand = models.CharField(_("Brand"), max_length=200)
    car_model = models.CharField(_("Car Model "), max_length=200)
    year = models.PositiveIntegerField(_("Year "))
    mileage = models.PositiveIntegerField(_("MileAge"))
    color = models.CharField(_("Color"), max_length=100)
    plate = models.CharField(_("Plate"),max_length=17, unique=True,null=True)  # VIN is usually 17 characters long and unique
    insurance_company = models.CharField(_("Insurance Company"), max_length=200)
    insurance_policy_number = models.CharField(_("Insurance Policy Number"),max_length=100, unique=True)  # Assuming this should be unique for each vehicle
    current_service_schedule = models.DateField(_("Current Service Schedule"))

    def __str__(self):
        return f"{self.brand} {self.car_model}"
    

class VehicleMaintenance(models.Model):
    """
    Represents maintenance records for vehicles. 
    Each record links to a vehicle (foreign key relation)
    and has attributes to specify the date of maintenance,
    the type of service performed, parts used, and any additional notes. 
    The string representation provides a quick overview of the service type and date for a given vehicle.
    """
    vehicle_picture=models.FileField(_("Vehicle Picture"), upload_to='Vehicle_Maintenance_Picture', max_length=100,null=True)
    # vehicle = models.ForeignKey(model=VehicleManagement, verbose_name=_("Vehicle"), on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, verbose_name=_("Vehicle"), on_delete=models.CASCADE)
    maintenance_date = models.DateField(_("Maintenance Date"))
    service_type = models.CharField(_("Service Type "), max_length=200)  # Service type field
    maintenance_comments = models.TextField(_("Maintenance Comments "),null=True)  # Notes regarding the maintenance
    def __str__(self):
        return f"{self.vehicle} - {self.service_type} on {self.maintenance_date}"

class FundManagement(models.Model):
    """
    Represents financial management records with attributes for date,
    account number, entries, quantities, and total amounts.
    There's also an attribute to track withdrawals, which can either be from cash or labels.
    """
    label = models.CharField(_("Label"),max_length=200)
    account_number = models.CharField(_("Account Number"),max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.label}"
    
    def grand_total(self):
        t = self.items.aggregate(total=Sum("total"))
        return t['total'] or 0
    
    class Meta:
        verbose_name = _("Fund management ")
        verbose_name_plural = _("Fund managements")
        
class FundItem(models.Model):
    fundmanagement = models.ForeignKey("FundManagement", related_name="items", verbose_name=_("Fund Management"), on_delete=models.CASCADE)
    transaction_date = models.DateField(_("Transaction Date"))
    designation = models.CharField(_("Designation"), max_length=255)
    unit_price = models.CharField(_("Unit price"), max_length=50)
    total = models.CharField(_("Total"), max_length=50)
    observation = models.CharField(_("Observation"), max_length=255)    

    def __str__(self):
        return ""

    class Meta:
        db_table = 'fund_items'
        managed = True
        verbose_name = 'Fund Item'
        verbose_name_plural = 'Fund Items'
    
class Chat(models.Model):
    title = models.CharField(_("Title"), null=True, blank=True, max_length=50)
    reference_code = models.CharField(_("Reference code"), unique=True, max_length=50, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Participants"))
    
    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.reference_code:
            ref = "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(32))
            self.reference_code = ref
        
        super().save(*args, **kwargs)

class ChatHistory(models.Model):
    chat = models.ForeignKey("Chat", verbose_name=_("Chat"), related_name='histories', on_delete=models.CASCADE)    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE, verbose_name=_("Sender"))
    message = models.TextField(_("Message"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)  # Automatically set the field to now when the object is first created.

    class Meta:
        verbose_name = _("Chat History")
        verbose_name_plural = _("Chat Histories")

    def __str__(self):
        return f"{self.chat}"

class Staff (models.Model):
   
    sex_options = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]
    
    marital_choices= [
        ('single', _('Single')),
        ('married', _('Married')),
        ('widow', _('Widow(er)')),
        ('divorced', _('Divorced')),
    ]

    title_choices = [
        ('mr', _('Mr')),
        ('mrs', _('Mrs')),
        ('miss', _('Miss')),
    ]
    passport_photo = models.ImageField(_("Passport Photo"), upload_to='employees/photos/', max_length=1000, null=True, blank=True)

    title = models.CharField(_('Title'),choices=title_choices,max_length=1000, null=True, blank=True)
    first_name = models.CharField(_('First Name'), max_length=1000, null=True)
    last_name = models.CharField(_('Last Name'), max_length=11000, null=True)
    biginning_date = models.DateField(_("Beginning date of service"), auto_now=False, auto_now_add=False, null=True, blank=True)
    employee_no = models.CharField(_("Employee number"), max_length=1000, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(_("Date of birth"), null=True, blank=True, auto_now=False, auto_now_add=False)
    sex = models.CharField(_("Gender"), choices=sex_options, max_length=1000, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=1000, null=True, blank=True)
    email = models.EmailField(_("Email address"), null=True, blank=True, max_length=1000) 
    emergency_phone = models.CharField(_("Emergency Phone"), max_length=1000, null=True, blank=True)
    # nationality = models.CharField("country.Country", verbose_name=_("nationality"), on_delete=models.CASCADE, null=True, blank=True)
    nationality = models.CharField(max_length=50, verbose_name=_("nationality"), null=True, blank=True)

    id_card = models.CharField(_("NID NUMBER"), max_length=1000, null=True, blank=True)
    place_of_issue = models.CharField(_("Place of issue"), max_length=1000, null=True, blank=True)
    Insurance_number = models.CharField(_("Insurance Number "), max_length=1000, null=True, blank=True)
    # employee_bank = models.CharField("Bank", verbose_name=_("Bank"), null=True, blank=True, on_delete=models.CASCADE)
    employee_bank = models.CharField(max_length=50, verbose_name=_("Bank"), null=True, blank=True)
    bank_account = models.CharField(_("Account Number"), null=True, blank=True, max_length=1000)
    marital_status = models.CharField(_("Maritial status"), choices=marital_choices, max_length=1000, null=True, blank=True)
    # position = models.CharField(_("Position"), help_text='CEO, Secretariat,accountant,internee', on_delete=models.CASCADE, null=True, blank=False)
    position = models.CharField(_("Position"), max_length=100, help_text='CEO, Secretariat,accountant,internee', null=True, blank=False)

    
    class Meta:
        verbose_name = _("Staff ")
        verbose_name_plural = _("Staffs")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Create your models here.
class Invoice(models.Model):
   
    statuses = [
        ['unpaid', 'Unpaid'],
        ['paid', 'Paid'],
    ]
    COMMERCIAL_INVOICE = 'commercial_invoice'
    OTHER_INVOICE = 'other_invoice'
    
    INVOICE_TYPE_CHOICES = [
        (COMMERCIAL_INVOICE, _('Commercial Invoice')),
        (OTHER_INVOICE, _('Other Invoice')),
    ]

    invoice_type = models.CharField(max_length=50,choices=INVOICE_TYPE_CHOICES,default=COMMERCIAL_INVOICE,)
    invoice_number = models.CharField(_("Invoice number"), max_length=50, unique=True, null=True)
    invoice_date = models.DateField(_("Invoice Date"), auto_now=False, auto_now_add=False, null=True)
    client_information = models.TextField(_("Client Information"))
    invoice_object = models.TextField(_("Reason"), help_text="Reason for the invoice")
    invoice_location = models.CharField(_("Invoice Location"), max_length=255)
    bank_account = models.CharField(_("Bank Account"), max_length=50, null=True, blank=True)
    status = models.CharField(_("Status"), choices=statuses, default="unpaid", max_length=50)
    
    def __str__(self):
        return "%s"%self.invoice_number
    
    def total_amount(self):
        total_monthly_price = self.items.aggregate(total=Sum('monthly_price'))
        return total_monthly_price['total']

class InvoiceItem(models.Model):
    
    invoice = models.ForeignKey(Invoice, related_name='items',on_delete=models.CASCADE)
    designations = models.CharField(max_length=255)
    quantity_or_days = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.designations
    

    def save(self, *args, **kwargs):
        self.monthly_price=self.quantity_or_days * self.unit_price
        
        super().save(*args, **kwargs)
        
class ArchivedDocument(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('xlsx', 'Excel'),
        ('txt', 'Text'),
        ('other', 'Other')
    ]

    document = models.FileField(_("Document"), upload_to='archived_documents')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Uploaded By"))
    upload_date = models.DateTimeField(_("Upload Date"), auto_now_add=True)
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    document_type = models.CharField(_("Document Type"), choices=DOCUMENT_TYPES, default='other', max_length=20)
    is_confidential = models.BooleanField(_("Confidential"), default=False)
    
    class Meta:
        verbose_name = _("Archived Document")
        verbose_name_plural = _("Archived Documents")

    def __str__(self):
        return f"{self.title} - Uploaded by {self.uploaded_by} on {self.upload_date}"



"""
This module defines the data models for a vehicle management system in Django.

1. VehicleManagement:

2. VehicleMaintenance:
    

3. FundManagement:
    
"""
