from django.db import models
from django.contrib.auth.models import User



CALORIES = (
    (1000, "1000"),
    (1100, "1100"),
    (1200, "1200"),
    (1300, "1300"),
    (1400, "1400"),
    (1500, "1500"),
    (1600, "1600"),
    (1700, "1700"),
    (1800, "1800"),
    (1900, "1900"),
    (2000, "2000"),
    (2100, "2100"),
    (2200, "2200"),
    (2300, "2300"),
    (2400, "2400"),
    (2500, "2500"),
    (2600, "2600"),
    (2700, "2700"),
    (2800, "2800"),
    (2900, "2900"),
    (3000, "3000"),
)


GENRE = (
    (0, "Śniadanie"),
    (1, "Obiad"),
    (2, "Kolacja"),
    (3, "Przekąska"),
)


class FoodItem(models.Model):
    name = models.CharField(max_length=200, verbose_name="Posiłek")
    weight = models.DecimalField(null=True, max_digits=6, decimal_places=2, verbose_name="Waga")
    calories = models.DecimalField(null=True, max_digits=6, decimal_places=2, verbose_name="Kalorie")
    protein = models.DecimalField(null=True, max_digits=6, decimal_places=2, verbose_name="Białko")
    carbs = models.DecimalField(null=True, max_digits=6, decimal_places=2, verbose_name="Węglowodany")
    fats = models.DecimalField(null=True, max_digits=6, decimal_places=2, verbose_name="Tłuszcze")
    genre = models.IntegerField(choices=GENRE, default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desirable_intake = models.IntegerField(default=0, choices=CALORIES, verbose_name="Dzienna liczba kalorii")
    daily_calories = models.FloatField(null=True, blank=True,)
    foods = models.ManyToManyField(FoodItem)

    def __str__(self):
        return str(self.user.username)


class History(models.Model):
    day_calories = models.DecimalField(max_digits=8, decimal_places=2)
    day_protein = models.DecimalField(max_digits=8, decimal_places=2)
    day_carbs = models.DecimalField(max_digits=8, decimal_places=2)
    day_fats = models.DecimalField(max_digits=8, decimal_places=2)
    day = models.DateField(auto_now_add=True)