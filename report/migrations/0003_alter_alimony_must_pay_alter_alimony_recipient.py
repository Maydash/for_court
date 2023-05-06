# Generated by Django 4.2 on 2023-05-04 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_remove_alimony_must_pay_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimony',
            name='must_pay',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.mustpay', verbose_name='Bergidaryn ady, familiyasy'),
        ),
        migrations.AlterField(
            model_name='alimony',
            name='recipient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.recipient', verbose_name='Algydaryn ady, familiyasy'),
        ),
    ]