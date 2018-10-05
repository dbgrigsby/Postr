import sqlite3

file_path = '../Postr/postr/master_schedule.sqlite'

conn = sqlite3.connect(file_path)
c = conn.cursor()

# Define Job, the main driver of all scheduling tasks
c.execute("""CREATE TABLE Job (
        JobID INTEGER PRIMARY KEY AUTOINCREMENT,
        Comment TEXT NOT NULL,
        MediaPath TEXT
        )""")

# create storage for daily jobs
c.execute("""CREATE TABLE DailyJob (
        Frequency INTEGER DEFAULT 1,
        FrequencyCounter INTEGER DEFAULT 1,
        IntervalInMinutes INTEGER DEFAULT 0,
        StartTime TEXT NOT NULL,
        EndTime TEXT,
        ID INTEGER NOT NULL,
        FOREIGN KEY (ID) REFERENCES Job(JobID) ON DELETE CASCADE
        )""")

conn.commit()
conn.close()
