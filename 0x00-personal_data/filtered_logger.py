#!/usr/bin/env python3
"""
Module for the filter_datum function.
"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return an obfuscated log message """
    for field in fields:
        message = re.sub(r'{}=.*{}'.format(field, separator),
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
