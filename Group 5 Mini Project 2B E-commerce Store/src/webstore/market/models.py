from django.db import models
from storefront.models import Seller, Listing, User, Category

class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=False, blank=False, default=2.5)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f"{self.listing} {self.reviewer}"

class Interaction(models.Model):
    listing = models.ForeignKey(Listing, related_name='interactions', blank=True, null=True, on_delete=models.CASCADE)
    User = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    action = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

class userInterests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.FloatField()

class cluster(models.Model):
    cluster = models.AutoField(primary_key=True)

class userClusters(models.Model):
    cluster = models.ForeignKey(cluster, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corelation = models.FloatField()

class clusterCorelations(models.Model):
    cluster = models.ForeignKey(cluster, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    corelation = models.FloatField()

class itemCorelations(models.Model):
    category1 = models.ForeignKey(Category, related_name='category1_corelations', on_delete=models.CASCADE)
    category2 = models.ForeignKey(Category, related_name='category2_corelations', on_delete=models.CASCADE)
    corelations = models.FloatField()

class userRecommendations(models.Model):
    listing = models.ForeignKey(Listing, related_name='recommendations', blank=True, null=True, on_delete=models.CASCADE)
    User = models.ForeignKey(User, related_name='person', on_delete=models.CASCADE)