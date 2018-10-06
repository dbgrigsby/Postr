import sqlite3
from sqlite3 import Connection
from typing import Optional


def create_connection(db_file: str) -> Optional[Connection]:
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception:
        print('connection unestablished')

    return None


def create_person(conn: Connection, first: str, last: str, social: str) -> None:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Person(FirstName, LastName, SocialMedia)
                VALUES(?, ?, ?)""", (first, last, social),
    )
    conn.commit()


def create_job(conn: Connection, comment: str, media_path: str, optional_text: str) -> None:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Job(Comment, MediaPath, OptionalText)
                VALUES(?, ?, ?)""", (comment, media_path, optional_text),
    )
    conn.commit()


def create_custom_job(conn: Connection, date: str, job_id: str) -> None:
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
) -> None:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Bio (UseDisplayNameInfo, DisplayFirstName,
                Age, Comment, Person_ID) VALUES(?, ?, ?, ?, ?)""",
        (use_display, display_first, display_first, age, comment),
    )
    conn.commit()
