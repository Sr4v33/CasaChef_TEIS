from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PaymentModel",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ("order_id", models.PositiveIntegerField(blank=True, null=True)),
                ("method", models.CharField(choices=[("CARD", "Card"), ("BANK_TRANSFER", "Bank Transfer"), ("CASH", "Cash")], max_length=20)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("CONFIRMED", "Confirmed"), ("FAILED", "Failed")], default="PENDING", max_length=20)),
                ("transaction_reference", models.CharField(blank=True, max_length=200, null=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="COP", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
