DROP TABLE IF EXISTS saved_game_states;

CREATE TABLE saved_game_states (
    "id" SERIAL PRIMARY KEY, -- game id
    "playerPositions" JSONB NOT NULL, -- '{"player1": [1, 2], "player2": [1, 3]}'
	"playerScores" JSONB NOT NULL, -- '{"player1": {"c1":"_","c2":"_","c3":"_","c4":"_"}, "player2": {"c1":"_","c2":"_","c3":"_","c4":"_"}}'
	"setupInfo" JSONB NOT NULL,
	"currentPlayerIndex" INT NOT NULL,
	"date" TIMESTAMP NOT NULL
);