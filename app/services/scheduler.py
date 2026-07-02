import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def postar_ofertas_automatico():
    from app.bot.handlers import carregar_ofertas_automatico
    await carregar_ofertas_automatico()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            postar_ofertas_automatico,
            trigger=IntervalTrigger(minutes=30),
            id='post_ofertas',
            replace_existing=True
        )
        scheduler.start()
        logger.info("✅ Scheduler automático iniciado (a cada 30 minutos)")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("⛔ Scheduler parado")

def is_scheduler_running() -> bool:
    return scheduler.running