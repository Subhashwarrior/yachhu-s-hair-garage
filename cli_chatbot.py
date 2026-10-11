import needle
import random

# ============================================================
# YOUR BUSINESS FAQ DATA - REPLACE WITH YOUR ACTUAL DATA
# ============================================================
# Sourced from Yacchu's Hair Garage service menu (PDF extracted)
BUSINESS_FAQ = {
    "returns": "We accept returns within 30 days of delivery. Items must be in original packaging with tags. Refunds process in 5-7 business days to original payment method.",
    "exchanges": "Exchanges are free within 30 days. Just return the original item and we'll ship the replacement at no extra cost.",
    "shipping": "Standard shipping: 3-5 business days ($5.99). Express: 1-2 days ($12.99). Free standard on orders over $50. International: 7-14 days, rates vary.",
    "warranty": "All products come with a 1-year manufacturer warranty. Covers defects in materials and workmanship. Extended warranties available at checkout.",
    "hours": "Customer support: Mon-Fri 8AM-8PM EST, Sat 9AM-5PM. Closed Sundays. Online orders 24/7.",
    "pricing": "We offer competitive pricing with price matching on identical items. Bulk discounts: 10% off $100+, 15% off $250+, 20% off $500+. Student discount: 15% with valid .edu email.",
    "contact": "Email: support@yourbusiness.com | Phone: 1-800-555-0123 | Live chat on website. Average response: <2 hours business hours.",
    "privacy": "We never sell your data. SSL encryption on all transactions. GDPR/CCPA compliant. You can request data deletion anytime.",
    "payment": "Accepted: Visa, Mastercard, Amex, Discover, PayPal, Apple Pay, Google Pay, Shop Pay. Buy now pay later with Klarna/Affirm.",
    "tracking": "Tracking emails sent within 1 hour of shipment. Check order status in your account. Text alerts available at checkout.",
    "cancellation": "Cancel within 1 hour of order for full refund. After 1 hour, contact support - we'll try to stop before it ships.",
    "damaged": "Damaged items: send photo within 48 hours, we'll replace immediately at no cost. No return needed for items under $50.",
    "international": "We ship to 50+ countries. Duties/taxes may apply - calculated at checkout. Delivery: 7-21 business days.",
    "gift_cards": "Digital gift cards delivered instantly via email. Physical cards available. No expiration, no fees. Can combine with promos.",
    "loyalty": "Join our rewards program free. Earn 1 point per $1 spent. 100 points = $5 off. Birthday bonus: double points all month.",
    "wholesale": "Wholesale pricing for verified businesses. Minimum order $250. Net-30 terms available after 3 orders. Contact sales@yourbusiness.com.",

    # Yacchu's Hair Garage specific services
    "basic_cut": "Basic Cut: 500/-",
    "layer_cuts": "Layer Cuts: 800/-",
    "fringes_bangs": "Fringes / Bangs: 200/-",
    "kids_cut_no_wash": "Kids cut (without hair wash): 300/-",
    "kids_cut_with_wash": "Kids cut (with hair wash): 500/-",
    # Hair coloring (for all color/highlight queries)
    "hair_coloring": "Coloring: Root Touch up Ammonia 1000/-, Root Touch up Non-Ammonia 1800-2000/-, Root Touch up Crown 1200/-, Global Ammonia free 3500-4000/-, Global Fashion 4000-4500/-, Global with Highlights 7000/-, Highlights 5000-6500/-, Highlights per streak 350/-.",
    "scalp_treatment": "Scalp/Hair Issues: Dandruff Control 1000/-, Hairfall Treatment 800/-, Head Massage 800/-.",

    "hair_treatment": "Smoothening: Starts From 3500/-. Nanoplastia: Starts From 4000/-. Botox Treatment: Starts From 5000/-. (*T & C Applied*).",
    "wash_blowdry_medium": "Hair wash and Blowdry (Medium / long): 500/-",
    "wash_blowdry_long": "Hair wash and Blowdry (Medium / long): 600/-",
    "bouncy_wave_blowdry_medium": "Bouncy Wave Blowdry (Medium / long): 700/-",
    "bouncy_wave_blowdry_long": "Bouncy Wave Blowdry (Medium / long): 900/-",
    "ironing_medium": "Ironing (Medium / long): 1000/-",
    "ironing_long": "Ironing (Medium / long): 1500/-",
    "tongs_medium": "Tongs (medium / long): 1200/-",
    "tongs_long": "Tongs (medium / long): 1500/-",
    "dandruff_treatment": "Dandruff Control Treatment: 1000/-",
    "hairfall_treatment": "Hairfall Treatment: 800/-",
    "head_massage": "Head Massage: 800/-",
    "hair_spa": "Hair Spa: Starts From 1500/-",
    "advance_hair_spa": "Advance Hair Spa: Starts From 2500/-",
    "korean_hair_spa": "Korean Hair Spa: Starts From 3000/-",
    "root_touch_up_ammonia": "Root Touch up Ammonia: 1000/-",
    "root_touch_up_non_ammonia": "Root Touch up Non-Ammonia: 1800/- / 2000/-",
    "root_touch_up_crown": "Root Touch up Crown Area: 1200/-",
    "global_ammonia_free": "Global Ammonia free: 3500/- / 4000/-",
    "global_fashion_color": "Global Fashion color: 4000/- / 4500/-",
    "global_highlights": "Global with Highlights: 7000/-",
    "highlights": "Highlights: 5000/- / 6500/-",
    "highlights_per_streak": "Highlights per streak: 350/-",
    "basic_cleanup": "Basic Cleanup: 700/-",
    "advance_cleanup": "Advance Cleanup: 1000/-",
    "whitening_cleanup": "Whitening Cleanup: 1500/-",
    "organic_facial": "Organic Facial (All Skin Types): 1800/- / 2200/-",
    "fruit_facial": "Fruit Facials: 2300/- / 3000/-",
    "gold_radiance_facial": "Gold Radiance Facial: 3000/- / 3500/-",
    "brightening_facials": "Brightening Facials: 3500/- / 4000/-",
    "whitening_facials": "Whitening Facials: 3500/- / 4000/-",
    "luxury_facial": "Luxury Facial (specially for bride): —",
    "korean_facial": "Korean Facial: 5500/-",
    "gold_facial": "Gold Facial: 6000/-",
    "hydra_facial": "Hydra Facial: 3000/-",
    "korean_glass_skin_facial": "Korean Glass Skin Facial: 3500/-",
    "rejuvenating_mask": "Rejuvenating: 800/-",
    "brightening_mask": "Brightening: 1000/-",
    "eyebrow_threading": "Eyebrows: 50/-",
    "upper_lip_threading": "Upper Lips: 50/-",
    "lower_lip_threading": "Lower Lips: 50/-",
    "side_locks_threading": "Side locks: 100/-",
    "full_face_threading": "Full Face Threading: 300/-",
    "facial_hair_removal": "Facial Hair Removal (Razor Method): 500/-",
    "face_neck_bleach": "Face & neck Detan / Bleach: 600/-",
    "full_hand_bleach": "Full Hand Bleach / Detan: 600/-",
    "full_leg_bleach": "Full Leg Bleach / Detan: 1000/-",
    "full_back_bleach": "Full Back Bleach / Detan: 800/- / 1000/-",
    "upper_lips_wax": "Upper Lips: 100/-",
    "side_locks_wax": "Side locks: 200/-",
    "lower_lips_wax": "Lower Lips: 100/-",
    "ear_wax": "Ear Wax: 200/-",
    "nose_wax": "Nose Wax: 200/-",
    "face_wax": "Face Wax: 400/-",
    "under_arm_wax": "Under arm wax: 300/-",
    "bikini_line_wax": "Bikini line: 2000/-",
    "full_bikini_wax": "Full bikini: 3000/- / 3500/-",
    "full_hands_wax": "Full hands wax: 600/-",
    "full_leg_wax": "Full leg wax: 800/-",
    "half_hands_wax": "Half hands wax: 400/-",
    "half_leg_wax": "Half leg wax: 500/-",
    "full_back_wax": "Full back wax: 1000/-",
    "stomach_wax": "Stomach: 800/-",
    "underarm_wax": "Underarm: 200/-",
    "blouse_line_wax": "Blouse line wax: 600/-",
    "bikini_line_wax_v2": "Bikini line wax: 1500/-",
    "full_bikini_wax_v2": "Full Bikini wax: 2500/-",
    "body_scrub": "Body Scrub: 2000/- / 2500/-",
    "body_polishing": "Body Polishing: 3500/- / 4000/-",
    "advance_manicure": "Advance Manicure: 600/-",
    "premium_manicure": "Premium Manicure: 800/-",
    "cut_and_file_manicure": "Cut and File: 200/-",
    "change_polish": "Change of Polish: 100/-",
    "pedicure": "Pedicure: 700/-",
    "advance_pedicure": "Advance Pedicure: 1200/-",
    "premium_pedicure": "Premium Pedicure: 1200/- / 1800/-",
    "heel_peel_treatment": "Heel Peel Treatment: 200/-",
    "cut_and_file_pedicure": "Cut and File: 200/-",
    "change_polish_pedicure": "Change of Polish: 100/-",
}

# ============================================================
# GREETING DETECTION & RESPONSES
# ============================================================
GREETING_KEYWORDS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy", "greetings", "hiya", "yo", "sup"]
FAREWELL_KEYWORDS = ["bye", "goodbye", "see you", "farewell", "cya", "later", "quit", "exit"]

GREETING_RESPONSES = [
    "Hello! Welcome to Yacchu's Hair Garage. How can I help you today?",
    "Hi there! What can I help you find?",
    "Hey! Ask me anything about hair services, pricing, or appointments.",
    "Good to see you! What questions do you have?",
]

FAREWELL_RESPONSES = [
    "Thanks for chatting! Have a great day!",
    "Goodbye! Come back anytime you have questions.",
    "See you later! We're here if you need anything.",
]

def detect_greeting(query: str) -> str | None:
    """Check if query is a greeting or farewell."""
    q = query.lower().strip()
    if any(q.startswith(k) or q == k for k in GREETING_KEYWORDS):
        return "greeting"
    if any(q.startswith(k) or q == k for k in FAREWELL_KEYWORDS):
        return "farewell"
    return None

def get_greeting_response() -> str:
    return random.choice(GREETING_RESPONSES)

def get_farewell_response() -> str:
    return random.choice(FAREWELL_RESPONSES)


# ============================================================
# FAQ LOOKUP TOOL (uses your business data)
# ============================================================
@needle.tool
def faq_lookup(query: str):
    """Retrieve a business FAQ answer from the user's query text using keyword matching."""
    q = query.lower()

    # ============================
    # FULL SERVICES MENU (check BEFORE specific keyword blocks)
    # ============================
    if any(k in q for k in ["services", "what services", "your services", "full menu", "service menu", "menu"]):
        return {"query": query, "answer":
            "Hair: Cut 500/-, Layer 800/-, Fringes 200/-, Kids 300-500/-  |  Treatments: Smoothening 3500/-, Nanoplastia 4000/-, Botox 5000/-, Hair Spa 1500-3000/-  |  Coloring: Highlights 5000-6500/-  |  Facials: Organic 1800-2200/-, Korean 5500/-, Gold 6000/-  |  Threading: 50-300/-  |  Waxing: 100-3500/-  |  Manicure 600-800/-, Pedicure 700-1800/-. Full menu at salon.", "grounded": True}

    if any(k in q for k in ["return", "refund", "exchange", "send back", "item back", "return it", "money back"]):
        if "exchange" in q:
            return {"query": query, "answer": BUSINESS_FAQ["exchanges"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["returns"], "grounded": True}

    if any(k in q for k in ["ship", "delivery", "shipping", "track", "deliver", "arrive", "when will", "where is", "transit"]):
        if "track" in q or "where is" in q:
            return {"query": query, "answer": BUSINESS_FAQ["tracking"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["shipping"], "grounded": True}

    if any(k in q for k in ["warranty", "guarantee", "broken", "defect", "defective", "not working", "stopped working"]):
        return {"query": query, "answer": BUSINESS_FAQ["warranty"], "grounded": True}

    if any(k in q for k in ["hour", "open", "close", "time", "store open", "business hours", "when are you", "available"]):
        return {"query": query, "answer": BUSINESS_FAQ["hours"], "grounded": True}

    if any(k in q for k in ["price", "cost", "discount", "bulk", "pricing", "how much", "expensive", "cheap", "student", "offer"]):
        if "student" in q:
            return {"query": query, "answer": BUSINESS_FAQ["pricing"], "grounded": True}
        return {"query": query, "answer":
            "Our prices vary by service and hair length. A Basic Hair Cut is 500/-, Layer Cuts 800/-, Hair Treatments start from 3500/-, Hair Spa starts from 1500/-, Facials from 1800/-, Waxing from 100/-. Type 'services' for the full menu!", "grounded": True}

    if any(k in q for k in ["hair", "hair service"]):
        return {"query": query, "answer": "Basic Cut 500/-, Layer Cuts 800/-, Hair Treatments from 3500/-, Hair Spa from 1500/-, Hair Coloring 5000-7000/-.", "grounded": True}

    if any(k in q for k in ["contact", "email", "phone", "call", "support", "talk to", "speak", "reach"]):
        return {"query": query, "answer": BUSINESS_FAQ["contact"], "grounded": True}

    if any(k in q for k in ["privacy", "data", "gdpr", "ccpa", "secret", "information", "personal info", "sell data"]):
        return {"query": query, "answer": BUSINESS_FAQ["privacy"], "grounded": True}

    if any(k in q for k in ["payment", "pay", "card", "apple pay", "google pay", "paypal", "klarna", "affirm", "buy now pay later"]):
        return {"query": query, "answer": BUSINESS_FAQ["payment"], "grounded": True}

    if any(k in q for k in ["track", "tracking", "where is my", "order status", "shipped"]):
        return {"query": query, "answer": BUSINESS_FAQ["tracking"], "grounded": True}

    if any(k in q for k in ["cancel", "cancellation", "change my order", "stop order"]):
        return {"query": query, "answer": BUSINESS_FAQ["cancellation"], "grounded": True}

    if any(k in q for k in ["damaged", "broken", "cracked", "wrong item", "missing", "defective"]):
        return {"query": query, "answer": BUSINESS_FAQ["damaged"], "grounded": True}

    if any(k in q for k in ["international", "overseas", "outside us", "customs", "duties", "import"]):
        return {"query": query, "answer": BUSINESS_FAQ["international"], "grounded": True}

    if any(k in q for k in ["gift card", "gift certificate", "present"]):
        return {"query": query, "answer": BUSINESS_FAQ["gift_cards"], "grounded": True}

    if any(k in q for k in ["loyalty", "rewards", "points", "vip", "member", "loyalty program"]):
        return {"query": query, "answer": BUSINESS_FAQ["loyalty"], "grounded": True}

    if any(k in q for k in ["wholesale", "bulk order", "business account", "reseller", "distributor"]):
        return {"query": query, "answer": BUSINESS_FAQ["wholesale"], "grounded": True}

    if any(k in q for k in ["hair cut", "haircut", "cut", "trim"]):
        if "kids" in q:
            return {"query": query, "answer": BUSINESS_FAQ["kids_cut_with_wash"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["basic_cut"], "grounded": True}

    if any(k in q for k in ["layer cut"]):
        return {"query": query, "answer": BUSINESS_FAQ["layer_cuts"], "grounded": True}

    if any(k in q for k in ["fringe", "bang"]):
        return {"query": query, "answer": BUSINESS_FAQ["fringes_bangs"], "grounded": True}

    if any(k in q for k in ["kids cut"]):
        return {"query": query, "answer": BUSINESS_FAQ["kids_cut_with_wash"], "grounded": True}

    if any(k in q for k in ["hair treatment", "smoothening", "nanoplastia", "botox"]):
        return {"query": query, "answer": BUSINESS_FAQ["hair_treatment"], "grounded": True}

    if any(k in q for k in ["hair spa", "advance hair spa"]):
        if "korean" in q:
            return {"query": query, "answer": BUSINESS_FAQ["korean_hair_spa"], "grounded": True}
        if "advance" in q:
            return {"query": query, "answer": BUSINESS_FAQ["advance_hair_spa"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["hair_spa"], "grounded": True}

    if any(k in q for k in ["wash", "blowdry", "blow dry", "dry"]):
        if "bouncy" in q:
            if "long" in q:
                return {"query": query, "answer": BUSINESS_FAQ["bouncy_wave_blowdry_long"], "grounded": True}
            return {"query": query, "answer": BUSINESS_FAQ["bouncy_wave_blowdry_medium"], "grounded": True}
        if "long" in q:
            return {"query": query, "answer": BUSINESS_FAQ["wash_blowdry_long"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["wash_blowdry_medium"], "grounded": True}

    if any(k in q for k in ["styling", "ironing", "tongs"]):
        if "long" in q:
            if "tongs" in q:
                return {"query": query, "answer": BUSINESS_FAQ["tongs_long"], "grounded": True}
            return {"query": query, "answer": BUSINESS_FAQ["ironing_long"], "grounded": True}
        if "tongs" in q:
            return {"query": query, "answer": BUSINESS_FAQ["tongs_medium"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["ironing_medium"], "grounded": True}

    if any(k in q for k in ["scalp", "dandruff", "hairfall"]):
        if "dandruff" in q:
            return {"query": query, "answer": BUSINESS_FAQ["dandruff_treatment"], "grounded": True}
        if "hairfall" in q:
            return {"query": query, "answer": BUSINESS_FAQ["hairfall_treatment"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["dandruff_treatment"], "grounded": True}

    if any(k in q for k in ["hair spa", "advance hair spa"]):
        if "korean" in q:
            return {"query": query, "answer": BUSINESS_FAQ["korean_hair_spa"], "grounded": True}
        if "advance" in q:
            return {"query": query, "answer": BUSINESS_FAQ["advance_hair_spa"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["hair_spa"], "grounded": True}

    if any(k in q for k in ["color", "root touch up", "global", "highlight"]):
        return {"query": query, "answer": BUSINESS_FAQ["hair_coloring"], "grounded": True}

    if any(k in q for k in ["cleanup", "basic cleanup"]):
        return {"query": query, "answer": BUSINESS_FAQ["basic_cleanup"], "grounded": True}

    if any(k in q for k in ["advance cleanup"]):
        return {"query": query, "answer": BUSINESS_FAQ["advance_cleanup"], "grounded": True}

    if any(k in q for k in ["whitening cleanup"]):
        return {"query": query, "answer": BUSINESS_FAQ["whitening_cleanup"], "grounded": True}

    if any(k in q for k in ["facial", "facial treatment"]):
        return {"query": query, "answer": BUSINESS_FAQ["organic_facial"], "grounded": True}

    if any(k in q for k in ["fruit facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["fruit_facial"], "grounded": True}

    if any(k in q for k in ["gold radiance"]):
        return {"query": query, "answer": BUSINESS_FAQ["gold_radiance_facial"], "grounded": True}

    if any(k in q for k in ["brightening facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["brightening_facials"], "grounded": True}

    if any(k in q for k in ["whitening facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["whitening_facials"], "grounded": True}

    if any(k in q for k in ["luxury facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["luxury_facial"], "grounded": True}

    if any(k in q for k in ["korean facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["korean_facial"], "grounded": True}

    if any(k in q for k in ["gold facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["gold_facial"], "grounded": True}

    if any(k in q for k in ["hydra facial"]):
        return {"query": query, "answer": BUSINESS_FAQ["hydra_facial"], "grounded": True}

    if any(k in q for k in ["korean glass skin"]):
        return {"query": query, "answer": BUSINESS_FAQ["korean_glass_skin_facial"], "grounded": True}

    if any(k in q for k in ["mask"]):
        if "rejuvenating" in q:
            return {"query": query, "answer": BUSINESS_FAQ["rejuvenating_mask"], "grounded": True}
        if "brightening" in q:
            return {"query": query, "answer": BUSINESS_FAQ["brightening_mask"], "grounded": True}
        return {"query": query, "answer": BUSINESS_FAQ["brightening_mask"], "grounded": True}

    if any(k in q for k in ["threading", "eyebrow"]):
        return {"query": query, "answer": BUSINESS_FAQ["eyebrow_threading"], "grounded": True}

    if any(k in q for k in ["upper lip"]):
        return {"query": query, "answer": BUSINESS_FAQ["upper_lip_threading"], "grounded": True}

    if any(k in q for k in ["lower lip"]):
        return {"query": query, "answer": BUSINESS_FAQ["lower_lip_threading"], "grounded": True}

    if any(k in q for k in ["side lock"]):
        return {"query": query, "answer": BUSINESS_FAQ["side_locks_threading"], "grounded": True}

    if any(k in q for k in ["facial hair removal"]):
        return {"query": query, "answer": BUSINESS_FAQ["facial_hair_removal"], "grounded": True}

    if any(k in q for k in ["bleach", "detan"]):
        return {"query": query, "answer": BUSINESS_FAQ["face_neck_bleach"], "grounded": True}

    if any(k in q for k in ["hand bleach"]):
        return {"query": query, "answer": BUSINESS_FAQ["full_hand_bleach"], "grounded": True}

    if any(k in q for k in ["leg bleach"]):
        return {"query": query, "answer": BUSINESS_FAQ["full_leg_bleach"], "grounded": True}

    if any(k in q for k in ["back bleach"]):
        return {"query": query, "answer": BUSINESS_FAQ["full_back_bleach"], "grounded": True}

    if any(k in q for k in ["waxing", "wax"]):
        return {"query": query, "answer": BUSINESS_FAQ["upper_lips_wax"], "grounded": True}

    if any(k in q for k in ["body scrub", "body polishing"]):
        return {"query": query, "answer": BUSINESS_FAQ["body_polishing"], "grounded": True}

    if any(k in q for k in ["manicure", "pedicure"]):
        return {"query": query, "answer": BUSINESS_FAQ["advance_manicure"], "grounded": True}

    if any(k in q for k in ["pedicure"]):
        return {"query": query, "answer": BUSINESS_FAQ["pedicure"], "grounded": True}

    # Fallback: try needle agent / broader keyword matches
    return {"query": query, "answer": "Please contact customer services for any extra information.", "grounded": False}


# ============================================================
# AGENT SETUP
# ============================================================
agent = needle.Needle(
    tools=[faq_lookup],
    system="You are BizAssist, a friendly and professional support assistant for Yacchu's Hair Garage. "
           "When a customer asks a question, ALWAYS call faq_lookup with their exact question. "
           "Respond using ONLY the answer from faq_lookup. Never invent policies, prices, or procedures. "
           "Keep answers conversational but concise (2-3 sentences max). Be helpful and warm."
)


# ============================================================
# MAIN CHAT LOOP
# ============================================================
def main():
    print("=" * 55)
    print("  [BOT] Yacchu's Hair Garage Support Bot - Needle 3 (121M params)")
    print("  Type 'quit', 'exit', or 'bye' to end")
    print("=" * 55)

    # Show a welcome message
    print(f"\nBot: {get_greeting_response()}")

    while True:
        try:
            query = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n\nBot: {get_farewell_response()}")
            break

        query = query.strip()
        if not query:
            continue

        # Check for greeting/farewell FIRST (before agent)
        greeting_type = detect_greeting(query)
        if greeting_type == "greeting":
            print(f"Bot: {get_greeting_response()}")
            agent.reset()  # Reset conversation state
            continue
        elif greeting_type == "farewell":
            print(f"Bot: {get_farewell_response()}")
            break

        # Get answer from agent (with direct fallback)
        result = agent.run(query)

        answer = None
        if result.get('results'):
            for r in result['results']:
                if isinstance(r, dict) and 'answer' in r:
                    answer = r['answer']
                    break

        # Direct fallback (guaranteed to work)
        if not answer:
            direct = faq_lookup(query)
            answer = direct['answer']

        print(f"Bot: {answer}")


if __name__ == "__main__":
    main()