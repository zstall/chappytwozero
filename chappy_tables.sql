CREATE TABLE users (
 id INTEGER PRIMARY KEY,
 fname TEXT NOT NULL,
 lname TEXT NOT NULL,
 phone TEXT NOT NULL,
 email TEXT NOT NULL,
 username TEXT NOT NULL,
 password TEXT NOT NULL
);

CREATE TABLE chores (
 id INTEGER PRIMARY KEY,
 chore TEXT NOT NULL,
 schedule TEXT NOT NULL,
 name TEXT,
 done TEXT
);
