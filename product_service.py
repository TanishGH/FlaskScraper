from models import *

def upsert_product_data(product):
    # Upsert main product
    existing_product = Product.query.filter_by(title=product['title']).first()
    
    if existing_product:
        # Update existing product
        existing_product.viewport = product.get('viewport')
        existing_product.google_site_verification = product.get('google-site-verification')
        existing_product.apple_itunes_app = product.get('apple-itunes-app')
        existing_product.theme_color = product.get('theme-color')
        existing_product.og_site_name = product.get('og:site_name')
        existing_product.og_url = product.get('og:url')
        existing_product.og_image_alt = product.get('og:image:alt')
        existing_product.og_image_height = product.get('og:image:height')
        existing_product.og_image_width = product.get('og:image:width')
        existing_product.description = product.get('description')
        existing_product.og_title = product.get('og:title')
        existing_product.og_description = product.get('og:description')
        existing_product.og_image = product.get('og:image')
        existing_product.twitter_card = product.get('twitter:card')
        existing_product.price_currency = product.get('priceCurrency')
        db.session.add(existing_product)
        product_id = existing_product.id
    else:
        # Create new product
        new_product = Product(
            title=product['title'],
            viewport=product.get('viewport'),
            google_site_verification=product.get('google-site-verification'),
            apple_itunes_app=product.get('apple-itunes-app'),
            theme_color=product.get('theme-color'),
            og_site_name=product.get('og:site_name'),
            og_url=product.get('og:url'),
            og_image_alt=product.get('og:image:alt'),
            og_image_height=product.get('og:image:height'),
            og_image_width=product.get('og:image:width'),
            description=product.get('description'),
            og_title=product.get('og:title'),
            og_description=product.get('og:description'),
            og_image=product.get('og:image'),
            twitter_card=product.get('twitter:card'),
            price_currency=product.get('priceCurrency')
        )
        db.session.add(new_product)
        db.session.flush()  # To get the new product's ID
        product_id = new_product.id
    
    # Upsert product detail
    product_detail_data = product.get('product_detail', {})
    existing_detail = ProductDetail.query.filter_by(product_id=product_id).first()
    
    if existing_detail:
        existing_detail.name = product_detail_data.get('name')
        existing_detail.image = product_detail_data.get('image')
        existing_detail.description = product_detail_data.get('description')
        existing_detail.brand = product_detail_data.get('brand')
        existing_detail.sku = product_detail_data.get('sku')
        existing_detail.price = product_detail_data.get('price')
        existing_detail.currency = product_detail_data.get('currency')
        db.session.add(existing_detail)
    else:
        new_detail = ProductDetail(
            product_id=product_id,
            name=product_detail_data.get('name'),
            image=product_detail_data.get('image'),
            description=product_detail_data.get('description'),
            brand=product_detail_data.get('brand'),
            sku=product_detail_data.get('sku'),
            price=product_detail_data.get('price'),
            currency=product_detail_data.get('currency')
        )
        db.session.add(new_detail)
    
    # Upsert nutrition facts
    nutrition_data = product.get('nutrition_facts', {})
    existing_nutrition = NutritionFact.query.filter_by(product_id=product_id).first()
    
    if existing_nutrition:
        existing_nutrition.servings_per_container = nutrition_data.get('servings_per_container')
        existing_nutrition.serving_size = nutrition_data.get('serving_size')
        existing_nutrition.calories = nutrition_data.get('calories')
        existing_nutrition.disclaimer = nutrition_data.get('disclaimer')
        db.session.add(existing_nutrition)
        nutrition_id = existing_nutrition.id
        
        # Delete existing macros and micros to replace them
        Macro.query.filter_by(nutrition_fact_id=nutrition_id).delete()
        # Micro.query.filter_by(nutrition_fact_id=nutrition_id).delete()
    else:
        new_nutrition = NutritionFact(
            product_id=product_id,
            servings_per_container=nutrition_data.get('servings_per_container'),
            serving_size=nutrition_data.get('serving_size'),
            calories=nutrition_data.get('calories'),
            disclaimer=nutrition_data.get('disclaimer')
        )
        db.session.add(new_nutrition)
        db.session.flush()  # To get the new nutrition fact's ID
        nutrition_id = new_nutrition.id
    
    # Add macros and sub-nutrients
    macros_data = nutrition_data.get('macros', {})
    for macro_name, macro_data in macros_data.items():
        # Skip if this is actually a sub-nutrient (handled below)
        if macro_name in ['Saturated Fat', 'Trans Fat', 'Dietary Fiber', 'Sugar']:
            continue
            
        new_macro = Macro(
            nutrition_fact_id=nutrition_id,
            name=macro_name,
            amount=macro_data.get('amount'),
            daily_value=macro_data.get('daily_value')
        )
        db.session.add(new_macro)
        db.session.flush()  # To get the new macro's ID
        
        # Add sub-nutrients if they exist
        sub_nutrients_data = macro_data.get('sub_nutrients', {})
        for sub_name, sub_data in sub_nutrients_data.items():
            new_sub = SubNutrient(
                macro_id=new_macro.id,
                name=sub_name,
                amount=sub_data.get('amount'),
                daily_value=sub_data.get('daily_value')
            )
            db.session.add(new_sub)
    
    # Add micros
    # micros_data = nutrition_data.get('micros', {})
    # for micro_name, micro_data in micros_data.items():
    #     new_micro = Micro(
    #         nutrition_fact_id=nutrition_id,
    #         name=micro_name,
    #         amount=micro_data.get('amount'),
    #         daily_value=micro_data.get('daily_value')
    #     )
    #     db.session.add(new_micro)
    
    db.session.commit()

