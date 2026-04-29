import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",   # ← свой пароль
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        level_reached INTEGER,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit()


def get_player(username):
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()

    if res:
        return res[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    conn.commit()
    return cur.fetchone()[0]


def save_game(username, score, level):
    pid = get_player(username)
    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
        (pid, score, level)
    )
    conn.commit()


def get_top():
    cur.execute("""
    SELECT p.username, g.score, g.level_reached
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    ORDER BY g.score DESC
    LIMIT 10
    """)
    return cur.fetchall()


def get_best(username):
    cur.execute("""
    SELECT MAX(score)
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    WHERE p.username = %s
    """, (username,))
    res = cur.fetchone()[0]
    return res if res else 0