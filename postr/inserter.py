import sqlite3


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print("connection unestablished")

    return None


def create_person(conn, first, last, social):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Person(FirstName, LastName, SocialMedia)
                VALUES(?, ?, ?)""", (first, last, social),
    )
    conn.commit()


def create_job(conn, comment, media_path, optional_text):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Job(Comment, MediaPath, OptionalText)
                VALUES(?, ?, ?)""", (comment, media_path, optional_text),
    )
    conn.commit()


def create_custom_job(conn, date, job_id):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO CustomJob(CustomDate, Job_ID)
                VALUES(?, ?)""", (date, job_id),
    )
    conn.commit()


def create_bio(conn, use_display, display_first, display_last, age, comment):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Bio (UseDisplayNameInfo, DisplayFirstName,
                Age, Comment, Person_ID) VALUES(?, ?, ?, ?, ?)""",
        (use_display, display_first, display_first, age, comment),
    )
    conn.commit()
