# Generated by Django 5.1.7 on 2025-03-15 13:19

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, help_text='Rating from 1 to 5 stars.  Leave blank for general feedback.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, help_text='Detailed review or feedback.')),
                ('is_review', models.BooleanField(default=False, help_text='Is this a review (with a rating)?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(help_text='The user who submitted the opinion.', on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Opinion',
                'verbose_name_plural': 'User Opinions',
                'ordering': ['-created_at'],
            },
        ),
    ]
