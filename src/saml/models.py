from django.db import models
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from app.validators import validate_xml


class SAMLIdPConfiguration(models.Model):
    class Meta:
        verbose_name = "SAML IdP Configuration"
        verbose_name_plural = "SAML IdP Configuration"

    name = models.CharField("IdP 名", max_length=256)
    metadata = models.TextField("SAML メタデータ", validators=[validate_xml])

    def __str__(self) -> str:
        return self.name

    @property
    def get_assertion_url(self) -> str | None:
        tree = ET.fromstring(self.metadata)
        for element in tree.findall(r"{urn:oasis:names:tc:SAML:2.0:metadata}IDPSSODescriptor/{urn:oasis:names:tc:SAML:2.0:metadata}SingleSignOnService"):
            if element.attrib["Binding"] == "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-GET":
                return element.attrib["Location"]
        return None

    @property
    def post_assertion_url(self) -> str | None:
        tree = ET.fromstring(self.metadata)
        for element in tree.findall(r"{urn:oasis:names:tc:SAML:2.0:metadata}IDPSSODescriptor/{urn:oasis:names:tc:SAML:2.0:metadata}SingleSignOnService"):
            if element.attrib["Binding"] == "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST":
                return element.attrib["Location"]
        return None

    def get_metadata(self):
        return minidom.parseString(self.metadata).toprettyxml()

    def get_sample_request(self) -> str:
        from .utils import get_authentication_request
        return minidom.parseString(get_authentication_request(self).decode()).toprettyxml(indent="    ")



class SAMLAuthNRequestConfiguration(models.Model):
    class Meta:
        verbose_name = "SAML AuthN Request Configuration"
        verbose_name_plural = "SAML AuthN Request Configuration"

    TagNameChoices = [
        ("AuthnRequest", "AuthnRequest"),
        ("Issuer", "Issuer"),
        ("NameIDPolicy", "NameIDPolicy"),
    ]

    identity_provider = models.ForeignKey(SAMLIdPConfiguration, on_delete=models.CASCADE)

    tag_name = models.CharField(
        "タグ名",
        choices=TagNameChoices,
        max_length=256,
    )
    values = models.JSONField(blank=True, default=dict)

    def __str__(self) -> str:
        return self.tag_name
