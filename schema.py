from flask_marshmallow import Marshmallow
from models import Product, ProductDetail, NutritionFact, Macro, SubNutrient #, Micro

ma = Marshmallow()

class SubNutrientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubNutrient
        include_fk = True
        fields = ('id', 'name', 'amount', 'daily_value')

class MacroSchema(ma.SQLAlchemyAutoSchema):
    sub_nutrients = ma.Nested(SubNutrientSchema, many=True)
    
    class Meta:
        model = Macro
        include_fk = True
        fields = ('id', 'name', 'amount', 'daily_value', 'sub_nutrients')

# class MicroSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Micro
#         include_fk = True
#         fields = ('id', 'name', 'amount', 'daily_value')

class NutritionFactSchema(ma.SQLAlchemyAutoSchema):
    macros = ma.Nested(MacroSchema, many=True)
    # micros = ma.Nested(MicroSchema, many=True)
    
    class Meta:
        model = NutritionFact
        include_fk = True
        fields = ('id', 'servings_per_container', 'serving_size', 'calories', 
                 'disclaimer', 'macros') #, 'micros')

class ProductDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductDetail
        include_fk = True
        fields = ('id', 'name', 'image', 'description', 'brand', 
                 'sku', 'price', 'currency')

class ProductSchema(ma.SQLAlchemyAutoSchema):
    product_detail = ma.Nested(ProductDetailSchema)
    nutrition_fact = ma.Nested(NutritionFactSchema)
    
    class Meta:
        model = Product
        include_fk = True
        fields = ('id', 'title', 'viewport', 'google_site_verification',
                 'apple_itunes_app', 'theme_color', 'og_site_name', 'og_url',
                 'og_image_alt', 'og_image_height', 'og_image_width', 'description',
                 'og_title', 'og_description', 'og_image', 'twitter_card',
                 'price_currency', 'product_detail', 'nutrition_fact')

# Instantiate schemas
product_schema = ProductSchema()




class ProductDetailSchemaV2(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductDetail
        fields = ('id', 'name', 'image', 'price', 'currency', 'brand')


class ProductListingSchema(ma.SQLAlchemyAutoSchema):
    product_detail = ma.Nested(ProductDetailSchemaV2)
    
    class Meta:
        model = Product
        fields = (
            'id', 
            'title', 
            'og_image', 
            'price_currency',
            'description',
            'product_detail'
        )

product_listing_schema = ProductListingSchema(many=True)