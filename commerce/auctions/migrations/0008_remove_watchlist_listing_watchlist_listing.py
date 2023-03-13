# Generated by Django 4.1.7 on 2023-03-13 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(null=True, related_name='listing', to='auctions.listing'),
        ),
    ]