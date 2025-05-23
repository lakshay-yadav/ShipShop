import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY
def payment_session_create(request,amount,purpose,email="",order_id=""):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': amount*100,
                        'product_data': {
                            'name': 'Donation'
                        },
                    },
                    'quantity': 1,
                },
            ],
            customer_email = email,
            mode='payment',
            success_url='http://localhost:8000/payment/success?session_id={CHECKOUT_SESSION_ID}' + f'&purpose={purpose}' + f'&order_id={order_id}',
            cancel_url=f'http://localhost:8000/payment/failed?purpose={purpose}' + f'&order_id={order_id}',
        )

        return checkout_session
    
    except Exception as e:
        print(e)
