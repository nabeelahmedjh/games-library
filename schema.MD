### Creating a gamees Table:

```sql

CREATE TABLE game (
    game_id NUMBER(5) CONSTRAINT game_pk PRIMARY KEY,
    game_title VARCHAR2(255) NOT NULL,
    game_cover bfile,
    -- game_description VARCHAR2(3000),
    -- release_date DATE NOT NULL,
    add_at DATE DEFAULT SYSDATE NOT NULL,
)

```

### Creating a Ratings Table:

```sql
CREATE TABLE rating (
    rating_id NUMBER(5) CONSTRAINT rating_pk PRIMARY KEY,
    game_id NUMBER(5),
    steam_rating *DATATYPE*,
    ign_rating *DATATYPE*,
    google_rating *DATATYPE*,
    CONSTRAINT rating_game_rel
    FOREIGN KEY (game_id)
    REFERENCES (game.game_id)
)

```

### CREATING A platform Table:

```sql

CREATE TABLE platform (

)

```

### CREATING A genre Table:

```sql

CREATE TABLE genre (
    genre_id NUMBER(3) CONSTRAINT genre_pk PRIMARY KEY,
    genre_name VARCHAR2(255) NOT NULL,
    genre_description VARCHAR2(3000)

)

```

### CREATING A studio Table:

```sql

CREATE TABLE studio (

)

```

### CREATING A requirements Table:

```sql

CREATE TABLE requirement (

)

```

### CREATING A features Table:

```sql

CREATE TABLE requirement (

)

```

CREATE TABLE GLP.has_genres (
game_id NUMBER(5),
genre_id NUMBER(5),
CONSTRAINT rel_game FOREIGN KEY (game_id)
REFERENCES GLP.game(game_id),
CONSTRAINT rel_genres FOREIGN KEY (genre_id)
REFERENCES GLP.genre(genre_id),
CONSTRAINT game_genres_rel PRIMARY KEY (game_id, genre_id)
)

CREATE TABLE GLP.favorites (
game_id NUMBER(5),
user_id NUMBER(4),
CONSTRAINT rel_game1 FOREIGN KEY (game_id)
REFERENCES GLP.game(game_id),
CONSTRAINT rel_user FOREIGN KEY (user_id)
REFERENCES GLP.users(user_id),
CONSTRAINT favorites_pk PRIMARY KEY (game_id, user_id)
)
