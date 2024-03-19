from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from basket.basket import Basket
from orders.views import payment_confirmation
import stripe
import json


@login_required
def basket_view(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = int(total.replace(".", ''))
    stripe.api_key = 'sk_test_51OviijSGt255RwNS7NzN0rV4iqHxxBqI7leB0rHo7CZ3xPLWrnla78Xmvu1794fNUQms0A0jtwcZQMwlZejLgyA100sQTqDgnQ'
    intent = stripe.PaymentIntent.create(
        description="Software development services",
        shipping={
            "name": "Jenny Rosen",
        },
        amount=total,
        currency="usd",
        payment_method_types=["card"],
        metadata={
            "user_id": request.user.id,
        }
    )
    return render(request, 'payment/home.html', context={'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def orders_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')
