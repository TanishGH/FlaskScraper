import httpx
from bs4 import BeautifulSoup
import json

def scrape_product(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # try:
    with httpx.Client(timeout=55) as client:
        response = client.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    product_data = {}

    title_tag = soup.find("title")
    if title_tag:
        product_data["title"] = title_tag.text.strip()

    meta_tags = soup.find_all("meta")
    for tag in meta_tags:
        if tag.get("property"):
            key = tag.get("property")
            value = tag.get("content", "")
            product_data[key] = value
        elif tag.get("name"):
            key = tag.get("name")
            value = tag.get("content", "")
            product_data[key] = value

    # Product detail
    product_detail = {
        "name": None,
        "image": None,
        "description": None,
        "brand": None,
        "sku": None,
        "price": None,
        "currency": None
    }

    script_tags = soup.find_all('script', type='application/ld+json')
    for script_tag in script_tags:
        try:
            raw_data = script_tag.string.strip()
            if raw_data:
                data = json.loads(raw_data)
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Product':
                            data = item
                            break

                if data.get('@type') == 'Product':
                    product_detail['name'] = data.get('name')
                    product_detail['image'] = data.get('image')
                    product_detail['description'] = data.get('description')
                    product_detail['brand'] = data.get('brand', {}).get('name') if isinstance(data.get('brand'), dict) else data.get('brand')
                    product_detail['sku'] = data.get('sku')

                    offers = data.get('offers', [{}])[0] if isinstance(data.get('offers'), list) else data.get('offers')
                    product_detail['price'] = offers.get('price')
                    product_detail['currency'] = offers.get('priceCurrency')
                    break
        except Exception:
            continue

    product_data['product_detail'] = product_detail

    # Nutrition facts
    nutrition_facts = {}

    nutrition_section = soup.find("div", class_="NutritionLabel")
    if nutrition_section:
        servings_per_container = nutrition_section.find("div", class_="NutritionLabel-ServingsPerContainer")
        if servings_per_container:
            nutrition_facts['servings_per_container'] = servings_per_container.text.strip()

        serving_size = nutrition_section.find("div", class_="NutritionLabel-ServingSize")
        if serving_size:
            nutrition_facts['serving_size'] = ' '.join([span.text.strip() for span in serving_size.find_all("span")])

        calories = nutrition_section.find("div", class_="NutritionLabel-Calories")
        if calories:
            nutrition_facts['calories'] = ' '.join([span.text.strip() for span in calories.find_all("span")])

        macros = {}
        macro_sections = nutrition_section.find_all("div", class_="Nutrient")
        for macro in macro_sections:
            title = macro.find("span", class_="NutrientDetail-Title")
            amount = macro.find("span", class_="NutrientDetail-TitleAndAmount")
            daily_value = macro.find("span", class_="NutrientDetail-DailyValue")

            if title:
                macro_name = title.text.strip()
                macro_data = {}

                if amount:
                    macro_data['amount'] = amount.text.replace(title.text, '').strip()
                if daily_value:
                    macro_data['daily_value'] = daily_value.text.strip()

                sub_nutrients = {}
                sub_nutrient_sections = macro.find_all("div", class_="NutrientDetail-SubNutrients")
                for sub_section in sub_nutrient_sections:
                    for sub_nutrient in sub_section.find_all("div", class_="Nutrient"):
                        sub_title = sub_nutrient.find("span", class_="NutrientDetail-Title")
                        sub_amount = sub_nutrient.find("span", class_="NutrientDetail-TitleAndAmount")
                        sub_daily_value = sub_nutrient.find("span", class_="NutrientDetail-DailyValue")

                        if sub_title:
                            sub_name = sub_title.text.strip()
                            sub_data = {}

                            if sub_amount:
                                sub_data['amount'] = sub_amount.text.replace(sub_title.text, '').strip()
                            if sub_daily_value:
                                sub_data['daily_value'] = sub_daily_value.text.strip()

                            sub_nutrients[sub_name] = sub_data

                if sub_nutrients:
                    macro_data['sub_nutrients'] = sub_nutrients

                macros[macro_name] = macro_data

        nutrition_facts['macros'] = macros

        # micros = {}
        # micro_sections = nutrition_section.find_all("div", class_="NutritionLabel-Micros")
        # for micro_section in micro_sections:
        #     for micro in micro_section.find_all("div", class_="Nutrient"):
        #         title = micro.find("span", class_="NutrientDetail-Title")
        #         amount = micro.find("span", class_="NutrientDetail-TitleAndAmount")
        #         daily_value = micro.find("span", class_="NutrientDetail-DailyValue")

        #         if title:
        #             micro_name = title.text.strip()
        #             micro_data = {}

        #             if amount:
        #                 micro_data['amount'] = amount.text.replace(title.text, '').strip()
        #             if daily_value:
        #                 micro_data['daily_value'] = daily_value.text.strip()

        #             micros[micro_name] = micro_data

        # nutrition_facts['micros'] = micros

        disclaimer = nutrition_section.find("div", class_="NutritionLabel-DailyValueDisclaimer")
        if disclaimer:
            nutrition_facts['disclaimer'] = disclaimer.text.strip()

    product_data['nutrition_facts'] = nutrition_facts

    return product_data

    # except Exception as e:
    #     print(f"Scraping error: {e}")
    #     return None
