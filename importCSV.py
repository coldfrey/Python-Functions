# import csvfile and extract data using set of rules outlined below

import pandas as pd
import numpy as np

from uncommonClasses import Taxon, Product, Variant

# Read CSV file
product_upload_df = pd.read_csv('EPU.csv')

# Split df into Products and Variants
unique_products = product_upload_df[product_upload_df['Type'] == 'Product']['Product Name'].dropna().unique()

# Create a new column in the dataframe to hold product type
# for each unique product, check if string exists in the product name column, if so, assign product type to the new column
product_upload_df['Product Type'] = np.nan
for product in unique_products:
    product_upload_df.loc[product_upload_df['Product Name'].str.contains(product), 'Product Type'] = product

    # Assign the same taxon to all variants of the same product
    product_upload_df.loc[product_upload_df['Product Name'].str.contains(product), 'Taxons'] = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product), 'Taxons'].iloc[0]
 
# Split the dataframe into two dataframes, one for products and one for variants
product_df = product_upload_df[product_upload_df['Type'] == 'Product']
variant_df = product_upload_df[product_upload_df['Type'] == 'Variant']

# For each product, if the Product sku column is NaN, assign the Product sku of its first variant to the product sku column
for product in unique_products:
    if pd.isna(product_df.loc[product_df['Product Type'] == product, 'Product SKU'].iloc[0]):
        product_df.loc[product_df['Product Type'] == product, 'Product SKU'] = variant_df.loc[variant_df['Product Name'].str.contains(product), 'Product SKU'].iloc[0] + '-P'

# sizes - Will need to be uploaded to Sanity before uploading products/variants, update or insert.
sizes = product_upload_df['Size'].dropna().unique() 

# Create list of unique taxons
taxons = product_df['Taxons'].dropna().unique()
AllTaxons = []

# Create list of products
for taxon in taxons:
    taxon = Taxon(taxon)

    # create list of products
    products = product_df[product_df['Taxons'] == taxon.name]

    for index, product in products.iterrows():

      # create product object
      product = Product(
        name = product['Product Name'],
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
      variants = variant_df[variant_df['Product Type'] == product.name]

      # for each variant, create a variant object
      for index, row in variants.iterrows():
        variant = Variant(
          name = row['Product Name'],
          sku = row['Product SKU'],
          barcode = row['Barcode EAN'],
          size = row['Size'],
          # colour = row['Colour'],
          )
        # append variant object to product object
        product.variants.append(variant)
      
      # add product to taxon
      taxon.products.append(product)
    # add taxon to list of taxons
    AllTaxons.append(taxon)


# print the first variant of the first product of the first taxon - First test.
print(AllTaxons[0].products[0].variants[0].name)

# create toJson dictionary
toJson = {}
for taxon in AllTaxons:
  toJson[taxon.name] = {'label': taxon.label, 'slug': taxon.slug, 'products': []}
  for product in taxon.products:
    toJson[taxon.name]['products'].append({
      'name': product.name,
      'composition': product.composition,
      'coo': product.coo,
      'slug': product.slug,
      'moq': product.moq,
      'oqi': product.oqi,
      'reference': product.reference,
      'price': product.price,
      'variants': []
      })
    for variant in product.variants:
      toJson[taxon.name]['products'][-1]['variants'].append({
        'name': variant.name,
        'sku': variant.sku,
        'barcode': variant.barcode,
        'size': variant.size,
        # 'colour': variant.colour,
        })

print('\n Here:')
print(toJson['envision-clothing']['products'][0]['coo'])

import json
with open("TaxonData.json", "w") as outfile:
    json.dump(toJson, outfile, indent=4)





