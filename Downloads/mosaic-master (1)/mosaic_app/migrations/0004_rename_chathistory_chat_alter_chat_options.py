# Generated by Django 4.2.2 on 2023-09-02 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mosaic_app', '0003_invoice_staff_vehicle_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatHistory',
            new_name='Chat',
        ),
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['timestamp'], 'verbose_name': 'Chat', 'verbose_name_plural': 'Chats'},
        ),
    ]
