# Generated by Django 3.2.18 on 2023-12-21 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title')),
                ('reference_code', models.CharField(max_length=50, null=True, unique=True, verbose_name='Reference code')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Participants')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
            },
        ),
        migrations.CreateModel(
            name='FundManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200, verbose_name='Label')),
                ('account_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Account Number')),
            ],
            options={
                'verbose_name': 'Fund management ',
                'verbose_name_plural': 'Fund managements',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_type', models.CharField(choices=[('commercial_invoice', 'Commercial Invoice'), ('other_invoice', 'Other Invoice')], default='commercial_invoice', max_length=50)),
                ('invoice_number', models.CharField(max_length=50, null=True, unique=True, verbose_name='Invoice number')),
                ('invoice_date', models.DateField(null=True, verbose_name='Invoice Date')),
                ('client_information', models.TextField(verbose_name='Client Information')),
                ('invoice_object', models.TextField(help_text='Reason for the invoice', verbose_name='Reason')),
                ('invoice_location', models.CharField(max_length=255, verbose_name='Invoice Location')),
                ('bank_account', models.CharField(blank=True, max_length=50, null=True, verbose_name='Bank Account')),
                ('status', models.CharField(choices=[['unpaid', 'Unpaid'], ['paid', 'Paid']], default='unpaid', max_length=50, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_photo', models.ImageField(blank=True, max_length=1000, null=True, upload_to='employees/photos/', verbose_name='Passport Photo')),
                ('title', models.CharField(blank=True, choices=[('mr', 'Mr'), ('mrs', 'Mrs'), ('miss', 'Miss')], max_length=1000, null=True, verbose_name='Title')),
                ('first_name', models.CharField(max_length=1000, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=11000, null=True, verbose_name='Last Name')),
                ('biginning_date', models.DateField(blank=True, null=True, verbose_name='Beginning date of service')),
                ('employee_no', models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='Employee number')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=1000, null=True, verbose_name='Gender')),
                ('phone', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=1000, null=True, verbose_name='Email address')),
                ('emergency_phone', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Emergency Phone')),
                ('nationality', models.CharField(blank=True, max_length=50, null=True, verbose_name='nationality')),
                ('id_card', models.CharField(blank=True, max_length=1000, null=True, verbose_name='NID NUMBER')),
                ('place_of_issue', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Place of issue')),
                ('Insurance_number', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Insurance Number ')),
                ('employee_bank', models.CharField(blank=True, max_length=50, null=True, verbose_name='Bank')),
                ('bank_account', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Account Number')),
                ('marital_status', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('widow', 'Widow(er)'), ('divorced', 'Divorced')], max_length=1000, null=True, verbose_name='Maritial status')),
                ('position', models.CharField(help_text='CEO, Secretariat,accountant,internee', max_length=100, null=True, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Staff ',
                'verbose_name_plural': 'Staffs',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(null=True, upload_to='vehicle', verbose_name='Picture')),
                ('brand', models.CharField(max_length=200, verbose_name='Brand')),
                ('car_model', models.CharField(max_length=200, verbose_name='Car Model ')),
                ('year', models.PositiveIntegerField(verbose_name='Year ')),
                ('mileage', models.PositiveIntegerField(verbose_name='MileAge')),
                ('color', models.CharField(max_length=100, verbose_name='Color')),
                ('plate', models.CharField(max_length=17, null=True, unique=True, verbose_name='Plate')),
                ('insurance_company', models.CharField(max_length=200, verbose_name='Insurance Company')),
                ('insurance_policy_number', models.CharField(max_length=100, unique=True, verbose_name='Insurance Policy Number')),
                ('current_service_schedule', models.DateField(verbose_name='Current Service Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_picture', models.FileField(null=True, upload_to='Vehicle_Maintenance_Picture', verbose_name='Vehicle Picture')),
                ('maintenance_date', models.DateField(verbose_name='Maintenance Date')),
                ('service_type', models.CharField(max_length=200, verbose_name='Service Type ')),
                ('maintenance_comments', models.TextField(null=True, verbose_name='Maintenance Comments ')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mosaic_app.vehicle', verbose_name='Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designations', models.CharField(max_length=255)),
                ('quantity_or_days', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mosaic_app.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='FundItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(verbose_name='Transaction Date')),
                ('designation', models.CharField(max_length=255, verbose_name='Designation')),
                ('unit_price', models.CharField(max_length=50, verbose_name='Unit price')),
                ('total', models.CharField(max_length=50, verbose_name='Total')),
                ('observation', models.CharField(max_length=255, verbose_name='Observation')),
                ('fundmanagement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mosaic_app.fundmanagement', verbose_name='Fund Management')),
            ],
            options={
                'verbose_name': 'Fund Item',
                'verbose_name_plural': 'Fund Items',
                'db_table': 'fund_items',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='mosaic_app.chat', verbose_name='Chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Chat History',
                'verbose_name_plural': 'Chat Histories',
            },
        ),
        migrations.CreateModel(
            name='ArchivedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='archived_documents/', verbose_name='Document')),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='Upload Date')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('document_type', models.CharField(choices=[('pdf', 'PDF'), ('docx', 'Word'), ('xlsx', 'Excel'), ('txt', 'Text'), ('other', 'Other')], default='other', max_length=20, verbose_name='Document Type')),
                ('is_confidential', models.BooleanField(default=False, verbose_name='Confidential')),
                ('uploaded_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uploaded By')),
            ],
            options={
                'verbose_name': 'Archived Document',
                'verbose_name_plural': 'Archived Documents',
            },
        ),
    ]
