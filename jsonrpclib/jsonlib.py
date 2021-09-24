#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Loads the "best" Python library available for the current interpreter and
provides a single interface for all
"""

import json
import sys


PYTHON_2 = sys.version_info[0] < 3


class JsonHandler(object):
    """
    Parent class for JSON handlers
    """

    def get_methods(self):
        """
        Returns the loads and dumps methods
        """
        if PYTHON_2:
            # We use the Py2 API with an encoding argument
            return json.loads, json.dumps

        def dumps_py3(obj, encoding="utf-8"):
            return json.dumps(obj)

        return json.loads, dumps_py3


class CJsonHandler(JsonHandler):
    """
    Handler based on cjson
    """

    def get_methods(self):
        import cjson

        def dumps_cjson(obj, encoding="utf-8"):
            return cjson.encode(obj)

        return cjson.decode, dumps_cjson


class SimpleJsonHandler(JsonHandler):
    """
    Handler based on simplejson
    """

    def get_methods(self):
        import simplejson

        return simplejson.loads, simplejson.dumps


class UJsonHandler(JsonHandler):
    """
    Handler based on ujson
    """

    def get_methods(self):
        import ujson

        print("ujson-jsonlib:", id(ujson))

        def dumps_ujson(obj, encoding="utf-8"):
            return ujson.dumps(obj)

        print("jsonlib:", ujson.loads)
        return ujson.loads, dumps_ujson


def get_handler():
    # type: () -> JsonHandler
    """
    Returns the best available Json parser
    """
    for handler_class in (UJsonHandler, SimpleJsonHandler, CJsonHandler):
        handler = handler_class()
        try:
            loader, dumper = handler.get_methods()
        except ImportError:
            # Library is missing
            pass
        else:
            try:
                # Check if the library really works
                loader(dumper({"answer": 42}))
                break
            except Exception:
                pass
    else:
        handler = JsonHandler()

    return handler


def get_handler_methods():
    """
    Returns the load and dump methods of the best Json handler
    """
    return get_handler().get_methods()