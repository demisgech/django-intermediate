# Generated by Django 5.2 on 2025-04-23 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'can cancel order')]},
        ),
    ]
