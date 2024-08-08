DROP TABLE IF EXISTS questions;

DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR UNIQUE
);

CREATE TABLE questions (
    "id" SERIAL PRIMARY KEY,
    "question" TEXT NOT NULL,
    "answer" TEXT NOT NULL,
    "category" VARCHAR NOT NULL,
    "imageBase64" TEXT,
    FOREIGN KEY ("category") REFERENCES categories("name")
);