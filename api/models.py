from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
        The category represents the type of product.
        Each product must have a single category.
        For example: Car, Mobile
    """

    title = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    """
        Product is an item whose ad is created by the user.
        A user can create multiple products.
    """

    title = models.TextField(null=False)
    description = models.TextField(null=False)
    base_price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid_till = models.DateTimeField(null=False)
    creator = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    

class Bid(models.Model):
    """
        A bid is a record representing the a user's claim of interest
        or offer for a product. A user can make only one bid for a product
    """

    class Meta:
        unique_together = (("bidder", "product"),)

    bidder = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    bid_amount = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bid_amount
    
