import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

starting_image = 1
product_id = 3
total_images = 100

for i in range(starting_image, total_images+1):
    img = "products/"+str(i)+".jpg"
    product_id += 1
    cursor.execute('''
        INSERT INTO storefront_product_images (
            img, product_id
        ) VALUES (?, ?)
    ''', (img, product_id))

conn.commit()
conn.close()
