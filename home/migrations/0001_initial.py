# Generated by Django 4.0 on 2025-07-21 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficAccident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('result_of_the_accident', models.CharField(max_length=100)),
                ('number_of_people', models.IntegerField()),
                ('result_of_the_accident_ar', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('year', 'result_of_the_accident')},
            },
        ),
    ]
