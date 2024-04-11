#!/usr/bin/env python3
"""
Module for the filter_datum function.
"""
import logging
import mysql
import mysql.connector
from mysql.connector.connection import MySQLConnection
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password",)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return an obfuscated log message """
    for field in fields:
        message = re.sub(r'{}=.*?{}'.format(field, separator),
                         r'{}={}{}'.format(field, redaction, separator),
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Method that filters values in incoming log records """
        record.msg = filter_datum(list(self.fields), self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ returns a Logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """ returns a object connector to the database """
    config = {
        'user': os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        'password': os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        'host': os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': os.getenv("PERSONAL_DATA_DB_NAME")
    }
    conn = mysql.connector.connect(**config)
    return conn


def main() -> None:
    """ main entry point. """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    fields = ["name", "email", "password", "ssn", "phone"]
    logger = get_logger()
    for row in cursor:
        msg = "; ".join("{}={}".format(k, v) for k, v in zip(fields, row))
        logger.info(msg=msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
