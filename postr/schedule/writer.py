from datetime import datetime as dt
import sqlite3
import time


class Writer():
    """
    Inserts rows into the database tables regarding scheduling
    operations
    """

    def __init__(self) -> None:
        file_path: str = 'postr/schedule/master_schedule.sqlite'
        self.conn = sqlite3.connect(file_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def cleanup(self) -> None:
        """ Closes the database connection"""
        self.conn.close()

    @classmethod
    def now(cls) -> dt:
        """ Returns the current time """
        return dt.now()

    def create_person(self, first: str, last: str, social: str) -> str:
        """Inserts a person/user into the database Person table; generates a unique ID """
        self.cursor.execute(
            """INSERT INTO Person(FirstName, LastName, SocialMedia)
                    VALUES(?, ?, ?)""", (first, last, social),
        )
        self.conn.commit()

        # return the autoincrement ID
        return str(self.cursor.lastrowid)

    def create_job(self, comment: str, media_path: str, optional_text: str) -> str:
        """Creates a scheduled job/task for media operations.
           comment and media path can be null """
        self.cursor.execute(
            """INSERT INTO Job(Comment, MediaPath, OptionalText)
                    VALUES(?, ?, ?)""", (comment, media_path, optional_text),
        )
        self.conn.commit()

        # return the autoincrement ID
        return str(self.cursor.lastrowid)

    def create_custom_job(self, date: str, job_id: str) -> None:
        """Creates a custom job/task, that is, a one-time job on a specific date """
        self.cursor.execute(
            """INSERT INTO CustomJob(CustomDate, Job_ID)
                    VALUES(?, ?)""", (date, job_id),
        )
        self.conn.commit()

    def create_bio(
            self,
            use_display: bool,
            display_first: str,
            display_last: str,
            age: int,
            comment: str,
            website: str,
            person_id: int,
    ) -> None:
        """ Creates a Bio for an associated user on a given platform
            Used to store all saved users' bios, and can be used to retrieve any user
            bio that meets a certain condition (e.g. contains a specific handle) """
        self.cursor.execute(
            """INSERT INTO Bio (UseDisplayNameInfo, DisplayFirstName,
                    DisplayLastName, Age, Comment, Website, Person_ID) VALUES(?, ?, ?, ?, ?, ?)""",
            (use_display, display_first, display_last, age, comment, website, person_id),
        )
        self.conn.commit()

    def example(self) -> None:
        """ Inserts two times for custom jobs """
        now1 = str(dt.now())
        id1 = self.create_job('testComment1', 'testPath1', '')
        self.create_custom_job(now1, id1)

        time.sleep(5)

        now2 = str(dt.now())
        id2 = self.create_job('testComment2', 'testPath2', '')
        self.create_custom_job(now2, id2)

        print('done!')
