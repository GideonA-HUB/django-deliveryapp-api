# Generated by Django 4.2.7 on 2025-04-13 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_business_description_businessprofile_description_and_more'),
        ('orders', '0002_orderstatus'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0002_deliveryzone_businesses_deliveryzone_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('picked_up', 'Picked Up'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('actual_pickup_time', models.DateTimeField(blank=True, null=True)),
                ('actual_delivery_time', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='orders.order')),
                ('rider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveries', to='accounts.riderprofile')),
            ],
            options={
                'verbose_name_plural': 'Deliveries',
            },
        ),
        migrations.RemoveField(
            model_name='deliveryrating',
            name='assignment',
        ),
        migrations.AddField(
            model_name='deliveryrating',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deliveryzone',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='deliveryzone',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryrating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
        migrations.AlterField(
            model_name='deliveryzone',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='DeliveryTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('picked_up', 'Picked Up'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=20)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracking', to='delivery.delivery')),
            ],
            options={
                'verbose_name_plural': 'Delivery tracking',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='delivery',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to='delivery.deliveryzone'),
        ),
        migrations.AddField(
            model_name='deliveryrating',
            name='delivery',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='delivery.delivery'),
        ),
    ]
