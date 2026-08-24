import re, os
print("\n=== STRIPE FIX ===")
k = input("Paste your FULL sk_live_ or sk_test_ key (tap Reveal first, long press copy):\n> ").strip()
if "..." in k or "****" in k or len(k) < 80:
    print("\n❌ THAT KEY IS STILL HIDDEN/TRUNCATED.")
    print("You pasted the short ...6Mqr version.")
    print("Go to Stripe -> tap directly on sk_live_...6Mqr -> Reveal live key -> Copy the LONG one.")
    exit()
if not k.startswith("sk_"):
    print(f"\n❌ Wrong key. You pasted pk_... publishable. Need sk_... secret. Got: {k[:10]}")
    exit()
# Write clean .env
with open(".env","w") as f:
    f.write(f"STRIPE_SECRET_KEY={k}\n")
    f.write("STRIPE_WEBHOOK_SECRET=whsec_dummy_for_now\n")
print(f"\n✅ Saved. Key length {len(k)} starts {k[:20]}... ends {k[-4:]}")
# restart
os.system("pkill -9 -f python; nohup python app.py > server.log 2>&1 &")
print("✅ Server restarted")
