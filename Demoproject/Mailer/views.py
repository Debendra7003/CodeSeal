import openpyxl
from django.core.mail import EmailMultiAlternatives,BadHeaderError
from django.shortcuts import render, redirect
from .forms import EmailUploadForm
from .models import EmailUpload
from django.views.decorators.csrf import csrf_protect
import time
import smtplib

@csrf_protect
def email_upload_view(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('send_emails')
    else:
        form = EmailUploadForm()
    return render(request, 'mailer/bulk_sender.html', {'form': form})

def send_emails(request):
    upload = EmailUpload.objects.last()
    email_file = upload.email_file.path
    template_file = upload.template_file.path
# Read emails from Excel file
    wb = openpyxl.load_workbook(email_file)
    sheet = wb.active
    emails = [row[0].value for row in sheet.iter_rows(min_row=1)]
# Read HTML template
    with open(template_file, 'r') as file:
        html_content = file.read()
# Send emails
    subject = 'Proposal: Streamlined Placements and Upskilling In Your College'
    from_email = 'Code Seals <recruitment@codeseals.in>'
    for email in emails:
        try:
            msg = EmailMultiAlternatives(subject, '', from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            time.sleep(2)
        except BadHeaderError:
            print("Invalid header found for email")
        except smtplib.SMTPDataError as e:
            print(f"SMTPDataError: {e}")
            break
        except Exception as e:
            print(f"Error sending email to: {e}")

    return render(request, 'mailer/result_page.html', {'emails': emails})
