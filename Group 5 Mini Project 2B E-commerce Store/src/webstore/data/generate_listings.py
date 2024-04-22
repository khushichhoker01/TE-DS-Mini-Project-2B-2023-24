import csv
import random
import re

def generate_slug(product_name, iterable):
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s]', '', product_name)  # Keep only alphanumeric characters and spaces
    cleaned_name = cleaned_name.replace(' ', '_')  # Replace spaces with underscores
    slug = f"{cleaned_name.lower()}-{iterable}"
    return slug

def generate_data(max_price, min_price, rating, strategy):
    price_diff = max_price - min_price
    if rating >= 4:
        discount = 0.25 * price_diff
    elif rating == 3:
        discount = 0.35 * price_diff
    elif rating == 2:
        discount = 0.45 * price_diff
    elif rating == 1:
        discount = 0.6 * price_diff
    else:
        discount = 0.2 * price_diff
    discount = int(discount+(0.1*strategy*discount))
    current_price = int(min(max(max_price - discount, min_price),max_price))
    return discount, current_price

def generate_listings(csv_file, output_file, listing_limits=(20, 30)):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        listings = []
        product_id = 3  # Starting product ID
        for row in reader:
            lower_limit, upper_limit = listing_limits
            num_listings = random.randint(lower_limit, upper_limit)
            for i in range(num_listings):
                name = row['Product Name']
                inventory = random.randint(20, 1000)
                rating = random.randint(1, 5)
                strategy = random.randint(1, 5)
                min_price = int(row['min_price']) - random.randint(1, 15) * int(row['min_price']) // 100
                max_price = int(row['max_price']) + random.randint(1, 15) * int(row['max_price']) // 100
                
                # Generate data and calculate discount and current price
                discount, current_price = generate_data(max_price, min_price, rating, strategy)
                
                slug = generate_slug(name, i)
                product_fk = product_id
                
                listings.append({
                    'name': name,
                    'inventory': inventory,
                    'min_price': min_price,
                    'max_price': max_price,
                    'current_price': current_price,
                    'rating': rating,
                    'strategy': strategy,
                    'slug': slug,
                    'product(fk)': product_fk,
                    'discount': discount  # Include discount in the CSV output
                })
            product_id += 1
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['name', 'inventory', 'min_price', 'max_price', 'current_price', 'rating', 'strategy', 'slug', 'product(fk)', 'discount']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)

# Usage example:
generate_listings('product_prices.csv', 'listings.csv', listing_limits=(20, 30))
