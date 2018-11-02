from datetime import datetime as dt
import sqlite3
import time
from typing import List
from typing import Any
from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler


class Reader():
    """
    Continuously reads the database for scheduled operations.
    Returns any scheduled operations that need to be ran.
    """

    def __init__(self) -> None:
        file_path: str = 'postr/schedule/master_schedule.sqlite'
        self.conn = sqlite3.connect(file_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.sched = BackgroundScheduler()

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

    async def start(self) -> None:
        """ Starts a scheduler """
        self.sched.add_job(self.scan, 'interval', seconds=10)
        self.sched.start()

    async def scan(self) -> Any:
        """ Scans every 30 seconds for new jobs in the past 30 seconds """
        time.sleep(30)
        todo = self.scan_custom_jobs()
        print(todo)
        # pass

    def schedule_range(self, seconds: int) -> int:
        """ Returns the lower bound for a scheduled range """
        now = self.now()
        return now - seconds
