INSERT INTO categories (name)
VALUES 
    ('Astronomy'),
	('Biology'),
	('Chemistry'),
	('Geology'),
	('Computer Science');

INSERT INTO questions (question, answer, category)
VALUES 
    ('What is the sun?', 'A star', 'Astronomy'),
	('What are the names of the planets in the solar system?', 'Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune', 'Astronomy'),
	('What does DNA stand for?', 'Deoxyribonucleic acid', 'Biology'),
	('What is a cell?', 'A cell is the smallest unit of life of all living organisms', 'Biology'),
	('What charge does a proton have?', 'Positive charge', 'Chemistry'),
	('What charge does an electron have?', 'Negative charge', 'Chemistry'),
	('What is the outermost layer of the Earth?', 'The crust', 'Geology'),
	('What are the three types of plate boundaries?', 'Divergent, convergent, and transform', 'Geology'),
	('What does the acronym "HTTP" stand for in web addresses?', 'HyperText Transfer Protocol', 'Computer Science'),
	('What does the "CPU" stand for', 'Central Proccessing Unit', 'Computer Science');