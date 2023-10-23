# Generated by Django 4.2.6 on 2023-10-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_ledger', '0004_remove_transaction_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
