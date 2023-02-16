import os, sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, "..")))

import cv2
import numpy as np
import sqlite3
from tools.utils import (
    cosine_similarity,
    Embedded,
    parse_text_from_html,
    load_vector_from_path_db,
)


data_path = "data/HIME.db"
embedded = Embedded()


def query_thing(query):
    result = []
    sqliteConnection = None

    try:
        sqliteConnection = sqlite3.connect("./data/HIME.db")

        cursor = sqliteConnection.execute(query)
        for row in cursor:
            result.append(row)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return result


def get_baihoc(id=None):
    query = "SELECT * from BAI_HOC"

    if id != None:
        query = query + " WHERE ID_BAIHOC = " + id

    return query_thing(query)


def get_story(id=None):
    query = "SELECT * from STORY"

    if id != None:
        query = query + " WHERE ID_Content = " + id

    return query_thing(query)


def get_relative_lesson(image):
    query_vec = embedded.get_vector(image)
    table = []
    sqliteConnection = None
    rs = []
    try:
        sqliteConnection = sqlite3.connect("./data/HIME.db")
        query = "SELECT * from IMAGINE"
        cursor = sqliteConnection.execute(query)
        data = cursor.fetchall()
        for row in data:
            db_vec = load_vector_from_path_db(row[3])
            score = cosine_similarity(db_vec, query_vec)
            table.append(score)

        min_value = min(table)
        min_index = table.index(min_value)

        rs = data[min_index]

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return rs