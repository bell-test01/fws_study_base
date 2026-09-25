-- Summary:
--     fws_case_recorder アプリのテーブル定義SQL。
-- Description:
--     案件記録テーブルと定型文テーブルを定義します。

-- 案件記録テーブル
CREATE TABLE IF NOT EXISTS case_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT,
    building TEXT,
    case_number TEXT,
    record_time TEXT,
    content TEXT,
    created_at TEXT,
    updated_at TEXT,
    is_editing INTEGER DEFAULT 0
);

-- 定型文テーブル
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT
);
