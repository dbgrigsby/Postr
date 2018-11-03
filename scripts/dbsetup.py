import sqlite3

file_path: str = 'postr/schedule/master_schedule.sqlite'

conn = sqlite3.connect(file_path)
c = conn.cursor()

# Define Job, the main driver of all scheduling tasks
c.execute("""CREATE TABLE Job(
        JobID INTEGER PRIMARY KEY AUTOINCREMENT,
        Comment TEXT,
        MediaPath TEXT,
        OptionalText TEXT,
        Platforms TEXT,
        Action TEXT
        )""")

# Define a generic bio
c.execute("""CREATE TABLE Bio (
        BioID INTEGER PRIMARY KEY AUTOINCREMENT,
        UseDisplayNameInfo INTEGER NOT NULL,
        DisplayFirstName TEXT,
        DisplayLastName TEXT,
        Age INTEGER NOT NULL,
        Comment TEXT,
        Website TEXT,
        Person_ID INTEGER NOT NULL,
        FOREIGN KEY (Person_ID) REFERENCES Person(PersonID) ON DELETE CASCADE
        )""")

# Define a person
c.execute("""CREATE TABLE Person (
        PersonID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        SocialMedia TEXT NOT NULL
        )""")

# Create storage for daily jobs
c.execute("""CREATE TABLE DailyJob (
        DailyJobID INTEGER PRIMARY KEY AUTOINCREMENT,
        Frequency INTEGER DEFAULT 1,
        FrequencyCounter INTEGER DEFAULT 1,
        IntervalInMinutes INTEGER DEFAULT 0,
        StartTime INTEGER NOT NULL,
        EndTime INTEGER,
        Job_ID INTEGER NOT NULL,
        FOREIGN KEY (Job_ID) REFERENCES Job(JobID) ON DELETE CASCADE
        )""")

# Create storage for monthly jobs
c.execute("""CREATE TABLE MonthlyJob (
        MonthlyJobID INTEGER PRIMARY KEY AUTOINCREMENT,
        Frequency INTEGER DEFAULT 1,
        FrequencyCounter INTEGER DEFAULT 1,
        IntervalInDays INTEGER DEFAULT 0,
        StartTime INTEGER NOT NULL,
        EndTime INTEGER,
        Job_ID INTEGER NOT NULL,
        FOREIGN KEY (Job_ID) REFERENCES Job(JobID) ON DELETE CASCADE
        )""")

c.execute("""CREATE TABLE CustomJob (
        CustomJobID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomDate INTEGER NOT NULL,
        Job_ID INTEGER NOT NULL,
        FOREIGN KEY (Job_ID) REFERENCES Job(JobID) ON DELETE CASCADE
        )""")

conn.commit()
conn.close()
