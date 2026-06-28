# app/services/scheduler_service.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def agendar_tarefa(self, func, tempo_segundos, *args):
        """Agenda uma função para rodar após X segundos."""
        self.scheduler.add_job(func, 'interval', seconds=tempo_segundos, args=args, max_instances=1)
        print(f"✅ Tarefa agendada para rodar a cada {tempo_segundos} segundos.")

    def start(self):
        self.scheduler.start()