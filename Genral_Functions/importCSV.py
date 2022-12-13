# import csvfile and extract data using set of rules outlined below

import pandas as pd
from sympy import Q

from uncommonClasses import Product, Size, Taxon, Variant

# import numpy as np
# from sanity_connect import AllTaxons

# CATALOGNAME = "ENV"
CATALOGNAME = "TCS"

def checkForTBC(string):
  if (string == 'TBC' or string == '' or string == False):
    return ''
  else:
    return str(string)

def makeInt(stringOrFloat):
  # print(stringOrFloat)
  if (pd.isna(stringOrFloat) or stringOrFloat == 'nan'):
    return -1
  else:
    # make into string
    string = str(stringOrFloat)
    # split by decimal point
    string = string.split('.')
    return int(string[0])
  

def generateTaxonObjects(inputCSV):
  # Read CSV file
  product_upload_df = pd.read_csv(inputCSV)


  # Find Unique Taxons
  unique_taxons = product_upload_df['Taxons'].dropna().unique()
  # print the length of the unique taxons
  print("Number of unique taxons: ", len(unique_taxons))
  
  # create taxon objects
  taxon_objects = []
  for taxon in unique_taxons:
    taxon_objects.append(Taxon(taxon))

  # return AllTaxons
  return taxon_objects


def generateProductObjects(inputCSV):
  # Read CSV file
  product_upload_df = pd.read_csv(inputCSV)

  # Split df into Products and Variants
  unique_products = product_upload_df[product_upload_df['Type'] == 'Product']['Product Name'].dropna().unique()
  # print the length of the unique products 
  print("Number of unique products: ", len(unique_products))
  
  
  
  product_objects = []
  for product in unique_products:
    # check if has SKU
    hasVariant = False
    ref = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na = False), 'Product SKU'].iloc[0]
    if not pd.isna(ref):
      ref = str(ref)
    else:
      ref = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na = False), 'Product SKU'].iloc[1]
      hasVariant = True
    
    bar = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na = False), 'Barcode EAN'].iloc[0]
    if not pd.isna(bar):
      bar = str(bar)
    else:
      bar = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na = False), 'Barcode EAN'].iloc[1]
 
    # print(comp)
    product = Product(
      # Name
      CATALOGNAME,
      product,
      # Slug
      (CATALOGNAME.lower() + "-" + product.lower()) .replace(' ', '-'),
      # Reference - note that this will be 'P-' + the first variant sku 
      reference = 'P-' + ref,
      price = checkForTBC(product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na = False), 'Price'].iloc[0]),
      composition = checkForTBC(product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na=False), 'Composition'].iloc[0]),
      coo = checkForTBC(product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na=False), 'COO'].iloc[0]),
      moq = makeInt(checkForTBC(product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na=False), 'MOQ'].iloc[0])),
      oqi = makeInt(checkForTBC(product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na=False), 'OQI'].iloc[0])),
      barcode = makeInt(bar),
      taxons = product_upload_df.loc[product_upload_df['Product Name'].str.contains(product, na=False), 'Taxons'].iloc[0],
    )
    if not hasVariant:
      variant = Variant(
        # Name
        product.name['en'],
        # SKU
        ref,
        # Barcode
        makeInt(bar),
      )
      product.addVariant(variant)
    product_objects.append(product)
    
  return product_objects

def checkType(string):
  if "Men" in string:
    return "Male"
  elif "Women" in string:
    return "Female"
  else:
    return "Unisex"

def generateVariantObjects(inputCSV):
  # Read CSV file
  product_upload_df = pd.read_csv(inputCSV)


  # unique variants
  unique_variants = product_upload_df[product_upload_df['Type'] == 'Variant']['Product SKU']
  # print the length of the unique variants
  print("Number of unique variants: ", len(unique_variants))

  variant_objects = []
  for variant in unique_variants:
    # print(variant)
    product_name = product_upload_df.loc[product_upload_df['Product SKU'].str.contains(variant, na=False), 'Product Name'].iloc[0]
    
    size = product_upload_df.loc[product_upload_df['Product SKU'].str.contains(variant, na=False), 'Size'].iloc[0]
    if pd.isna(size):
      size = ''
    else:
      size = str(size)
    
    # colour = product_upload_df.loc[product_upload_df['Product SKU'].str.contains(variant, na=False), 'Colour'].iloc[0]
    # if pd.isna(colour):
    #   colour = ''
    # else:
    #   colour = str(colour)

    
    variant_name = CATALOGNAME + " " + product_name + ' (' + size + ')'
    # print(variant_name)

    variant = Variant(
      # Name
      variant_name,
      # SKU
      variant,
      # Barcode
      makeInt(product_upload_df.loc[product_upload_df['Product SKU'].str.contains(variant, na=False), 'Barcode EAN'].iloc[0]),
      # size
      size=Size(size, size_type = checkType(product_name)),
      #composition
      composition = checkForTBC(product_upload_df.loc[product_upload_df['Product SKU'].str.contains(variant, na=False), 'Composition'].iloc[0]),
    )
    variant_objects.append(variant)    
  return variant_objects


def combineObjects(taxon_objects, product_objects, variant_objects):
  # add variants to products
  for taxon in taxon_objects:
    for product in product_objects:
      if taxon.slug['en'] in product.taxons:
        for variant in variant_objects:
          if variant.name['en'].lower().find(product.name['en'].lower()) != -1:
              # print("Adding variant: ", variant.name['en'], " to product: ", product.name['en'])
              product.addVariant(variant)
        taxon.addProduct(product)

  # add products to taxons
  for taxon in taxon_objects:
    for product in product_objects:
      if taxon.slug['en'] in product.taxons:
        taxon.addProduct(product)
  
  return taxon_objects
  
def importTaxons(CSVPath):
  AllTaxons = generateTaxonObjects(CSVPath)
  # print("first taxon: ")
  # print(AllTaxons[0])
  AllProducts = generateProductObjects(CSVPath)
  # print("first product: ")
  # print(AllProducts[0])
  AllVariants = generateVariantObjects(CSVPath)
  # print("first variant: ")
  # print(AllVariants[0])
  AllTaxons = combineObjects(AllTaxons, AllProducts, AllVariants)
  return AllTaxons

if __name__ == "__main__":
  AllTaxons = generateTaxonObjects('TCS1.csv')
  # print("first taxon: ")
  # print(AllTaxons[0])
  AllProducts = generateProductObjects('TCS1.csv')
  # print("first product: ")
  # print(AllProducts[0])
  AllVariants = generateVariantObjects('TCS1.csv')
  # print("first variant: ")
  # print(AllVariants[2])
  AllTaxons = combineObjects(AllTaxons, AllProducts, AllVariants)
  print("first taxon: ")
  print(AllTaxons[0].products[0])
  print("second taxon: ")
  print(AllTaxons[1].products[0])
  # print(AllTaxons[1].products)
