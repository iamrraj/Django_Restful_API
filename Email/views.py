from django.shortcuts import render

# Create your views here.


def subscription_confirmation(request):
    if "POST" == request.method:
        raise Http404

    token = request.GET.get("token", None)

    if not token:
        logging.getLogger("warning").warning("Invalid Link ")
        messages.error(request, "Invalid Link")
        return HttpResponseRedirect(reverse('appname:subscribe'))

    token = decrypt(token)
    if token:
        token = token.split(constants.SEPARATOR)
        email = token[0]
        print(email)
        initiate_time = token[1]  # time when email was sent , in epoch format. can be used for later calculations
        try:
            subscribe_model_instance = SubscribeModel.objects.get(email=email)
            subscribe_model_instance.status = constants.SUBSCRIBE_STATUS_CONFIRMED
            subscribe_model_instance.updated_date = utility.now()
            subscribe_model_instance.save()
            messages.success(request, "Subscription Confirmed. Thank you.")
        except ObjectDoesNotExist as e:
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logging.getLogger("warning").warning("Invalid token ")
        messages.error(request, "Invalid Link")

    return HttpResponseRedirect(reverse('appname:subscribe'))