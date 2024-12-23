import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(amount):
    return stripe.Price.create(
      currency="usd",
      unit_amount=amount * 100,
      product_data={"name": "Курс"},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
      success_url="http://127.0.0.1/",
      line_items=[{"price": price.get("id"), "quantity": 1}],
      mode="payment",
    )
    return session.get("id"), session.get("url")