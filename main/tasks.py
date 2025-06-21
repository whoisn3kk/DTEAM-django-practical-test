import io
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import get_template
import pdfkit
from .models import CV

@shared_task
def send_email(cv_pk:int, recipient_email:str):
    cv = CV.objects.get(pk=cv_pk)
    template = get_template('main/cv_pdf_template.html')
    html = template.render({'cv': cv})


    buffer = io.BytesIO(pdfkit.from_string(html)) # type: ignore
    buffer.seek(0)

    try:
        email = EmailMessage(
            f'Your CV for {cv.firstname} {cv.lastname}',
            'Please find your generated CV attached.',
            'from@example.com',
            [recipient_email],
        )
        email.attach(f'CV_{cv.pk}.pdf', buffer.getvalue(), 'application/pdf')
        email.send()
        return f"Email sent to {recipient_email}"
    except Exception as e:
        print(e)
    
    return "Error generating PDF"