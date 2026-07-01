import logging
import re

logger = logging.getLogger(__name__)

def gerar_link_afiliado(link_original: str, subid: str = "ofertabot") -> str:
    try:
        if not link_original or "shopee" not in link_original.lower():
            return link_original
        base = re.split(r'\?', link_original)[0]
        if '?' in link_original:
            return f"{base}&sub_id={subid}"
        else:
            return f"{base}?sub_id={subid}"
    except:
        return link_original