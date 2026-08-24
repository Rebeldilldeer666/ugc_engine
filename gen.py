import os, sys
from dotenv import load_dotenv
import stripe
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY","").strip().strip('"').strip("'")
biz = sys.argv[1] if len(sys.argv) > 1 else "Rebel AI Client"
amount = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
session = stripe.checkout.Session.create(
  payment_method_types=['card'],
  line_items=[{'price_data':{'currency':'usd','product_data':{'name':f'{biz} - AI Quick Cash Kit'},'unit_amount':amount},'quantity':1}],
  mode='payment',
  success_url='https://example.com/success',
  cancel_url='https://example.com/cancel',
)
print(f"SEND THIS LINK: {session.url}")
