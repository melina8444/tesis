# Generated by Django 3.2.18 on 2023-05-24 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Disponibilidades',
            },
        ),
        migrations.CreateModel(
            name='Campsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('images', models.ImageField(null=True, upload_to='imagenes/')),
            ],
            options={
                'db_table': 'Campings',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField(max_length=10)),
            ],
            options={
                'db_table': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='NaturalPark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('province', models.IntegerField(choices=[(1, 'Buenos Aires'), (2, 'Ciudad Autónoma de Buenos Aires'), (3, 'Catamarca'), (4, 'Chaco'), (5, 'Chubut'), (6, 'Córdoba'), (7, 'Corrientes'), (8, 'Entre Ríos'), (9, 'Formosa'), (10, 'Jujuy'), (11, 'Salta'), (12, 'Tucumán'), (13, 'La Pampa'), (14, 'La Rioja'), (15, 'San Juan'), (16, 'Mendoza'), (17, 'Misiones'), (18, 'Neuquén'), (19, 'Río Negro'), (20, 'San Luis'), (21, 'Santa Cruz'), (22, 'Santa Fé'), (23, 'Santiago del Estero'), (24, 'Tierra del Fuego')])),
                ('image', models.ImageField(null=True, upload_to='imagenes/')),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Parques_Naturales',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.FloatField(auto_created=True, default=0.0, unique=True)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('number_guests', models.IntegerField()),
                ('total_cost', models.FloatField(max_length=10)),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.availability')),
                ('campsite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.campsite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Reservas',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('dni', models.CharField(max_length=255)),
                ('is_client', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Perfiles',
            },
        ),
        migrations.AddField(
            model_name='campsite',
            name='categories',
            field=models.ManyToManyField(related_name='campsites', to='administracion.Category'),
        ),
        migrations.AddField(
            model_name='campsite',
            name='natural_park',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campsites', to='administracion.naturalpark'),
        ),
        migrations.AddField(
            model_name='availability',
            name='campsite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='administracion.campsite'),
        ),
    ]
