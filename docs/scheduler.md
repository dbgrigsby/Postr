# Example use cases
    - Creating the database
      If you haven't done this, type 'make database' to create the database.
      It is located at postr/schedule/master_schedule.sqlite

    - Seeing jobs in the last 30 seconds
      To see jobs in the last 30 seconds, we can write two jobs, and then immediately scan for jobs.

      To write a job, do 'python -im postr.schedule.writer'
      Then, 'w = Writer()'
      Then, w.example()

      This will write two jobs, 5 seconds apart from each other. It will print 'done!' when finished.

      Next, do 'python -im postr.schedule.reader'
      Then, 'r = Reader()'
      Then, 'r = scan_custom_jobs()'

      This will return a JSON list of all jobs in the last 30 seconds.

      Its default paramater is 30 seconds.
