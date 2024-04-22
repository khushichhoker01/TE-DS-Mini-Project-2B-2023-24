import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

starting_image = 0
product_id = 3
total_images = 100

for i in range(starting_image, total_images + 1):
    img = "products/" + str(i) + ".jpg"
    cursor.execute('''
        UPDATE storefront_product
        SET img = ?
        WHERE id = ?
    ''', (img, product_id))
    product_id += 1

conn.commit()
conn.close()
