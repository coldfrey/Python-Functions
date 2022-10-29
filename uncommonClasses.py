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
