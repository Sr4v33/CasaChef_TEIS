from django.db import models

class DailyProduction(models.Model):
    dish_id = models.PositiveIntegerField()

    date = models.DateField()

    available_units = models.PositiveIntegerField()

    class Meta:
        unique_together = ("dish_id", "date")

    def __str__(self):
        return f"Dish {self.dish_id} - {self.date}"
