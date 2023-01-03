# **GAME LIBRARY DATABASE SCHEMA**

## Game Table

```sql

CREATE TABLE game (
    game_id NUMBER(5) CONSTRAINT game_pk PRIMARY KEY,
    game_title VARCHAR2(255) NOT NULL,
    add_at DATE DEFAULT SYSDATE NOT NULL,
    game_cover LONG,
    game_desc VARCHAR2(500),
    release_date DATE,
    download_link VARCHAR2(255),
    rating NUMBER(1, 0)

)

```

## Genre Table

```sql

CREATE TABLE genre (
    genre_id NUMBER(5, 0) CONSTRAINT genre_pk PRIMARY KEY,
    genre_name VARCHAR2(255) NOT NULL,
    genre_description LONG

)

```

## Requirements Table

```sql

CREATE TABLE requirement (
    game_id NUMBER(5, 0),
    req_type VARCHAR2(20),
    os VARCHAR2(255),
    cpu VARCHAR2(255),
    memory VARCHAR2(255),
    gpu VARCHAR2(255),
    CONSTRAINT req_pk PRIMARY KEY (game_id, req_type)

)

```

## has_genres Table

```sql

CREATE TABLE GLP.has_genres (
    game_id NUMBER(5),
    genre_id NUMBER(5),
    CONSTRAINT rel_game FOREIGN KEY (game_id)
    REFERENCES GLP.game(game_id),
    CONSTRAINT rel_genres FOREIGN KEY (genre_id)
    REFERENCES GLP.genre(genre_id),
    CONSTRAINT game_genres_rel PRIMARY KEY (game_id, genre_id)
)

```

## Favorites Table

```sql

CREATE TABLE GLP.favorites (
    game_id NUMBER(5),
    user_id NUMBER(4),
    CONSTRAINT rel_game1 FOREIGN KEY (game_id)
    REFERENCES GLP.game(game_id),
    CONSTRAINT rel_user FOREIGN KEY (user_id)
    REFERENCES GLP.users(user_id),
    CONSTRAINT favorites_pk PRIMARY KEY (game_id, user_id)
)

```

## User Table

```sql
CREATE TABLE GLP.users (

    user_id NUMBER(4, 0) CONSTRAINT user_pk PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    user_type VARCHAR(30)
)

```
