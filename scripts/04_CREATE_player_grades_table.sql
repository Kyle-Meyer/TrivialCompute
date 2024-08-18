DROP TABLE IF EXISTS player_grades;

CREATE TABLE player_grades (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL,
	"category" VARCHAR NOT NULL,
	"grade" INT NOT NULL,
	"date" TIMESTAMP NOT NULL
);