# create Class for Taxons


def seededKey(seed):
  import random
  import string
  random.seed(seed)
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class Taxon:
  def __init__(self, slug):
    self.name = {
      'en': slug.replace('-', ' ').title()
    }
    self.label = {
      'en': slug.replace('-', ' ').title()
    }
    # generate slug
    self.slug = {
      'en': slug
    }
    # self.description
    self.products = []
    self.id = seededKey('taxon-' + seededKey(slug))
    self.key = seededKey('taxon-' + seededKey(slug))

  def __str__(self) -> str:
    print_string = """
      Taxon:    {name}
      Label:    {label}
      Slug:     {slug}
      ID:       {id}
      Key:      {key}
      Products: {products}
    """
    return print_string.format(
      name=self.name['en'],
      label=self.label['en'],
      slug=self.slug['en'],
      id=self.id,
      key=self.key,
      products=self.products
    )
  def __repr__(self) -> str:
    return self.__str__()

  def addProduct(self, product):
    self.products.append(product)


# Create Class for Products
class Product:
  def __init__(
    self,
    catalog,
    name, 
    slug,
    reference = None,
    price = None,
    composition = "", 
    coo = "", 
    moq = 1,
    oqi = 1,
    barcode = None,
    taxons = None,
    # leadtime,
    ):
    self.name = {
      'en': catalog + " " + name
    }
    self.label = {
      'en': name
    }
    # self.description = {
    # 'en': description
    # }
    self.composition = {
      'en': composition
    }
    self.coo = coo
    self.slug = {
      'en': {
        '_type': 'slug',
        'current': slug
      }
    }
    if moq == -1:
      self.moq = 1
    else:
      self.moq = moq
    if oqi == -1:
      self.oqi = 1
    else:
      self.oqi = int(oqi)
    self.reference = reference
    if barcode is not None:
      self.barcode = barcode
    # self.leadtime = leadtime
    self.variants = []
    if reference is not None:
      self.id = 'product-' + seededKey(self.reference)
      self.key = 'product-' + seededKey(self.reference)
    if (price != None and price != ''):
      for i in range(len(price)):
        try:
          priceNum = float(price)
        except:
          price = price[1:]
          priceNum = -1
        if priceNum > 0.01:
          self.price = int(priceNum*100)
          break
    else:
      self.price = None
    if taxons is not None:
      self.taxons = taxons

  def __str__(self, verbose = True) -> str:
    print_string = """
      Product:                {name}
      Composition:            {composition}
      Country of Origin:      {coo}
      Slug:                   {slug}
      Minimum Order Quantity: {moq}
      Order Increment:        {oqi}
      Reference:              {reference}
      Barcode:                {barcode}
      Price:                  {price}
      ID:                     {id}
      Key:                    {key}
      Variants:               {variants}
    """
    if not verbose:
      print_string = """
        Product:                {name}
      """
    return print_string.format(
      name=self.name['en'],
      composition=self.composition['en'],
      coo=self.coo,
      slug=self.slug['en'],
      moq=self.moq,
      oqi=self.oqi,
      reference=self.reference,
      barcode=self.barcode,
      price=self.price,
      id=self.id,
      key=self.key,
      variants=self.variants
    )
  def __repr__(self) -> str:
    return self.__str__(verbose=True)

  def addVariant(self, variant):
    self.variants.append(variant)

  def Variants2JSON(self):
    # return hashable list of variants
    return [variant.__dict__ for variant in self.variants]
    


class Size():
  def __init__(self, name, size_type = 'Unisex', reference = ""):
    self.name = name
    self.size_type = size_type
    self.id = seededKey('size-' + self.name + self.size_type)
    self.reference = reference

  def __str__(self) -> str:
    gender = ''
    if self.size_type == 'Male':
      gender = 'Male'
    elif self.size_type == 'Female':
      gender = 'Female'
    else:
      gender = 'Unisex'

      
    print_string = """
        Size:      {name}
        Gender:    {type}
        Reference: {reference}
    """

    return print_string.format(
      name=self.name,
      type=self.size_type,
      reference=self.reference
    )

  def __repr__(self) -> str:
    return self.__str__()

  def __eq__(self, o: object) -> bool:
    # assert that o is a Size
    if not isinstance(o, Size):
      return False
    
    # print('Comparing: ', self.name, o.name, self.name == o.name)
    # print('Comparing: ', self.size_type, o.size_type, self.size_type == o.size_type)
    return self.name == o.name and self.size_type == o.size_type

  def generateReference(self):
    self.reference = seededKey('size-' + self.name + self.size_type)


class Color:
  def __init__(self, name, reference = ""):
    self.name = {
      'en': name
    }
    self.id = reference
    self.reference = reference

  def __str__(self) -> str:
    print_string = """
        Color:     {name}
        Reference: {reference}
    """

    return print_string.format(
      name=self.name,
      reference=self.reference
    )

  def __repr__(self) -> str:
    return self.__str__()

  def __eq__(self, o: object) -> bool:
    # assert that o is a Color
    if not isinstance(o, Color):
      return False
    return self.name == o.name

# Create Class for Variants
class Variant:
  def __init__(
    self,
    name, # [Product Name] ([size] [colour])
    sku,
    barcode,
    # lead_time,
    size = Size("One Size", "Unisex"), 
    colour = None,
    composition = ""
    ):
    self.sku = sku
    self.barcode = barcode
    self.leadttime = ""
    self.description = {
      'en': ""
    }
    self.composition = {
      'en': composition
    }
    self.size = size # this is normally a reference to a size object
    # self.colour = # reference to colour object
    self.name = {
      'en': name 
    }
    self.id = seededKey('variant-' + self.sku)
    self.key = 'variant-' + seededKey(self.sku)

  def __str__(self) -> str:
    print_string = """
         Variant:     {name}
         SKU:         {sku}
         Barcode:     {barcode}
         Composition: {composition}
         Size:        {size}
         ID:          {id}
         Key:         {key}
    """
    return print_string.format(
      sku=self.sku,
      barcode=self.barcode,
      description=self.description['en'],
      composition=self.composition['en'],
      size=self.size,
      name=self.name['en'],
      id=self.id,
      key=self.key
    )
  def __repr__(self) -> str:
    return self.__str__()

  def __dict__(self) -> dict:
    return {
      'id': self.id,
      'key': self.key,
    }


  def setComposition(self, composition):
    self.composition = {
      'en': composition
    }


class SKU:
  def __init__(self, sku, price, name):
      self.sku = sku
      # check price is an integer or reject the init
      if isinstance(price, int):
        self.price = price
      else:
        self.price = None
        print('Price must be an integer')
      self.name = name
      self.id = seededKey('sku-' + self.sku)
      self.skuId = ''
      self.priceId = ''
  def setPriceId(self, priceId):
      self.priceId = priceId
    
  def setSkuId(self, skuId):
      self.skuId = skuId
  def __str__(self):
      return f'{self.sku} {self.price} {self.name}'
