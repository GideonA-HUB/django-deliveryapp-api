# Generated by Django 4.2.7 on 2025-04-12 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_price_range_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('preferred_price_range_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('preferred_rating_min', models.FloatField(blank=True, null=True)),
                ('preferred_delivery_time_max', models.PositiveIntegerField(blank=True, help_text='Maximum delivery time in minutes', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('preferred_categories', models.ManyToManyField(blank=True, to='services.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBehavior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('behavior_type', models.CharField(choices=[('view', 'View'), ('search', 'Search'), ('add_to_cart', 'Add to Cart'), ('purchase', 'Purchase'), ('review', 'Review'), ('rating', 'Rating')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField(blank=True, default=dict)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_behaviors', to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='behaviors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PopularService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('purchase_count', models.PositiveIntegerField(default=0)),
                ('average_rating', models.FloatField(default=0)),
                ('total_ratings', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='popularity', to='services.service')),
            ],
            options={
                'ordering': ['-purchase_count'],
            },
        ),
        migrations.CreateModel(
            name='TrendingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=20)),
                ('score', models.FloatField()),
                ('rank', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trending', to='services.service')),
            ],
            options={
                'ordering': ['period', 'rank'],
                'unique_together': {('service', 'period')},
            },
        ),
        migrations.CreateModel(
            name='SimilarService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity_score', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_services', to='services.service')),
                ('similar_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_from', to='services.service')),
            ],
            options={
                'ordering': ['-similarity_score'],
                'unique_together': {('service', 'similar_to')},
            },
        ),
        migrations.CreateModel(
            name='ServiceRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('reason', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-score'],
                'unique_together': {('user', 'service')},
            },
        ),
    ]
