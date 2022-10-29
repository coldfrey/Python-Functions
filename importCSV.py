# import csvfile and extract data using set of rules outlined below

import pandas as pd


# Notes for Andre:
# - below is a not working version of what we are going for. 

# The Taxons and the sizes should already be in the Sanity database and hence no need to reupload.
# The prices are tbc and will be added later. For now we can just make the SKUs on Commerce Layer and add the prices later.

# See also sanity_connect.py for how to connect to Sanity and make a query.

# See sudo code below:

# 1. Create a list of unique taxons
# 2. For each taxon, create a taxon object
# 3. Create a list of products
# 4. For each product, create a product object
# 5. Create a list of variants (There will need to be a varient added for each of the accessories because the accessories varients are not in the CSV)
# 6. For each variant, create a variant object
# 7. Add variant to product
# 8. Add product to taxon
# 9. Add taxon to list of taxons
# 10. Print the first variant of the first product of the first taxon - First test.
# 11. Upload variants to Sanity - update or insert
# 12. Upload products to Sanity - update or insert
# 13. Upload taxons to Sanity - update or insert
# 15. For each SKU (Variant), create a SKU object on Commerce Layer

# DONE! Enjoy your weekend!




# read csv file
product_upload_df = pd.read_csv('EPU.csv') # Envision Product Upload

# Column names
# print(df.columns)
# 'Product SKU', 'Barcode EAN', 'HS Codes', 'Type', 'Taxons', 'Size', 'Colour', 'Product Name', 'Price', 'Inventory (qty)', 'Composition', 'COO', 'MOQ', 'OQI', 'Image Source', 'Weight', 'Pieces Per Pack'

# sizes - Will need to be uploaded to Sanity before uploading products/variants, update or insert.
sizes = product_upload_df['Size'].unique() 

# colours - Will need to be uploaded to Sanity before uploading products/variants, update or insert.
# colours = product_upload_df['Colour'].unique() # note that for this catalogue, there are no colours.

# create Class for Taxons
class Taxon:
    def __init__(self, name):
        self.name = name
        self.label = name # Will update in Sanity
        # generate slug
        self.slug = self.name.lower().replace(' ', '-')
        self.products = []


# Create Class for Products
class Product:
  def __init__(
    self,
    name, 
    composition, 
    coo, 
    slug,
    moq, 
    oqi, 
    reference,
    price,
    ):
    self.name = name
    # self.description = description
    self.composition = composition
    self.coo = coo
    self.slug = slug
    self.moq = moq
    self.oqi = oqi
    self.reference = reference
    self.price = price
    self.variants = []


# Create Class for Variants
class Variant:
  def __init__(
    self,
    name, # [Product Name] ([size] [colour])
    sku,
    barcode,
    # lead_time,
    size, 
    # colour,
    ):
    self.sku = sku
    self.barcode = barcode
    self.size = size
    # self.colour = colour
    # generate slug
    self.name = name

# Create list of unique taxons
taxons = product_upload_df['Taxons'].unique()

# Create list of products

for taxon in taxons:
    # create taxon object
    taxon = Taxon(taxon)
    # create list of products
    products = product_upload_df[product_upload_df['Taxons'] == taxon.name]
    # create list of unique products where 'Type' == 'Product'
    unique_products = products[products['Type'] == 'Product']['Product Name'].unique()
    for product in unique_products:
      # create product object
      product = Product(
        name = product,
        # description = product['Description'],
        composition = product['Composition'],
        coo = product['COO'],
        slug = product['Product Name'].lower().replace(' ', '-'),
        moq = product['MOQ'],
        oqi = product['OQI'],
        reference = product['Product SKU'],
        price = product['Price'],
        )
      # create list of variants
      variants = products[products['Product Name'] == product.name]
      # for each variant, create a variant object
      for variant in variants:
        # create variant object
        variant = Variant(
          name = variant['Product Name'] + ' (' + variant['Size'] + ')',
          sku = variant['Product SKU'],
          barcode = variant['Barcode EAN'],
          # lead_time = variant['Lead Time'],
          size = variant['Size'],
          # colour = variant['Colour'],
          )
          # add variant to product
        product.variants.append(variant)
      # add product to taxon
      taxon.products.append(product)
    # add taxon to list of taxons
    taxons.append(taxon)

# print the first variant of the first product of the first taxon - First test.
print(taxons[0].products[0].variants[0].name)


