# СТоронние бибилиотеки
import logging
import traceback


class Logger(object):
    """
    Запись ошибок в файл logger.log
    """
    def __init__(self):
        self.logger = logging.getLogger('logger')

        console_handler_log = logging.StreamHandler()
        file_handler_log = logging.FileHandler('logger.log')
        console_handler_log.setLevel(logging.DEBUG)
        file_handler_log.setLevel(logging.ERROR)

        console_format_log = logging.Formatter('%(message)s')
        file_format_log = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n'
                                            '-----------------------------------------------------------------------')

        console_handler_log.setFormatter(console_format_log)
        file_handler_log.setFormatter(file_format_log)

        self.logger.addHandler(console_handler_log)
        self.logger.addHandler(file_handler_log)

    def error(self):
        self.logger.error('Ошибка:\n{}'.format(traceback.format_exc()))

    def warning(self):
        self.logger.warning('Ошибка записана в файл logger.log')





