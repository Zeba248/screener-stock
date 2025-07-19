from django.db import models
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, default="N/A")
    current_price = models.FloatField(null=True, blank=True)
    price_change = models.FloatField()
    price_change_percent = models.FloatField(null=True, blank=True)
    rsi = models.FloatField(default=50.0)
    volume = models.CharField(max_length=20, default="N/A")
    market_cap = models.CharField(max_length=20, default="N/A")
    is_positive = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    last_fetched = models.DateTimeField(null=True, blank=True)  # When data was fetched from API
    
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
    class Meta:
        ordering = ['-price_change']
