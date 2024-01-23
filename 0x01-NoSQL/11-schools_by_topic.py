#!/usr/bin/env python3
"""
A module that lists where can I learn Python
"""


def schools_by_topic(mongo_collection, topic):
    """function that returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})
