from app.api.client import ShopeeAPI

api = ShopeeAPI()


def buscar_ofertas(limit=10):

    query = f"""
    {{
      productOfferV2(limit:{limit}) {{
        nodes {{
          productName
          price
          commission
          commissionRate
          sales
          imageUrl
          shopName
          productLink
          offerLink
        }}
      }}
    }}
    """

    return api.execute(query)