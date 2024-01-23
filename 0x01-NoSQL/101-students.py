#!/usr/bin/env python3
"""
Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Python function that returns all students sorted by average score
    where mongo_collection will be the pymongo collection object
    """
    return mongo_collection.aggregate([
        {
            "$project":
            {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
            {
                "averageScore": -1
            }
        }
    ])
