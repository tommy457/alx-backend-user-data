#!/usr/bin/env python3
"""
Module for the filter_datum function.
"""
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
