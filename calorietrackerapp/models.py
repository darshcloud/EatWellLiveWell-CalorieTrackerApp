from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class Food_Cat(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_food_by_category(self):
        return Food_Obj.objects.filter(category=self).count()


class Food_Obj(models.Model):
    food_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.IntegerField(default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Food_Cat, on_delete=models.CASCADE, related_name='food_category')

    def __str__(self):
        return f'{self.food_name} - category: {self.category}'


class Image(models.Model):
    food = models.ForeignKey(Food_Obj, on_delete=models.CASCADE, related_name='get_images')
    image = models.ImageField()

    def __str__(self):
        return f'{self.image}'

        
class Food_log_mdl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food_Obj, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Log'

    def __str__(self):
        return f'{self.user.username} - {self.food_consumed.food_name}'

class UserWeight(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    user_weight = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weight'

    def __str__(self):
        return f'{self.user_name.username} - {self.user_weight} lb on {self.entry_date}'



