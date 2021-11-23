# Generated by Django 3.2.9 on 2021-11-22 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingrediant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time_miniutes', models.IntegerField()),
                ('prince', models.DecimalField(decimal_places=2, max_digits=5)),
                ('link', models.CharField(blank=True, max_length=255)),
                ('ingregiants', models.ManyToManyField(to='core.Ingrediant')),
                ('tags', models.ManyToManyField(to='core.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]