# Generated by Django 4.2 on 2023-05-04 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_alter_alimony_must_pay_alter_alimony_recipient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mustpayreceipt',
            old_name='own_receipt',
            new_name='must_pay',
        ),
        migrations.RenameField(
            model_name='recipientchild',
            old_name='mother',
            new_name='recipient',
        ),
    ]
