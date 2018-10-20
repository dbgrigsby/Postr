# Using the generic logger for postr
  - How to use it:
      - Stop using print statements!
      - `from .postr_logger import make_logger`
      - `log = make_logger(YOUR_API_HERE)
      - `log.info('some normal message that's a good sign')
      - `log.error('something really bad!!')
  - What this does:
      - Logs everything put into it to a logs folder, and to standard out
      - Has timestamps, the exact module you wre in (including in libraries)
