from datetime import datetime as dt
import sqlite3


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
