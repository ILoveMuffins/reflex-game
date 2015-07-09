#!/usr/bin/env python

import sqlite3
conn = sqlite3.connect('scores.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE Scores
             (ID integer primary key autoincrement , Nick text, CorrectAns
             integer,
             AllAns integer, Score integer)''')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

