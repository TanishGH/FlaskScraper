from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# -------------------------
# Main Product Metadata
# -------------------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    viewport = db.Column(db.String)
    google_site_verification = db.Column(db.String)
    apple_itunes_app = db.Column(db.String)
    theme_color = db.Column(db.String)
    og_site_name = db.Column(db.String)
    og_url = db.Column(db.String)
    og_image_alt = db.Column(db.String)
    og_image_height = db.Column(db.String)
    og_image_width = db.Column(db.String)
    description = db.Column(db.Text)
    og_title = db.Column(db.String)
    og_description = db.Column(db.Text)
    og_image = db.Column(db.String)
    twitter_card = db.Column(db.String)
    price_currency = db.Column(db.String)

    # One-to-one relationships
    product_detail = db.relationship('ProductDetail', backref='product', uselist=False)
    nutrition_fact = db.relationship('NutritionFact', backref='product', uselist=False)

# -------------------------
# Product Detail
# -------------------------
class ProductDetail(db.Model):
    __tablename__ = "product_details"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    brand = db.Column(db.String)
    sku = db.Column(db.String)
    price = db.Column(db.String)
    currency = db.Column(db.String)

# -------------------------
# Nutrition Fact
# -------------------------
class NutritionFact(db.Model):
    __tablename__ = "nutrition_facts"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    servings_per_container = db.Column(db.String)
    serving_size = db.Column(db.String)
    calories = db.Column(db.String)
    disclaimer = db.Column(db.Text)

    # One-to-many relationships
    macros = db.relationship('Macro', backref='nutrition_fact', cascade="all, delete-orphan")
    # micros = db.relationship('Micro', backref='nutrition_fact', cascade="all, delete-orphan")

# -------------------------
# Macro Nutrients
# -------------------------
class Macro(db.Model):
    __tablename__ = "macros"

    id = db.Column(db.Integer, primary_key=True)
    nutrition_fact_id = db.Column(db.Integer, db.ForeignKey('nutrition_facts.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.String)
    daily_value = db.Column(db.String)

    # One-to-many relationship for sub-nutrients
    sub_nutrients = db.relationship('SubNutrient', backref='macro', cascade="all, delete-orphan")

# -------------------------
# Sub Nutrients (under Macros)
# -------------------------
class SubNutrient(db.Model):
    __tablename__ = "sub_nutrients"

    id = db.Column(db.Integer, primary_key=True)
    macro_id = db.Column(db.Integer, db.ForeignKey('macros.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.String)
    daily_value = db.Column(db.String)

# -------------------------
# Micro Nutrients
# -------------------------
# class Micro(db.Model):
#     __tablename__ = "micros"

#     id = db.Column(db.Integer, primary_key=True)
#     nutrition_fact_id = db.Column(db.Integer, db.ForeignKey('nutrition_facts.id'), nullable=False)

#     name = db.Column(db.String, nullable=False)
#     amount = db.Column(db.String)
#     daily_value = db.Column(db.String)
