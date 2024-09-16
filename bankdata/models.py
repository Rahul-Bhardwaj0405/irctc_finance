# bankdata/models.py
from django.db import models

class BankData(models.Model):
    BANK_CHOICES = [
        ('hdfc', 'HDFC'),
        ('icici', 'ICICI'),
        # Add more banks as needed
    ]

    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES)
    year = models.IntegerField()
    month = models.CharField(max_length=20)
    booking_or_refund = models.CharField(max_length=20)  # 'booking' or 'refund'
    date = models.DateField()
    extracted_data = models.JSONField()  # Store data in a flexible JSON format

    def __str__(self):
        return f"{self.bank_name} - {self.year}-{self.month} - {self.booking_or_refund} - {self.date}"
