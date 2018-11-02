from datetime import datetime as dt
import sqlite3
from typing import List
from typing import Any


class Reader():
    """
    Continuously reads the database for scheduled operations.
    Returns any scheduled operations that need to be ran.
    """

    def __init__(self) -> None:
        file_path: str = 'postr/schedule/master_schedule.sqlite'
        self.conn = sqlite3.connect(file_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cleanup(self) -> None:
        """ Closes the database connection"""
        self.conn.close()

    @classmethod
    def now(cls) -> int:
        """ Returns the current time """
        return int(dt.now().timestamp())

    def scan_custom_jobs(self, seconds: int = 30) -> List[Any]:
        """ Scans jobs every 'seconds' seconds, and returns a JSON
            object representing any jobs to be operated on """
        lower = self.schedule_range(seconds)
        upper = self.now()

        self.cursor.execute(f"""SELECT * FROM CustomJob WHERE
                CustomJob.CustomDate BETWEEN {lower} and {upper}""")

        json = [{
            self.cursor.description[i][0]: value
            for i, value in enumerate(row)
        } for row in self.cursor.fetchall()]

        return json

    def schedule_range(self, seconds: int) -> int:
        """ Returns the lower bound for a scheduled range """
        now = self.now()
        return now - seconds
