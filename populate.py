import requests

BASE = "http://127.0.0.1:5000"

# Categories: id -> name
categories = {
    1: "Electronics",
    2: "Home & Furniture",
    3: "Gaming Accessories"
}

# Products per category: (name, description, price)
products = {
    1: [
        ("UltraSonic Noise-Cancelling Bluetooth Headphones with 48-Hour Battery Life and Alexa Integration",
         "Top-tier headphones with deep bass, long battery, and voice control.",
         299.99),
        ("QuantumEdge 32GB RAM Gaming Laptop with 4K OLED Display and Liquid Cooling System",
         "Powerful gaming laptop for hardcore gamers and content creators.",
         2499.99),
        ("SmartVision AI-Powered 75-inch 8K Ultra HD Smart TV with Voice Control",
         "Massive 8K display with AI enhancements and built-in streaming apps.",
         5999.99)
    ],
    2: [
        ("ErgoComfort Memory Foam Recliner Chair with Heated Massage and Cup Holder",
         "Comfortable recliner for home living rooms with massage and heating.",
         499.99),
        ("LuxWood Solid Oak Dining Table Set with Extendable Leaf and 6 Ergonomic Chairs",
         "Elegant oak dining set, seats 6, extendable for guests.",
         1299.99),
        ("CloudSoft King Size Hybrid Mattress with Cooling Gel and 12-Zone Support",
         "Premium mattress with perfect firmness and cooling gel.",
         899.99)
    ],
    3: [
        ("HyperX RGB Mechanical Gaming Keyboard with Programmable Macro Keys and Wrist Rest",
         "Satisfying mechanical switches with customizable RGB lighting.",
         149.99),
        ("PhantomEdge Wireless Gaming Mouse with 16000 DPI Sensor and Customizable Buttons",
         "Ultra-precise mouse for competitive gaming with ergonomic design.",
         89.99),
        ("UltraGamer 34-inch Curved 144Hz Monitor with FreeSync and HDR Support",
         "Immersive ultra-wide monitor for ultimate gaming experience.",
         549.99)
    ]
}

# Good and bad reviews
good_comments = [
    "Absolutely love this! Works perfectly and exceeded my expectations.",
    "Fantastic product! Highly recommend to everyone.",
    "Incredible quality and service. Worth every penny.",
    "Exceeded my expectations. Top-notch quality!"
]

bad_comments = [
    "Terrible experience. Broke within a week and support is useless.",
    "Very disappointed. Quality is poor and delivery was late.",
    "Not worth the money. Completely regret this purchase.",
    "Worst purchase ever. Would not recommend."
]

# Function to add products
def add_product(name, description, price, category_id):
    r = requests.post(f"{BASE}/add_product", json={
        "name": name,
        "description": description,
        "price": price,
        "category_id": category_id
    })
    if r.status_code == 200:
        return r.json()["product_id"]
    else:
        # If endpoint doesn't exist, assume product already exists
        return None

# Now we bombard the reviews
review_id = 1
for cat_id, product_list in products.items():
    for idx, (name, desc, price) in enumerate(product_list):
        product_id = idx + 1 + sum(len(products[c]) for c in products if c < cat_id)  # simple ID calc
        for i in range(50):
            # Decide good or bad based on category
            if cat_id == 1:  # Electronics: alternate
                comment = good_comments[i % len(good_comments)] if i % 2 == 0 else bad_comments[i % len(bad_comments)]
                rating = 5 if i % 2 == 0 else 1
            elif cat_id == 2:  # Home: mostly bad
                comment = good_comments[i % len(good_comments)] if i % 3 == 0 else bad_comments[i % len(bad_comments)]
                rating = 5 if i % 3 == 0 else 2
            else:  # Gaming Accessories: mostly good
                comment = good_comments[i % len(good_comments)] if i % 4 != 0 else bad_comments[i % len(bad_comments)]
                rating = 5 if i % 4 != 0 else 1

            data = {
                "product_id": product_id,
                "rating": rating,
                "comment": comment
            }
            r = requests.post(f"{BASE}/add_review", json=data)
            if r.status_code == 200:
                print(f"Added review {review_id} for product {product_id}")
            else:
                print(f"Failed to add review {review_id} for product {product_id}: {r.text}")
            review_id += 1

print("All reviews added! Sentiment analysis should now be triggered. Victory at all costs!")
