from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    pfp = models.ImageField(upload_to=f'pfps/', default='user.png')


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def  __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    store_name = models.CharField(max_length=256)
    desc = models.TextField(blank=True)
    trust_score =  models.FloatField(default=50.0)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.user.email} {self.store_name}"
    

class Payment_Method(models.Model):
    SELLER_CHOICES = [
        ('UPI', 'UPI'),
        ('Card', 'Debit/Credit Card'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=SELLER_CHOICES)
    acc_holder_name = models.CharField(max_length=100, blank=True, null=True)
    upi_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.seller} - {self.method}"
    

class Category(models.Model):
        name = models.CharField(max_length=30)
        
        def __str__(self):
            return self.name
    

class Product(models.Model):
    product_name =  models.CharField(max_length=256)
    brand_name = models.CharField(max_length=256)
    specs = models.TextField(help_text="Product specifications")
    desc = models.TextField()
    category = models.ManyToManyField(Category)
    img = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.product_name

class Product_Images(models.Model):
    img = models.ImageField(upload_to='products/', default='no-default')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    
class Listing(models.Model):
    name  = models.CharField(max_length=80)
    inventory = models.IntegerField(default=0)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    current_price = models.IntegerField()
    rating = models.PositiveIntegerField(null=False, blank=False, default=2.5)

    strategy = models.FloatField(default=0.0)
    slug = models.SlugField(default="", null=False)



    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
# Create your models here.
