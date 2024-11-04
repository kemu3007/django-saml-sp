from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from .utils import get_authentication_request
import base64
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode, parse_qs
from .models import SAMLIdPConfiguration, SAMLAuthNRequestConfiguration
import zlib


def index(request):
    idp = SAMLIdPConfiguration.objects.filter(name=request.GET.get("identity_provider")).first()
    return render(request, "index.html", context={ "selected": idp, "idp_list": SAMLIdPConfiguration.objects.all(), "config_list": SAMLAuthNRequestConfiguration.objects.all() })


def login(request):
    saml_idp = get_object_or_404(SAMLIdPConfiguration, name=request.GET.get("identity_provider"))
    authNRequest = base64.b64encode(zlib.compress(get_authentication_request(saml_idp), wbits=-zlib.MAX_WBITS))
    return redirect(f"{saml_idp.post_assertion_url}?{urlencode({'SAMLRequest': authNRequest.decode() })}")


@csrf_exempt
def saml_acs_view(request):
    data = parse_qs(request.body.decode())
    return HttpResponse(base64.b64decode(data['SAMLResponse'][0]), content_type="application/xml")
