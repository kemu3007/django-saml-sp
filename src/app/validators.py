import xml.etree.ElementTree as ET
from django.core.exceptions import ValidationError

def validate_xml(raw_value):
    try:
        _ = ET.fromstring(raw_value)
    except Exception as e:
        raise ValidationError(e)
