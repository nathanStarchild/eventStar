from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.utils.crypto import get_random_string
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .forms import *

import random

from io import StringIO
import csv

# Create your views here.

def imgUrl():
    images = [
        {"id": "2517db2c-bd5d-4715-95bc-795474b312fb",
         "idx": [0]
        },
        {"id": "f22f4fbf-64bb-4c66-86e2-5965df059e85",
         "idx": [0, 1, 2, 3]
        },
        {"id": "b874f30a-b1ab-4454-b54e-7ac4eef895f3",
         "idx": [0, 1, 2, 3]
        },
        {"id": "79d86b73-0cfd-4777-8527-9004b45be2f7",
         "idx": [0]
        },
        {"id": "5de3dce0-d03a-449f-9322-503c99052cbe",
         "idx": [0, 1, 2, 3]
        },
        {"id": "c67cb6e6-ca26-488c-8aec-cf70fd469ea9",
         "idx": [0, 1, 2, 3]
        },
    ]
    image = random.choice(images)
    imageUrl = f"https://cdn.midjourney.com/{image['id']}/0_{random.choice(image['idx'])}.jpeg"
    return imageUrl


def index(request):
    context = {"message": "", "imageUrl": imgUrl()}
    return render(request, 'events/index.html', context)

def info(request):
    context = {
        "message": "",
        "imageUrl": imgUrl(),
        }
    return render(request, 'events/info.html', context)

def tickets(request):
    humanForm = HumanForm()
    context = {
        "message": "", 
        "imageUrl": imgUrl(),
        "humanForm": humanForm,
    }
    return render(request, 'events/tickets.html', context)

def ajaxAddHuman(request):
    try:
        assert request.method == "POST", "POST requests only"
        msg = ""
        ok = False
        form = HumanForm(request.POST)
        print(request.POST)
        errors = None
        human = None
        if form.is_valid():
            human = form.save()
            nights = request.POST['nights']
            ok = True
            msg = "human saved"
            human = model_to_dict(human)
            human['nights'] = nights
        else:
            errors = form.errors.as_json()
        return JsonResponse({
            'ok': ok,
            'msg': msg,
            'errors': errors,
            "human": human,
        })

    except Exception as e:
        print(str(e))
        print(e)
        return JsonResponse({"ok":False, "msg":str(e)})
    
@login_required
def ajaxDeleteHuman(request, humanId):
    try:
        msg = ""
        ok = False
        human = Human.objects.get(pk=humanId)
        human.delete()
        ok = True
        msg = "human delted"
        return JsonResponse({
            'ok': ok,
            'msg': msg,
        })

    except Exception as e:
        print(str(e))
        print(e)
        return JsonResponse({"ok":False, "msg":str(e)})
    
def ajaxCreatePayment(request):
    try:
        assert request.method == "POST", "POST requests only"
        msg = ""
        ok = False
        errors = None
        contact = Human.objects.get(pk=request.POST['contact'])
        token = get_random_string(6)
        print(Decimal(request.POST['amount']))
        try:
            payment = Payment.objects.create(
                token = token,
                contact = contact,
                amount = Decimal(request.POST['amount'])
            )
        except IntegrityError:
            #duplicate token
            token = get_random_string(6)
            payment = Payment.objects.create(
                token = token,
                contact = contact,
                amount = Decimal(request.POST['amount'])
            )

        ok = True

        return JsonResponse({
            'ok': ok,
            'msg': msg,
            'errors': errors,
            "paymentId": payment.id,
            "token": payment.token,
        })

    except Exception as e:
        print(str(e))
        print(e)
        raise
        return JsonResponse({"ok":False, "msg":str(e)})
    
def ajaxCreateTicket(request):
    try:
        assert request.method == "POST", "POST requests only"
        msg = ""
        ok = False
        errors = None
        human = Human.objects.get(pk=request.POST['human'])
        payment = Payment.objects.get(pk=request.POST['payment'])
        event = Event.objects.get(name="Starfest")
        ticket = Ticket.objects.create(
            human = human,
            event = event,
            payment = payment,
            ticketType = request.POST['ticketType'],
            nights = request.POST['nights']
        )
        print(ticket.price())
        payment.amount += ticket.price()
        payment.save()

        ok = True

        return JsonResponse({
            'ok': ok,
            'msg': msg,
            'errors': errors,
            "ticket": model_to_dict(ticket),
        })

    except Exception as e:
        print(str(e))
        print(e)
        return JsonResponse({"ok":False, "msg":str(e)})
    
def ajaxPaymentAmount(request, paymentId):
    try:
        msg = ""
        ok = False
        errors = None
        payment = Payment.objects.get(pk=paymentId)

        ok = True

        return JsonResponse({
            'ok': ok,
            'msg': msg,
            'errors': errors,
            "amount": payment.amount,
        })

    except Exception as e:
        print(str(e))
        print(e)
        return JsonResponse({"ok":False, "msg":str(e)})

@login_required
def eventAdmin(request):
    humans = Human.objects.order_by("name")
    tickets = Ticket.objects.order_by("human__name")
    context = {
        "message": "",
        "imageUrl": imgUrl(),
        "humans": humans,
        "tickets": tickets,
        }
    return render(request, 'events/admin.html', context)


@login_required
def ticketList(request):
    humans = Human.objects.order_by("name")
    #create a file-like buffer to store the file
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["", "Name", "Nights"])
    for n, h in enumerate(humans):
        try:
            nights = h.ticket.nights
        except Ticket.DoesNotExist:
            nights = ""
        writer.writerow([n+1, h.name, nights])
    for n in range(humans.count() + 1, 101):
        writer.writerow([n])
    filename = f"starfest tickets.csv"
    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    buffer.close()
    return response