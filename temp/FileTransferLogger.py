import logging


class FileTransferLogger:
    def __init__(self, log_file_path):
        # Loglama ayarları
        logging.basicConfig(filename=log_file_path, level=logging.INFO)
        self.logger = logging.getLogger("file_transfer_logger")

    def log_activity(self, message):
        # Uygulama içindeki etkinlikleri logla
        self.logger.info(message)

    def log_error(self, error_message):
        # Hataları logla
        self.logger.error(error_message)
