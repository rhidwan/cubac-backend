import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()

@register.simple_tag
def encode_static(path, encodign='base64', file_type='image'):
  try:
    file_path = find_static_file(path)
    ext = file_path.split('.')[-1]
    file_str = _get_file_data(file_path).decode('utf-8')
    return "data:{0}/{1};{2}, {3}".format(file_type, ext, encodign, file_str)
  except IOError:
    return ''

def _get_file_data(file_path):
  with open(file_path, 'rb') as f:
    data = base64.b64encode(f.read())
    f.close()
    return data

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.simple_tag
def concat_all(*args):
    """concatenate all args"""
    return ''.join(map(str, args))
  

@register.simple_tag
def get_object_count(*args):
    objects = args[0]
    attribute = args[1]
    value = args[2]
    try:
        if value:
            if value == "True": value = True
            elif value == "False" : value = False
            
            return len([x for x in objects if  getattr(x, attribute)  == value])
        else:
            return len([x for x in objects if getattr(x, attribute)])
    except Exception as e:
        print(e)
        return 0