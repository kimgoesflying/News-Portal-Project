# Generated by Django 4.0.4 on 2022-05-10 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CategorySubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.subscriber')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscriber',
            field=models.ManyToManyField(through='news.CategorySubscriber', to='news.subscriber'),
        ),
    ]
