

### Creating a Games Table:
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
