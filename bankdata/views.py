# bankdata/views.py
from .models import BankData
from django.shortcuts import render, redirect
from .tasks import process_uploaded_files
from .forms import UploadForm  # If you have other form fields

def upload_files(request):
    if request.method == 'POST':
        # We can skip using a Django form to avoid the multiple files issue
        bank_name = request.POST.get('bank_name')
        year = request.POST.get('year')
        month = request.POST.get('month')
        booking_or_refund = request.POST.get('booking_or_refund')
        
        # Retrieve the uploaded files
        files = request.FILES.getlist('files')  # Use getlist to get multiple files
        
        # Process each uploaded file
        for f in files:
            file_content = f.read()  # Read file content
            file_name = f.name
            process_uploaded_files.delay(file_content, file_name, bank_name, year, month, booking_or_refund)

        return redirect('success')  # Redirect to success page

    return render(request, 'upload.html')

def display_data(request):
    bank_name = request.GET.get('bank_name')
    year = request.GET.get('year')
    month = request.GET.get('month')
    booking_or_refund = request.GET.get('booking_or_refund')
    date = request.GET.get('date')

    # Filter the data based on user selection
    data = BankData.objects.filter(
        bank_name=bank_name, 
        year=year, 
        month=month, 
        booking_or_refund=booking_or_refund, 
        date=date
    )
    return render(request, 'display_data.html', {'data': data})

def upload_success(request):
    return render(request, 'upload_success.html')
