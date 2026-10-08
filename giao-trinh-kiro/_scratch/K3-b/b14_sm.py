# [đã chạy] Bài 14 — dedupe + state machine bằng compare-and-set trong SQLite, có tiêm crash
import sqlite3, random, os, tempfile
ALLOWED = {("RECEIVED", "PENDING_MODERATION"), ("PENDING_MODERATION", "APPROVED"),
           ("PENDING_MODERATION", "REJECTED"), ("APPROVED", "QUEUED"), ("QUEUED", "SPEAKING"),
           ("SPEAKING", "DONE"), ("SPEAKING", "INTERRUPTED"), ("QUEUED", "DONE")}  # QUEUED→DONE: chỉ bản ngây thơ

def db_open(path):
    db = sqlite3.connect(path, isolation_level=None)          # autocommit: mỗi lệnh là một transaction
    db.execute("PRAGMA journal_mode=WAL"); db.execute("PRAGMA synchronous=FULL")
    db.execute("CREATE TABLE IF NOT EXISTS c(key TEXT PRIMARY KEY, text TEXT, state TEXT)")
    return db

def ingest(db, key, text):                                     # gửi lặp N lần vẫn chỉ 1 dòng
    db.execute("INSERT OR IGNORE INTO c VALUES(?,?, 'RECEIVED')", (key, text))

def move(db, key, a, b):                                       # CAS: chỉ chuyển nếu đang ở đúng trạng thái a
    assert (a, b) in ALLOWED, f"cấm {a}->{b}"
    return db.execute("UPDATE c SET state=? WHERE key=? AND state=?", (b, key, a)).rowcount == 1

class Crash(Exception): pass

def player_step(db, played, p_crash, naive):
    row = db.execute("SELECT key FROM c WHERE state='QUEUED' LIMIT 1").fetchone()
    if not row: return
    k = row[0]
    if not naive and not move(db, k, "QUEUED", "SPEAKING"):    # ghi SPEAKING bền TRƯỚC khi phát
        return
    if random.random() < p_crash: raise Crash()                # chết trước khi kịp phát
    played[k] = played.get(k, 0) + 1                           # "âm thanh ra loa" — không rollback được
    if random.random() < p_crash: raise Crash()                # chết sau khi phát, trước khi ghi DONE
    move(db, k, "QUEUED" if naive else "SPEAKING", "DONE")

def recover(db):                                               # khởi động lại: KHÔNG tự phát lại
    db.execute("UPDATE c SET state='INTERRUPTED' WHERE state='SPEAKING'")

def run(naive, seed=14):
    random.seed(seed)
    path = os.path.join(tempfile.mkdtemp(), "t.db"); db, played, crashes = db_open(path), {}, 0
    for i in range(200):
        for _ in range(5): ingest(db, f"form-{i}", f"nội dung {i}")
        move(db, f"form-{i}", "RECEIVED", "PENDING_MODERATION")
        if i % 7: move(db, f"form-{i}", "PENDING_MODERATION", "APPROVED"); move(db, f"form-{i}", "APPROVED", "QUEUED")
    while db.execute("SELECT count(*) FROM c WHERE state='QUEUED'").fetchone()[0]:
        try: player_step(db, played, 0.05, naive)
        except Crash:
            crashes += 1; db.close(); db = db_open(path); recover(db)
    st = dict(db.execute("SELECT state, count(*) FROM c GROUP BY state").fetchall())
    leak = any(int(k.split('-')[1]) % 7 == 0 for k in played)  # bản ghi chưa duyệt có bị phát?
    print(f"{'ngây thơ' if naive else 'SPEAKING trước':<15} dòng={sum(st.values())} crash={crashes} "
          f"phát>1 lần={sum(v > 1 for v in played.values())} rò chưa duyệt={leak} trạng thái={st}")

run(naive=False); run(naive=True)
