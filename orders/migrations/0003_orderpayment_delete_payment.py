# Generated by Django 4.2.7 on 2025-04-13 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('card', 'Credit/Debit Card'), ('bank_transfer', 'Bank Transfer'), ('cash', 'Cash'), ('mobile_money', 'Mobile Money')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
