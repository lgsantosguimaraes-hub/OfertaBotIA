import logging
import re

logger = logging.getLogger(__name__)

def gerar_link_afiliado(link_original: str, subid: str = "ofertabot") -> str:
    """Converte link da Shopee em link de afiliado."""
    try:
        if not link_original or "shopee" not in link_original.lower():
            return link_original

        # Limpa parâmetros existentes
        base = re.split(r'\?', link_original)[0]
        
        # Adiciona parâmetros de afiliado
        if '?' in link_original:
            link_afiliado = f"{base}&sub_id={subid}"
        else:
            link_afiliado = f"{base}?sub_id={subid}"

        logger.info(f"Afiliado gerado: {link_afiliado}")
        return link_afiliado
    except Exception as e:
        logger.warning(f"Falha ao gerar afiliado: {e}")
        return link_original