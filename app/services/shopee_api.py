import logging
import aiohttp
import json
from typing import List, Dict

logger = logging.getLogger(__name__)

class ShopeeAPI:
    GRAPHQL_URL = "https://open-api.affiliate.shopee.com.br/graphql"
    
    def __init__(self):
        self.session = None

    async def get_products(self, limit: int = 20, category: str = None) -> List[Dict]:
        """Busca produtos da Shopee via GraphQL"""
        query = """
        query {
          search_products(
            keyword: "",
            limit: %d,
            sort_by: "pop",
            order_by: "desc"
          ) {
            items {
              item_id
              name
              price
              original_price
              discount
              image
              shop_id
              url
            }
          }
        }
        """ % limit

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.GRAPHQL_URL,
                    json={"query": query}
                ) as resp:
                    data = await resp.json()
                    products = data.get("data", {}).get("search_products", {}).get("items", [])
                    logger.info(f"✅ {len(products)} produtos obtidos da Shopee")
                    return products
        except Exception as e:
            logger.error(f"Erro na API Shopee: {e}")
            return []