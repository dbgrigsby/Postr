import time
import asyncio
from datetime import datetime as dt
import os
import sqlite3
from typing import List
from typing import Any
from typing import Dict

from postr.schedule.task_processor import process_scheduler_events


def clean_empty_strings(items: Dict[str, Any]) -> Dict[str, Any]:
    print(f'Items was: {items}')
    return {k: v if not v == '' else None for k, v in items.items()}


class Reader():
    """
    Continuously reads the database for scheduled operations.
    Returns any scheduled operations that need to be ran.
    """

    def __init__(self) -> None:
        file_path: str = os.path.join('postr', 'schedule', 'master_schedule.sqlite')
        self.conn = sqlite3.connect(file_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cleanup(self) -> None:
        """ Closes the database connection"""
        self.conn.close()

    @classmethod
    def now(cls) -> int:
        """ Returns the current time """
        return int(dt.now().timestamp())

    def scan_custom_jobs(self, seconds: int = 30) -> List[Dict[str, Any]]:
        """ Scans jobs every 'seconds' seconds, and returns a JSON
            object representing any jobs to be operated on """
        lower = self.schedule_range(seconds)
        upper = self.now()

        self.cursor.execute(f"""SELECT * FROM CustomJob
                INNER JOIN Job on Job.JobID = CustomJob.Job_ID
                WHERE CustomJob.CustomDate BETWEEN {lower} and {upper}""")

        json = [{
            self.cursor.description[i][0]: value
            for i, value in enumerate(row)
        } for row in self.cursor.fetchall()]

        return json

    async def scan(self) -> Any:
        """ Scans every 30 seconds for new jobs in the past 30 seconds """
        while True:
            time.sleep(10)
            tasks = self.scan_custom_jobs()
            cleaned_tasks = [
                clean_empty_strings(task)
                for task in tasks
            ]
            await process_scheduler_events(cleaned_tasks)

    def run_scheduler(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scan())

    def schedule_range(self, seconds: int) -> int:
        """ Returns the lower bound for a scheduled range """
        now = self.now()
        return now - seconds


if __name__ == '__main__':
    r = Reader()
    r.run_scheduler()
