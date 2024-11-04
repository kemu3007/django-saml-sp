import xml.etree.ElementTree as ET
from .models import SAMLAuthNRequestConfiguration
import uuid
from django.utils import timezone

from django.conf import settings


def get_config(tag_name: str):
    if config := SAMLAuthNRequestConfiguration.objects.filter(tag_name=tag_name).last():
        return config.values
    return {}


def get_authentication_request(samlIdp: SAMLAuthNRequestConfiguration):
    root = ET.Element(r"{urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequest", {
        "ID": str(uuid.uuid4()), 
        "Destination": samlIdp.post_assertion_url,
        "AssertionConsumerServiceURL": "http://localhost:8080/saml/consume/",
        "Version": "2.0",
        "IssueInstant": timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    root.attrib.update(get_config("AuthnRequest"))
    issuer_el = ET.SubElement(root, r"{urn:oasis:names:tc:SAML:2.0:protocol}Issuer", {
        "Format": "urn:oasis:names:tc:SAML:2.0:nameid-format:entity"
    })
    issuer_el.text = settings.ISSUER_NAME
    issuer_el.attrib.update(get_config("Issuer"))
    name_id_policy = ET.SubElement(root, r"{urn:oasis:names:tc:SAML:2.0:protocol}NameIDPolicy")
    name_id_policy.attrib.update(get_config("NameIDPolicy"))

    return ET.tostring(root)
