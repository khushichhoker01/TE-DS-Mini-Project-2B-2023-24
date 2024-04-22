import csv

# Open the input CSV file for reading
with open('listings.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = list(csv_reader)

# Loop over each record and increment the product foreign key by 1
for record in data:
    record['product(fk)'] = int(record['product(fk)']) + 1

# Define the fieldnames for the output CSV file
fieldnames = [
    "name", "inventory", "min_price", "max_price", "current_price",
    "rating", "strategy", "slug", "product(fk)", "discount"
]

# Open the output CSV file for writing
with open('listings_fixed.csv', mode='w', newline='') as csv_output:
    writer = csv.DictWriter(csv_output, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the modified data to the output CSV file
    writer.writerows(data)

print("Product foreign keys incremented and saved to output_file.csv")
