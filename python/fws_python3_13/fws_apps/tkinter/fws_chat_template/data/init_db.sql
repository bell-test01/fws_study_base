-- 機器機種マスタテーブル
CREATE TABLE IF NOT EXISTS mst_device_models (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL UNIQUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

-- 初期マスタデータ投入（機器機種マスタ）
INSERT OR IGNORE INTO mst_device_models (model_id, model_name, sort_order) VALUES
('M0001', 'RTX1210', 10),
('M0002', 'RTX1220', 20),
('M0003', 'Catalyst 2960', 30),
('M0004', 'Catalyst 9200', 40),
('M0005', 'SRX300', 50),
('M0006', 'FortiGate 60F', 60);

-- タスクテンプレートマスタテーブル
CREATE TABLE IF NOT EXISTS mst_task_templates (
    task_template_id TEXT PRIMARY KEY,
    category_name TEXT NOT NULL,
    task_name TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

-- 初期マスタデータ投入（タスクテンプレートマスタ）
INSERT OR IGNORE INTO mst_task_templates (task_template_id, category_name, task_name, sort_order) VALUES
('T0001', '手配', 'Description更新', 10),
('T0002', '手配', 'オンサイト手配', 20),
('T0003', '調査', '機器ログ取得', 30),
('T0004', '調査', 'Ping疎通確認', 40),
('T0005', '検証', 'UIパターン検証', 50);

-- タスクチェックリストテンプレートマスタテーブル
CREATE TABLE IF NOT EXISTS mst_task_checklist_templates (
    checklist_template_id TEXT PRIMARY KEY,
    task_template_id TEXT NOT NULL,
    category_name TEXT NOT NULL,
    task_name TEXT NOT NULL,
    item_seq INTEGER NOT NULL,
    display_text TEXT NOT NULL,
    append_text TEXT NOT NULL,
    extra_builder TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

-- 初期マスタデータ投入（タスクチェックリストテンプレートマスタ）
INSERT OR IGNORE INTO mst_task_checklist_templates (checklist_template_id, task_template_id, category_name, task_name, item_seq, display_text, append_text, extra_builder) VALUES
('C0001', 'T0001', '手配', 'Description更新', 1, 'Description更新', 'Description更新', ''),
('C0002', 'T0001', '手配', 'Description更新', 2, 'AppsのDescriptionの更新', 'AppsのDescriptionの更新', ''),
('C0003', 'T0001', '手配', 'Description更新', 3, 'OsiansのDescriptionの更新', 'OsiansのDescriptionの更新', ''),
('C0004', 'T0001', '手配', 'Description更新', 4, 'オンサイトへメール再送付実施', 'オンサイトへメール再送付実施', ''),
('C0005', 'T0001', '手配', 'Description更新', 5, 'オンサイトへ電話連絡実施', 'オンサイトへ電話連絡実施', 'onsite_call'),
('C0006', 'T0001', '手配', 'Description更新', 6, '次のアクション', '次のアクション', ''),
('C0007', 'T0002', '手配', 'オンサイト手配', 1, 'オンサイト依頼メール送付', 'オンサイト依頼メール送付', ''),
('C0008', 'T0002', '手配', 'オンサイト手配', 2, '作業日程確定', '作業日程確定', ''),
('C0009', 'T0002', '手配', 'オンサイト手配', 3, '入館申請完了', '入館申請完了', ''),
('C0010', 'T0003', '調査', '機器ログ取得', 1, 'ターミナル接続確認', 'ターミナル接続確認', ''),
('C0011', 'T0003', '調査', '機器ログ取得', 2, 'show tech-support取得', 'show tech-support取得', ''),
('C0012', 'T0003', '調査', '機器ログ取得', 3, 'ログ保存', 'ログ保存', ''),
('C0013', 'T0004', '調査', 'Ping疎通確認', 1, 'NW側疎通確認', 'NW側疎通確認', ''),
('C0014', 'T0004', '調査', 'Ping疎通確認', 2, '端末側疎通確認', '端末側疎通確認', ''),
('C0015', 'T0005', '検証', 'UIパターン検証', 1, 'テキスト入力検証', 'テキスト入力', 'text_only'),
('C0016', 'T0005', '検証', 'UIパターン検証', 2, 'ホスト選択検証', 'ホスト選択', 'host_combo'),
('C0017', 'T0005', '検証', 'UIパターン検証', 3, 'テキスト加工連動検証', 'テキスト加工', 'text_transform'),
('C0018', 'T0005', '検証', 'UIパターン検証', 4, '動的UI切替検証', '動的UI切替', 'dynamic_selector'),
('C0020', 'T0005', '検証', 'UIパターン検証', 5, '機器交換作業', '工程終了', 'device_swap');

-- チケット基本情報テーブル（ヘッダ）
CREATE TABLE IF NOT EXISTS tickets (
    ticket_number TEXT NOT NULL,
    prefecture TEXT NOT NULL,
    building_name TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (ticket_number, prefecture, building_name)
);

-- チケット詳細テキストテーブル（本文・世代管理）
CREATE TABLE IF NOT EXISTS ticket_descriptions (
    ticket_number TEXT NOT NULL,
    prefecture TEXT NOT NULL,
    building_name TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    description TEXT NOT NULL DEFAULT '',
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (ticket_number, prefecture, building_name, revision)
);

-- 初期ダミーデータ投入（チケット基本情報）
INSERT OR IGNORE INTO tickets (ticket_number, prefecture, building_name, is_deleted) VALUES
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 0),
('TICKET-2026-001', '東京都', '新宿ミライナタワー', 0),
('TICKET-2026-001', '神奈川県', '武蔵小杉タワープレイス', 0),
('TICKET-2026-002', '神奈川県', '横浜ランドマークタワー', 0),
('TICKET-2026-003', '大阪府', 'グランフロント大阪', 0);

-- 初期ダミーデータ投入（チケット詳細テキスト）
INSERT OR IGNORE INTO ticket_descriptions (ticket_number, prefecture, building_name, revision, description, is_deleted) VALUES
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, '【障害概要】ルータ電源断による通信途絶\n【対応方針】オンサイトにて機器交換および疎通確認を実施する。', 0),
('TICKET-2026-001', '東京都', '新宿ミライナタワー', 1, '【障害概要】新宿拠点 サブ回線瞬断調査\nログ解析および回線キャリア問い合わせを実施。', 0),
('TICKET-2026-001', '神奈川県', '武蔵小杉タワープレイス', 1, '【障害概要】神奈川サテライト拠点 Wi-Fiアクセスポイント接続不能\n現地確認およびPoE給電確認。', 0),
('TICKET-2026-002', '神奈川県', '横浜ランドマークタワー', 1, '【定期作業】スイッチファームウェアアップデート作業\n事前連絡済み。', 0),
('TICKET-2026-003', '大阪府', 'グランフロント大阪', 1, '【調査依頼】パケットロス調査およびログ取得\nPing疎通確認とshow tech取得を実施。', 0);

-- チケット機器明細情報テーブル（世代管理・リスト順序インデックスPK）
CREATE TABLE IF NOT EXISTS ticket_devices (
    ticket_number TEXT NOT NULL,
    prefecture TEXT NOT NULL,
    building_name TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    item_number INTEGER NOT NULL DEFAULT 0,
    rack_name TEXT NOT NULL DEFAULT '',
    hostname TEXT NOT NULL DEFAULT '',
    model_name TEXT NOT NULL DEFAULT '',
    serial_number TEXT NOT NULL DEFAULT '',
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (ticket_number, prefecture, building_name, revision, item_number),
    FOREIGN KEY (ticket_number, prefecture, building_name)
        REFERENCES tickets (ticket_number, prefecture, building_name) ON DELETE CASCADE
);

-- 初期ダミーデータ投入（機器明細情報）
INSERT OR IGNORE INTO ticket_devices (ticket_number, prefecture, building_name, revision, item_number, rack_name, hostname, model_name, serial_number, is_deleted) VALUES
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, 0, 'ラックA-01', 'RT-SHIBUYA-01', 'RTX1220', 'SN-RTX-00123', 0),
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, 1, 'ラックA-02', 'SW-SHIBUYA-01', 'Catalyst 2960', 'SN-CAT-98765', 0),
('TICKET-2026-002', '神奈川県', '横浜ランドマークタワー', 1, 0, 'ラックB-01', 'FW-YOKOHAMA-01', 'FortiGate 60F', 'SN-FG-55555', 0);

-- チケット時系列タスクカードテーブル（世代管理・リスト順序インデックスPK）
CREATE TABLE IF NOT EXISTS ticket_timeline_tasks (
    ticket_number TEXT NOT NULL,
    prefecture TEXT NOT NULL,
    building_name TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    item_number INTEGER NOT NULL DEFAULT 0,
    task_template_id TEXT NOT NULL DEFAULT '',
    category_name TEXT NOT NULL DEFAULT '',
    task_name TEXT NOT NULL DEFAULT '',
    task_time TEXT NOT NULL DEFAULT '',
    memo TEXT NOT NULL DEFAULT '',
    is_completed INTEGER NOT NULL DEFAULT 0,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (ticket_number, prefecture, building_name, revision, item_number),
    FOREIGN KEY (ticket_number, prefecture, building_name)
        REFERENCES tickets (ticket_number, prefecture, building_name) ON DELETE CASCADE
);

-- チケット時系列タスクチェックリスト状態テーブル（世代管理・複合PK）
CREATE TABLE IF NOT EXISTS ticket_timeline_task_checklists (
    ticket_number TEXT NOT NULL,
    prefecture TEXT NOT NULL,
    building_name TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1,
    task_item_number INTEGER NOT NULL DEFAULT 0,
    item_seq INTEGER NOT NULL DEFAULT 0,
    checklist_template_id TEXT NOT NULL DEFAULT '',
    extra_builder TEXT NOT NULL DEFAULT '',
    extra_data TEXT NOT NULL DEFAULT '',
    display_text TEXT NOT NULL DEFAULT '',
    append_text TEXT NOT NULL DEFAULT '',
    is_checked INTEGER NOT NULL DEFAULT 0,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (ticket_number, prefecture, building_name, revision, task_item_number, item_seq),
    FOREIGN KEY (ticket_number, prefecture, building_name)
        REFERENCES tickets (ticket_number, prefecture, building_name) ON DELETE CASCADE
);

-- 初期ダミーデータ投入（時系列タスク情報）
INSERT OR IGNORE INTO ticket_timeline_tasks (ticket_number, prefecture, building_name, revision, item_number, task_template_id, category_name, task_name, task_time, memo, is_completed, is_deleted) VALUES
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, 0, 'T0001', '手配', 'Description更新', '10:00', 'タスク初期手配メモ', 0, 0);

-- 初期ダミーデータ投入（時系列タスクチェックリスト状態）
INSERT OR IGNORE INTO ticket_timeline_task_checklists (ticket_number, prefecture, building_name, revision, task_item_number, item_seq, checklist_template_id, extra_builder, extra_data, display_text, append_text, is_checked, is_deleted) VALUES
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, 0, 1, 'C0001', '', '', 'Description更新', 'Description更新', 1, 0),
('TICKET-2026-001', '東京都', '渋谷サクラステージ', 1, 0, 2, 'C0002', '', '', 'AppsのDescriptionの更新', 'AppsのDescriptionの更新', 0, 0);





