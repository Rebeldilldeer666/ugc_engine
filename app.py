import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import stripe

load_dotenv()
app = Flask(__name__)
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY","").strip()
stripe.api_key = STRIPE_KEY

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebel AI - UGC Invoice Generator</title>
<style>
body{background:#000;color:#fff;font-family:Arial;padding:20px}
input{width:100%;padding:15px;margin:10px 0;border-radius:8px;border:none;font-size:18px}
button{width:100%;padding:18px;background:#635bff;color:#fff;border:none;border-radius:8px;font-size:20px;font-weight:bold}
#result{margin-top:20px;padding:15px;background:#111;border-radius:8px;word-break:break-all;display:none}
a{color:#635bff}
</style>
</head>
<body>
<h1>Rebel AI Systems</h1>
<h3>UGC Growth Invoice Link</h3>
<input id="business" placeholder="Business Name (e.g. Apex Fitness)">
<input id="amount" type="number" placeholder="Amount in cents (120000 = $1200)" value="120000">
<button onclick="gen()">Generate Checkout Link</button>
<div id="result"></div>
<script>
async function gen(){
 let b=document.getElementById('business').value||'Client';
 let a=document.getElementById('amount').value||'120000';
 let res=document.getElementById('result');
 res.style.display='block';
 res.innerHTML='Generating...';
 try{
   let r=await fetch('/api/create-invoice-link',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({business:b,amount:parseInt(a)})});
   let d=await r.json();
   if(d.success){res.innerHTML=`<b>✅ Link Ready:</b><br><br><a href='${d.checkout_url}' target='_blank'>${d.checkout_url}</a><br><br><button onclick="navigator.clipboard.writeText('${d.checkout_url}')">Copy Link</button>`}
   else{res.innerHTML='Error: '+d.error}
 }catch(e){res.innerHTML='Error: '+e}
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/api/create-invoice-link", methods=["POST"])
def create_link():
    try:
        data=request.get_json()
        business=data.get("business","Client")
        amount=int(data.get("amount",120000))
        session=stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data':{'currency':'usd','product_data':{'name':f'UGC Growth Package - {business}'},'unit_amount':amount},'quantity':1}],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return jsonify({"success":True,"checkout_url":session.url})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),400

@app.route("/webhook", methods=["POST"])
def webhook():
    return jsonify({"received":True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

