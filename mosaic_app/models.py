from django.db import models


class VehicleManagement(models.Model):
    brand = models.CharField("Brand", max_length=200)
    car_model = models.CharField("Model", max_length=200)
    year = models.PositiveIntegerField("Year")
    mileage = models.PositiveIntegerField()
    color = models.CharField(max_length=100)
    vin = models.CharField(max_length=17, unique=True)  # VIN is usually 17 characters long and unique
    insurance_company = models.CharField(max_length=200)
    insurance_policy_number = models.CharField(max_length=100, unique=True)  # Assuming this should be unique for each vehicle
    current_service_schedule = models.DateField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class VehicleMaintenance(models.Model):
    vehicle = models.ForeignKey(VehicleManagement, on_delete=models.CASCADE)  # This creates a relation between VehicleMaintenance and VehicleManagement
    maintenance_date = models.DateField()
    service_type = models.CharField(max_length=200)  # Service type field
    parts_used = models.TextField()  # Parts used as a TextField. You can also consider using a ManyToMany field if you have a parts table.
    notes = models.TextField()  # Notes regarding the maintenance

    def __str__(self):
        return f"{self.vehicle} - {self.service_type} on {self.maintenance_date}"

class FundManagement(models.Model):
    label = models.CharField(max_length=200)
    transaction_date = models.DateField()
    account_number = models.CharField(max_length=20, null=True, blank=True)
    entries = models.TextField()
    quantities = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
     





"""
This module defines the data models for a vehicle management system in Django.

1. VehicleManagement:
    Represents individual vehicles with attributes such as make,
    model, year of manufacture, mileage, color, and related insurance details
    . The VIN (Vehicle Identification Number) and insurance policy number are unique for each vehicle entry. 
     The model also defines a string representation for better readability in the admin interface and other places.

2. VehicleMaintenance:
    Represents maintenance records for vehicles. 
    Each record links to a vehicle (foreign key relation)
    and has attributes to specify the date of maintenance,
    the type of service performed, parts used, and any additional notes. 
    The string representation provides a quick overview of the service type and date for a given vehicle.

3. FundManagement:
    Represents financial management records with attributes for date,
    account number, entries, quantities, and total amounts.
    There's also an attribute to track withdrawals, which can either be from cash or labels.
"""
