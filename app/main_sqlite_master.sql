INSERT INTO main.sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'platform', 'platform', 2, 'CREATE TABLE platform (
	id INTEGER NOT NULL, 
	api_id INTEGER, 
	created_at DATETIME, 
	name VARCHAR(80), 
	summary TEXT, 
	generation INTEGER, 
	image VARCHAR(128), 
	website VARCHAR(80), 
	PRIMARY KEY (id)
)');
INSERT INTO main.sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'studio', 'studio', 3, 'CREATE TABLE studio (
	id INTEGER NOT NULL, 
	name VARCHAR(256), 
	platform_id INTEGER, 
	logo VARCHAR(256), 
	description TEXT, 
	created_at DATETIME, 
	website VARCHAR(256), 
	PRIMARY KEY (id), 
	FOREIGN KEY(platform_id) REFERENCES platform (id)
)');
INSERT INTO main.sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'game', 'game', 4, 'CREATE TABLE game (
	id INTEGER NOT NULL, 
	name VARCHAR(256), 
	api_id INTEGER, 
	summary TEXT, 
	genre VARCHAR(256), 
	rating FLOAT, 
	storyline TEXT, 
	category VARCHAR(256), 
	esrb VARCHAR(256), 
	status VARCHAR(256), 
	platform_id INTEGER, 
	studio_id INTEGER, 
	video VARCHAR(256), 
	image VARCHAR(256), 
	release_date DATETIME, 
	website VARCHAR(256), 
	PRIMARY KEY (id), 
	FOREIGN KEY(platform_id) REFERENCES platform (id), 
	FOREIGN KEY(studio_id) REFERENCES studio (id)
)');
INSERT INTO main.sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'reviews', 'reviews', 7, 'CREATE TABLE reviews (
	id INTEGER NOT NULL, 
	title VARCHAR(256), 
	platform_id INTEGER, 
	game_id INTEGER, 
	created_at DATETIME, 
	views INTEGER, 
	video VARCHAR(256), 
	introduction TEXT, 
	content TEXT, 
	conclusion TEXT, 
	positive TEXT, 
	negative TEXT, 
	url VARCHAR(256), 
	PRIMARY KEY (id), 
	FOREIGN KEY(platform_id) REFERENCES platform (id), 
	FOREIGN KEY(game_id) REFERENCES game (id)
)');
