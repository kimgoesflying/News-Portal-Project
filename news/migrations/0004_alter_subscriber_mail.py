# Generated by Django 4.0.4 on 2022-05-11 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_subscriber_categorysubscriber_category_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='mail',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
