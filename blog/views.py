from django.shortcuts import render
from .models import Blog
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import os
import os.path
from django.http import HttpResponse
from PIL import Image
from django.urls import reverse


# Create your views here.


def email_seen(request, key):
    META = {
        header: value
        for header, value in request.META.items()
        if header.startswith(("HTTP_", "REMOTE_"))
    }
    Blog.objects.filter(key=key, seen_at=None).update(
        request=json.dumps(META), seen_at=now()
    )
    print("Successfully Tracketd")
    with open(os.path.dirname(os.path.abspath(__file__)) + "/res/1x1.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


def preview_email(request, pk):
    et = get_object_or_404(Blog, pk=pk)
    context = {"et": et}
    return render(request, "blog_email_template.html", context)


def test_email(request, pk):
    et = get_object_or_404(Blog, pk=pk)
    ctx = {"et": et}
    tpl = "blog_email_template.html"
    html_message = render_to_string(tpl, ctx)
    if request.user.email:
        try:
            send_mail(
                subject=et.title,
                message="",
                html_message=html_message,
                from_email="SimpleIsBest <contact@vivadrive.io>",
                recipient_list=[request.user.email],
            )
            print("Email Sent to: ", request.user.email)
        except Exception as e:
            pass
    return redirect("/admin/blog/blog/{}/change/".format(pk))
