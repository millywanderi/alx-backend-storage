#!/usr/bin/env python3
"""A script that provides some stats about Nginx logs"""
from pymongo import MongoClient


def printing_nginx_log_stats(log_collection):
    """Printing Nginx log stats"""
    print(f"{log_collection.count_document({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        log_count = len(list(log_collection.find({"method": method})))
        print(f"\tmethod {method}: {log_count}")
    status_count = len(list(
        log_collection.find({"method": "GET", "path": "/status"})
    ))
    print(f"{status_count} status check")


def main():
    """Prints Nginx stats log in Mongo database"""
    client = MongoClient("mongodb://127.0.0.1:27017")
    printing_nginx_log_stats(client.logs.nginx)


if __name__ == "__main__":
    main()
