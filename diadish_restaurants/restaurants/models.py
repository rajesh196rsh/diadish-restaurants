from django.db import models

# Create your models here.

class Menu(models.Model):
    all_type = models.BooleanField(default=False)
    veg = models.BooleanField(default=False)
    pizza = models.BooleanField(default=False)
    momo = models.BooleanField(default=False)
    sweets = models.BooleanField(default=False)
    south_indian = models.BooleanField(default=False)

    def __str__(self):
        menu_type = str(self.id)
        if self.all_type:
            menu_type += " all type"
        if self.veg:
            menu_type += " veg"
        if self.pizza:
            menu_type += " pizza"
        if self.momo:
            menu_type += " momo"
        if self.sweets:
            menu_type += " sweets"
        if self.south_indian:
            menu_type += " south indian"
        
        return menu_type



class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, blank=True)
    average_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    free_delivery = models.BooleanField(default=True)
    address = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
    longitude = models.DecimalField(max_digits=25, decimal_places=20)

    def __str__(self):
        return self.name
