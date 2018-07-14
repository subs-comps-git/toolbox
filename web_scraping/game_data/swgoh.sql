--swgoh.sql
--Schema for swgoh GP data


DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gp;


CREATE TABLE users (
    uid     integer PRIMARY KEY AUTOINCREMENT,
    name    text NOT NULL,
    CONSTRAINT name_constraint UNIQUE (name)
);

CREATE TABLE gp (
    gid         integer PRIMARY KEY AUTOINCREMENT,
    u_id        integer NOT NULL,
    dl_date     integer NOT NULL,
    total_gp    integer NOT NULL,
    char_gp     integer NOT NULL,
    ship_gp     integer NOT NULL,
    FOREIGN KEY(u_id) REFERENCES users(uid)
);

