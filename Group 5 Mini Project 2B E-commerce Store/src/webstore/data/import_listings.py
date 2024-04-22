import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

with open('listings_fixed.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        # Exclude the last two columns (discount and seller_id) from the CSV row
        name, inventory, min_price, max_price, current_price, rating, strategy, slug, product_id, _ = row
        seller_id = 1  # Set seller_id to 1 for every record
        cursor.execute('''
            INSERT INTO storefront_listing (
                name, inventory, min_price, max_price,
                current_price, rating, strategy, slug,
                product_id, seller_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, inventory, min_price, max_price, current_price, rating, strategy, slug, product_id, seller_id))

conn.commit()
conn.close()
