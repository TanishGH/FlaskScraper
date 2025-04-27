# Flask Scraper

## Description
This project is a web scraper built using Flask to scrape data from a website and list it in an organized format.

## Features
- Scrapes data.
- Returns product information like name, price, description, nutrition values etc.
- Exports data in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TanishGH/FlaskScraper.git

2. Install dependencies:

   pip install -r requirements.txt
   python app.py

3. product.json:

   contains the data stored in db represented in a nested json format.

4. apiDoc.txt:

   contains the api documentation


5. schema.py

   Created Marshmallow schemas for Product, ProductDetail, NutritionFact, Macro, and SubNutrient models.

   Implemented nested schemas to serialize related objects cleanly (e.g., macros inside nutrition facts).

   Developed lightweight schema versions for optimized product listing APIs.

   Controlled exposed fields using Marshmallow fields option for efficient responses.

   Maintained foreign key relationships with include_fk=True in schemas.

   Instantiated reusable schema objects for API integration.

6. view.py

   Developed API to fetch single product details with deep nested relations (product details, nutrition facts, macros, sub-nutrients).

   Implemented duplicate removal logic for sub-nutrients in API response.

   Built paginated API for listing products with minimal required fields.

   Created scrape-and-save endpoint to extract product data from a URL and upsert into the database.

7. models.py

   Designed SQLAlchemy models for Product, ProductDetail, NutritionFact, Macro, and SubNutrient entities.

   Established one-to-one relationships between Product and ProductDetail/NutritionFact.

   Created one-to-many relationships from NutritionFact to Macro, and Macro to SubNutrient.

   Used cascade delete on child relationships to maintain data integrity.

   Defined clear foreign key constraints to link models properly.

   Prepared the database structure for flexible product metadata and nutrition fact management.

