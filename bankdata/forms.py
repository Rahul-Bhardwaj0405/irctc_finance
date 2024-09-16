

# forms.py
from django import forms

class UploadForm(forms.Form):
    bank_name = forms.ChoiceField(choices=[('hdfc', 'HDFC'), ('icici', 'ICICI')])  # Add more banks as needed
    year = forms.CharField(max_length=4)
    month = forms.CharField(max_length=2)
    booking_or_refund = forms.ChoiceField(choices=[('booking', 'Booking'), ('refund', 'Refund')])
