from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.infrastructure.scheduler.jobs import provider_refresh_job


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler(timezone="UTC")
        self._configured = False

    def start(self) -> None:
        if not self._configured:
            self.scheduler.add_job(provider_refresh_job, "interval", minutes=1, id="provider_refresh")
            self._configured = True
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)


scheduler_service = SchedulerService()
