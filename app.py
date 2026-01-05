from flask import Flask, request, render_template, redirect, url_for, flash
from textblob import TextBlob

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "supersecretkey"  # Needed for flashing messages

# --- Product Data ---
PRODUCTS = [
    {
        "id": "s24",
        "name": "Samsung Galaxy S24",
        "description": "Cutting-edge tech, a stunning display, and a powerful processor. Perfect for work and entertainment.",
        "price": "₹79,999",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6570/6570268_sd.jpg"
    },
    {
        "id": "s24ultra",
        "name": "Samsung Galaxy S24 Ultra",
        "description": "Titanium frame, Snapdragon 8 Gen 3, built-in S Pen, and a 200MP quad camera system. The ultimate Android flagship.",
        "price": "₹1,29,999",
        "image_url": "https://media.hifi.lu/sys-master/products/9337882542110/1440x1440.51006326_01.webp"
    },
     {
        "id": "s25",
        "name": "Samsung Galaxy S25",
        "description": "Next-gen Snapdragon 8 Gen 4 chip, improved AI photo processing, and vibrant 120Hz AMOLED display.",
        "price": "₹89,999",
        "image_url": "https://media.elkjop.com/assets/image/dv_web_D18000128913971"
    },
    {
        "id": "s25plus",
        "name": "Samsung Galaxy S25 Plus",
        "description": "A bigger, faster, and smarter Galaxy with Snapdragon 8 Gen 4, AI-powered camera, and long-lasting battery.",
        "price": "₹1,04,999",
        "image_url": "https://cdn.findprix.com/images/products/samsung-galaxy-s25-plus_14.webp"
    },
    {
        "id": "s25ultra",
        "name": "Samsung Galaxy S25 Ultra",
        "description": "The ultimate Samsung flagship: 200MP camera, built-in S Pen, Galaxy AI features, and a titanium frame.",
        "price": "₹1,49,999",
        "image_url": "https://cdn.beebom.com/mobile/samsung-galaxy-s25-ultra-front-and-back-1.png"
    },
    {
        "id": "pixel8",
        "name": "Google Pixel 8",
        "description": "The Google AI-powered phone. Incredible camera quality and helpful features for your day.",
        "price": "₹69,999",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6559/6559243_sd.jpg"
    },
    {
        "id": "pixel8pro",
        "name": "Google Pixel 8 Pro",
        "description": "Google Tensor G3, Pro camera system, and advanced AI features for photos, voice, and productivity.",
        "price": "₹1,06,999",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6559/6559254_sd.jpg"
    },
    {
        "id": "iphone15",
        "name": "Apple iPhone 15",
        "description": "Featuring the Dynamic Island, A16 Bionic chip, and a durable color-infused glass design.",
        "price": "₹79,900",
        "image_url": "https://variety.com/wp-content/uploads/2023/09/apple-iphone-15.jpg"
    },
     {
        "id": "iphone15pro",
        "name": "Apple iPhone 15 Pro",
        "description": "Titanium design, A17 Pro chip, USB-C, and a powerful 48MP main camera. Compact, fast, and professional.",
        "price": "₹1,34,900",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6525/6525407_sd.jpg"
    },
    {
        "id": "iphone15promax",
        "name": "Apple iPhone 15 Pro Max",
        "description": "A17 Pro chip, 5x optical zoom telephoto camera, and a massive Super Retina XDR display.",
        "price": "₹1,59,900",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6525/6525421_sd.jpg"
    },
     {
        "id": "iphone16",
        "name": "Apple iPhone 16",
        "description": "The latest Apple flagship featuring the A18 chip, Apple Intelligence, and an even brighter Super Retina display.",
        "price": "₹89,900",
        "image_url": "https://think-ecuador.com/wp-content/uploads/2024/09/iPhone-16-Teal-1.png"
    },
    {
        "id": "iphone16pro",
        "name": "Apple iPhone 16 Pro",
        "description": "A18 Pro chip, titanium design, ProMotion display, and AI-powered camera enhancements.",
        "price": "₹1,39,900",
        "image_url":"https://cdn.shopify.com/s/files/1/0670/7688/2653/files/86fb9f06-1525-4b23-b257-805885ac798a-1_d60e4f68-d823-4bc0-b840-16b850cb12fa.png?v=1727445542"
    },
    {
        "id": "iphone16promax",
        "name": "Apple iPhone 16 Pro Max",
        "description": "Apple’s most advanced phone yet: A18 Pro chip, 5x telephoto zoom, and enhanced Apple Intelligence features.",
        "price": "₹1,69,900",
        "image_url": "https://jjstore.ru/image/cache/catalog/iphone16pro/desert/iphone_16pro_desert1-1181x865.png"
    },
    {
        "id": "oneplus12",
        "name": "OnePlus 12",
        "description": "Flagship performance with Snapdragon 8 Gen 3, Fluid AMOLED display, and fast charging.",
        "price": "₹64,999",
        "image_url": "https://static1.howtogeekimages.com/wordpress/wp-content/uploads/2024/01/oneplus-12-silky-black.jpg"
    },
    {
        "id": "oneplus12r",
        "name": "OnePlus 12R",
        "description": "A performance beast with Snapdragon 8 Gen 2, 1.5K display, and 100W SUPERVOOC fast charging.",
        "price": "₹45,999",
        "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/d343aa5e-68a0-4650-8b55-257874ef7a24.jpg"
    },
    {
        "id": "xiaomi14",
        "name": "Xiaomi 14",
        "description": "Leica-powered camera, brilliant performance, and sleek design at an amazing price.",
        "price": "₹59,999",
        "image_url": "https://m-cdn.phonearena.com/images/phones/84333-940/Xiaomi-14.jpg?w=1"
    },
    {
        "id": "xiaomi14ultra",
        "name": "Xiaomi 14 Ultra",
        "description": "Leica Summilux optics, Snapdragon 8 Gen 3, 2K AMOLED display, and ceramic design. Built for photography pros.",
        "price": "₹99,999",
        "image_url": "https://assets.mmsrg.com/isr/166325/c1/-/ASSET_MP_137560106/fee_786_587_png"
    },
    {
        "id": "nothing2",
        "name": "Nothing Phone (2)",
        "description": "Transparent design, unique Glyph interface, and a clean Android experience.",
        "price": "₹44,999",
        "image_url": "https://m.media-amazon.com/images/I/71x5ntU43-L._AC_SL1500_.jpg"
    }
]

# --- Review Storage (in-memory for demo) ---
REVIEWS = {}

# --- Sentiment Analysis ---
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def sentiment_to_rating(polarity):
    rating = int(round((polarity + 1) * 2)) + 1  # roughly maps -1..1 to 1..5
    return max(1, min(5, rating))

def sentiment_label(polarity):
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    return "Neutral"

# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html', products=PRODUCTS)

@app.route('/product/<product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        review_text = request.form['review'].strip()
        if not review_text:
            flash("Please enter a review before submitting.", "warning")
            return redirect(url_for('product_page', product_id=product_id))

        polarity = get_sentiment(review_text)
        rating = sentiment_to_rating(polarity)
        sentiment = sentiment_label(polarity)

        REVIEWS.setdefault(product_id, []).append({
            "text": review_text,
            "sentiment": sentiment,
            "rating": rating
        })

        flash("Your review has been submitted!", "success")
        return redirect(url_for('product_page', product_id=product_id))

    product_reviews = REVIEWS.get(product_id, [])
    avg_rating = round(sum(r['rating'] for r in product_reviews) / len(product_reviews), 1) if product_reviews else None

    return render_template('product.html', product=product, reviews=product_reviews, avg_rating=avg_rating)

if __name__ == '__main__':
    app.run(debug=True)
