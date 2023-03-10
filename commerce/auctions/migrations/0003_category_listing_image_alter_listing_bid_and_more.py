# Generated by Django 4.1.7 on 2023-03-09 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_category', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
    ]
