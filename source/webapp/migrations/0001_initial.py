# Generated by Django 3.2.7 on 2021-09-24 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('category', models.TextField(choices=[('drink', 'Напиток'), ('food', 'Еда')], max_length=15, verbose_name='Category')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_order', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dish_in_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='webapp.dish', verbose_name='Dish in order')),
            ],
        ),
    ]