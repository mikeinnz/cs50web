# Generated by Django 3.0.5 on 2021-11-06 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20211106_0555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='winner',
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auctions.Listing')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='won', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
