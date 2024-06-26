from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    oldprice = models.IntegerField(null=True)
    color = models.CharField(max_length=50, null=True)
    picture = models.ImageField(upload_to='product_images/', null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    GENDER = (
        ('Men','Men'),
        ('Women', 'Women')
    )
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    CATEGORY = (
        ('Formal Shoes', 'Formal Shoes'),
        ('Peshawari', 'Peshawari'),
        ('Loafers', 'Loafers'),
        ('Khussa', 'Khussa'),
        ('High Heels', 'High Heels'),
    )
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    AVAILABILITY = (
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock')
    )
    availability = models.CharField(max_length=200, null=True, choices=AVAILABILITY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.address