import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("email", models.EmailField(unique=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"app_label": "users"},
        ),
        migrations.CreateModel(
            name="CustomerModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=20)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="users.usermodel")),
            ],
            options={"app_label": "users"},
        ),
        migrations.CreateModel(
            name="CookModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("specialty", models.CharField(max_length=255)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="users.usermodel")),
            ],
            options={"app_label": "users"},
        ),
        migrations.CreateModel(
            name="AddressModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=20)),
                ("is_default", models.BooleanField(default=False)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="addresses",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"app_label": "users"},
        ),
    ]
