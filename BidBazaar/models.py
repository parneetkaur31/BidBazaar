from unittest import loader
from django.db import models
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your models here.
    

class Listing(models.Model):
    ItemCategory = [
        ("APR", "Apartments"),
        ("CAR", "Cars"),
        ("ELE", "Electronics"),
        ("FUR", "Furniture"),
        ("FAS", "Fashion"),
        ("OTH", "Others")
    ]

    AuctionStatus = [
        ("UP", "Upcoming"),
        ("AC", "Active"),
        ("PA", "Past"),
        ("WI", "Withdrawn")
    ]


    list_id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, default="")
    desc = models.TextField(null=False, max_length=1500, default="")
    img = models.ImageField(upload_to='pictures/')
    category = models.CharField(max_length=3, choices=ItemCategory)
    base_prize = models.IntegerField(null=False)
    incr_prize = models.IntegerField(null=False)
    no_of_bids = models.IntegerField(null=False, default=0)
    latest_bid_prize = models.IntegerField(null=False, default=0)
    start_auc = models.DateTimeField(null=False)
    end_auc = models.DateTimeField(null=False)
    auc_status = models.CharField(max_length=2, choices=AuctionStatus, default='PA')


class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amt = models.IntegerField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

