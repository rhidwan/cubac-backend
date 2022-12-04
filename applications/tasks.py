import io
import time
import logging
logger = logging.getLogger(__name__)

from weasyprint import HTML
from django.core.files import File
from .models import Application, PageRequest
from django.template.loader import get_template
import uuid
from background_task import background

@background(schedule=None, name="render_pdf",  remove_existing_tasks=True)
def render_pdf(page_id):
    page = PageRequest.objects.get(id=uuid.UUID(page_id))
    logger.info("Waiting 100 second")
    if page.status != page.Status.PENDING:
        return
    page.status = PageRequest.Status.GENERATING
    page.save()

    try:
        if page.context == "admit_card_all":
            applications = Application.objects.filter(call_for_application=page.season).prefetch_related( 'transaction', 'call_for_application', 'seat' )
            context = {
                    "applications": [x for x in applications if x.seat],
            }
            filename = "admit_card_%s" %(applications[0].call_for_application.title)
       
        elif page.context ==  "application_form_all":
            applications = Application.objects.filter(call_for_application=page.season).prefetch_related( 'transaction', 'call_for_application', 'seat' )
            context = {
                "applications": [x for x in applications if x.seat],
            }
            filename = "application_form_%s" %(applications[0].call_for_application.title)

        template = get_template(page.template_src)

        html  = template.render(context)
        pdf_file = HTML(string=html, base_url=page.base_url)
       

    except Exception as e:
        logger.warning("Failed to generate pdf for instance %s %s", page.pk, e)
        
        page.status = PageRequest.Status.ERROR
        page.error_msg = str(e)
        page.save()
        return
    
    try:
        pdf_in_memory = io.BytesIO()
        pdf_file.write_pdf(target=pdf_in_memory)
    except Exception as e:
        logger.warning("Failed to generate pdf for instance %s %s", page.pk, e)
        page.status = PageRequest.Status.ERROR
        page.error_msg = str(e)
        page.save()
        return
    
    logger.info("Success generate pdf for instance %s ", page.pk)
    
    page.pdf_file = File(pdf_in_memory, f"{filename}.pdf")
    page.status = PageRequest.Status.READY
    page.save()

    return