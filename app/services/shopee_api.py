import logging
import aiohttp
import os
from typing import List, Dict

logger = logging.getLogger(__name__)

class ShopeeAPI:
    GRAPHQL_URL = "https://open-api.affiliate.shopee.com.br/graphql"

    def __init__(self):
        self.partner_id = os.getenv("SHOPEE_PARTNER_ID")
        self.token = os.getenv("SHOPEE_AFFILIATE_TOKEN")

    async def get_products(self, limit: int = 10) -> List[Dict]:
        if not self.partner_id or not self.token:
            logger.error("Credenciais Shopee não configuradas!")
            return []

        query = """
        query {
          productOfferV2(
            listType: 0,
            sortType: 5,
            limit: %d
          ) {
            nodes {
              itemId
              productName
              price
              originalPrice
              commissionRate
              offerLink
              productLink
              image
              discount
            }
          }
        }
        """ % limit

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Partner-Id": self.partner_id
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.GRAPHQL_URL,
                    json={"query": query},
                    headers=headers
                ) as resp:
                    data = await resp.json()
                    nodes = data.get("data", {}).get("productOfferV2", {}).get("nodes", [])
                    logger.info(f"✅ {len(nodes)} produtos obtidos")
                    return nodes
        except Exception as e:
            logger.error(f"Erro na API Shopee: {e}")
            return []