from django import template

register = template.Library()

@register.filter
def to_ascii(value):
    turkish_to_ascii = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')
    return value.translate(turkish_to_ascii)
