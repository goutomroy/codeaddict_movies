# Generated by Django 4.0.3 on 2022-04-09 04:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('ticket_price', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0)])),
                ('number_of_tickets', models.PositiveSmallIntegerField(default=10)),
                ('rating', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)])),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='MovieTicket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'default_related_name': 'tickets',
            },
        ),
        migrations.AddConstraint(
            model_name='movieticket',
            constraint=models.UniqueConstraint(fields=('movie', 'user'), name='movies_movieticket_unique_user_movie'),
        ),
    ]
