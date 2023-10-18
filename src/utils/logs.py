import logging.handlers

my_logger = logging.getLogger('all_logs')
my_logger.setLevel(logging.INFO)


handler_file = logging.handlers.RotatingFileHandler('my_blog.log', mode='a', maxBytes=1024*10, backupCount=10)
handler_file.setLevel(logging.DEBUG)

handler_console = logging.StreamHandler()
handler_console.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s | %(funcName)s] %(message)s')

handler_file.setFormatter(formatter)
handler_console.setFormatter(formatter)

my_logger.addHandler(handler_file)
my_logger.addHandler(handler_console)
