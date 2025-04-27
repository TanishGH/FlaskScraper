# controllers/product_controller.py
from flask import Blueprint, jsonify
from models import Product, NutritionFact, Macro, db
from schema import product_schema, product_listing_schema
from scraper import scrape_product
from product_service import upsert_product_data
from sqlalchemy.orm import joinedload
from flask import request

product_bp = Blueprint('products', __name__)

@product_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = (
        Product.query
        .options(
            joinedload(Product.product_detail),
            joinedload(Product.nutrition_fact)
            .joinedload(NutritionFact.macros)
            .joinedload(Macro.sub_nutrients),
            joinedload(Product.nutrition_fact)
            # .joinedload(NutritionFact.micros)
        )
        .get_or_404(product_id)
    )
    
    # Serialize with custom handling to prevent duplicates
    result = product_schema.dump(product)
    
    # Post-processing to remove any potential duplicates
    if result.get('nutrition_fact', {}).get('macros'):
        for macro in result['nutrition_fact']['macros']:
            if macro.get('sub_nutrients'):
                # Remove duplicate sub-nutrients by name
                seen = set()
                unique_sub_nutrients = []
                for sub in macro['sub_nutrients']:
                    if sub['name'] not in seen:
                        seen.add(sub['name'])
                        unique_sub_nutrients.append(sub)
                macro['sub_nutrients'] = unique_sub_nutrients
    
    return jsonify(result)


@product_bp.route('/products', methods=['GET'])
def get_products():
    
    """Get paginated list of products"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    products = (
        Product.query
        .options(
            joinedload(Product.product_detail)
        )
        .order_by(Product.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    
    # Serialize the product list
    result = {
        'products': product_listing_schema.dump(products.items),
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    }
    
    return jsonify(result)


@product_bp.route('/scrape', methods=['POST'])
def scrape_and_upsert():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    product_data = scrape_product(url)
    if not product_data:
        return jsonify({"error": "Failed to scrape the URL."}), 500

    # try:
    upsert_product_data(product_data)
    return jsonify({"message": "Product scraped and saved successfully."}), 201
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
