# Generated by Django 5.1.4 on 2025-02-05 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_alter_nextdaymeal_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='mess',
            name='lunch_update_time',
            field=models.TimeField(default='08:00'),
        ),
        migrations.AlterField(
            model_name='mess',
            name='meal_update_time',
            field=models.TimeField(default='18:00'),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunch', models.IntegerField(default=0)),
                ('dinner', models.IntegerField(default=0)),
                ('total_meal', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('mess', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meal', to='webapp.mess')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meal', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
