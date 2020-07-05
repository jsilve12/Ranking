CREATE TABLE activity(
  id INT PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  UNIQUE (name)
);

CREATE TABLE season(
  id INT PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  activity_id INT REFERENCES activity(id) NOT NULL,
  UNIQUE(name)
);

CREATE TABLE team(
  id INT PRIMARY KEY NOT NULL,
  name TEXT,
  activity INT REFERENCES activity(id) NOT NULL,
  elo REAL,
  glicko REAL,
  glicko_time INT,
  side_1 REAL,
  side_2 REAL,
  UNIQUE (name, season)
);

CREATE TABLE season_team(
  season_id INT REFERENCES season(id) NOT NULL,
  team_id INT REFERENCES team(id) NOT NULL
);

CREATE TABLE tournament(
  id INT PRIMARY KEY NOT NULL,
  season_id INT NOT NULL,
  occured_date date
);

CREATE TABLE round(
  id INT PRIMARY KEY NOT NULL,
  tournament_id INT REFERENCES tournament(id),
  team_1 INT REFERENCES team(id) NOT NULL,
  team_2 INT REFERENCES team(id) NOT NULL,
  result REAL NOT NULL,
  rounds REAL NOT NULL,
  team_1_elo_change REAL NOT NULL,
  team_2_elo_change REAL NOT NULL
);
