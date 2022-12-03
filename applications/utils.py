from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
# from xhtml2pdf import pisa
from weasyprint import HTML, CSS
import zipfile
from applications.models import Application
# from PyPDF2 import PdfFileMerger

def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.PDF_STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    print("I am here")
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
        print(path)
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path


def render_to_pdf(request, template_src, context_dict={} ):
    template = get_template(template_src)

    html  = template.render(context_dict)

    base_url = os.path.dirname(os.path.realpath(__file__))
    pdf_file = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

    # result = BytesIO()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

def render_pdf(request, template_src, context_dict={} ):
    template = get_template(template_src)

    html  = template.render(context_dict)

    base_url = os.path.dirname(os.path.realpath(__file__))
    pdf_file = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

    return pdf_file
    
def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()


def generate_roll_no(call_application, latest_roll = None):
    '''
    Helper function to generate roll number
    input: 
        -  Call Application Object
    output :
        - Generated Roll Number 
    '''
    if latest_roll:
        last_roll = latest_roll

    else:
        latest_application = Application.objects.filter(call_for_application=call_application).order_by('roll_no').latest('roll_no')
        if latest_application:
            last_roll = latest_application.roll_no
        else:
            last_roll = '0'
    
    # print("last entry : ", last_entry)
    short_code = call_application.shortcode 
    
    chunk_size = int(call_application.chunk)
    skip_to = int(call_application.skip_to)

    last_entry = int(last_roll.replace(short_code, ""))
    if last_entry % chunk_size == 0 :
        print("chunk size got, skipping to next")
        print("last_entry, skipto, divide", last_entry, skip_to, last_entry//skip_to)
        if last_entry == 0:
            new_roll = 1
        else:
            new_roll = ((last_entry // skip_to) + 1) * skip_to + 1
        # else:
            # new_roll = 1
    else:
        new_roll = last_entry + 1

    roll_number = short_code + str(new_roll).zfill(3)
    print(roll_number)
    return roll_number  
# def merge_pdf(files):
#     mem_pdf = BytesIO()
#     merger = PdfFileMerger()
#     pdf_files = [x for x in files if x.endswith(".pdf")]
#     [merger.append(pdf) for pdf in pdf_files]
    
#     merger.write(mem_pdf)
    
#     return mem_pdf.getvalue()