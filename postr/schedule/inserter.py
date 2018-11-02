""" Inserts rows into the database tables regarding scheduling operations """
import sqlite3
from sqlite3 import Connection
from typing import Optional


def create_connection(db_file: str) -> Optional[Connection]:
    """Creates and returns a connection to a given database file """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception:
        print('connection unestablished')

    return None


def create_person(conn: Connection, first: str, last: str, social: str) -> None:
    """Inserts a person/user into the database Person table; generates a unique ID """
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Person(FirstName, LastName, SocialMedia)
                VALUES(?, ?, ?)""", (first, last, social),
    )
    conn.commit()


def create_job(conn: Connection, comment: str, media_path: str, optional_text: str) -> None:
    """Creates a scheduled job/task for media operations.
       comment and media path can be null """
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Job(Comment, MediaPath, OptionalText)
                VALUES(?, ?, ?)""", (comment, media_path, optional_text),
    )
    conn.commit()


def create_custom_job(conn: Connection, date: str, job_id: str) -> None:
    """Creates a custom job/task, that is, a one-time job on a specific date """
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO CustomJob(CustomDate, Job_ID)
                VALUES(?, ?)""", (date, job_id),
    )
    conn.commit()


def create_bio(
        conn: Connection,
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
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Bio (UseDisplayNameInfo, DisplayFirstName,
                DisplayLastName, Age, Comment, Website, Person_ID) VALUES(?, ?, ?, ?, ?, ?)""",
        (use_display, display_first, display_last, age, comment, website, person_id),
    )
    conn.commit()
