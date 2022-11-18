from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from xhtml2pdf import pisa
from weasyprint import HTML, CSS
import zipfile

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