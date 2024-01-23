#!/usr/bin/env python3
"""
that lists all documents in a collection
"""


def list_all(mongo_collection):
    """Return an empty list if no document in the collection"""
    doc = mongo_collection.find()
    return doc
