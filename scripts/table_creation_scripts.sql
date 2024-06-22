CREATE TABLE categories (
    "name" VARCHAR PRIMARY KEY
);

CREATE TABLE questions (
    "id" SERIAL PRIMARY KEY,
    "question" TEXT NOT NULL,
    "answer" TEXT NOT NULL,
    "category" VARCHAR NOT NULL,
    FOREIGN KEY ("category") REFERENCES categories("name")
);

CREATE TABLE players (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR NOT NULL UNIQUE,
    "score" INTEGER DEFAULT 0
);