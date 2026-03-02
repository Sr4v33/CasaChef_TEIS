from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_orderitem_delete_orderitems_delete_orders"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
