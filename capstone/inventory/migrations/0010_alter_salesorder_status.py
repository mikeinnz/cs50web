# Generated by Django 3.2.9 on 2021-12-05 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_alter_salesorder_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('CREATED', 'Created'), ('INVOICED', 'Invoiced'), ('DISPATCHED', 'Dispatched'), ('PAID', 'Paid'), ('CLOSED', 'Closed')], default='CREATED', max_length=32),
        ),
    ]
