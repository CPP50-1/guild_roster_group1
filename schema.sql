-- ==============================================================================
-- 1. ENTITY TABLES
-- ==============================================================================

CREATE TABLE roster (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT roster_name_key UNIQUE (name)
);

CREATE TABLE character (
    id SERIAL PRIMARY KEY,
    roster_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    class_type VARCHAR(20) NOT NULL,
    hp INTEGER NOT NULL,
    base_hp INTEGER NOT NULL,
    level INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    CONSTRAINT character_roster_id_fkey FOREIGN KEY (roster_id) REFERENCES roster(id) ON DELETE CASCADE,
    CONSTRAINT character_name_key UNIQUE (name),
    CONSTRAINT character_class_type_check CHECK (class_type IN ('Warrior', 'Mage', 'Rogue', 'Paladin')),
    CONSTRAINT character_hp_check CHECK (hp >= 0),
    CONSTRAINT character_base_hp_check CHECK (base_hp > 0),
    CONSTRAINT character_level_check CHECK (level >= 1 AND level <= 100),
    CONSTRAINT character_status_check CHECK (status IN ('Alive', 'Defeated'))
);
CREATE INDEX idx_character_roster_id ON character(roster_id);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rarity VARCHAR(20) NOT NULL,
    value INTEGER NOT NULL,
    CONSTRAINT item_name_key UNIQUE (name),
    CONSTRAINT item_rarity_check CHECK (rarity IN ('COMMON', 'UNCOMMON', 'RARE', 'EPIC', 'LEGENDARY')),
    CONSTRAINT item_value_check CHECK (value >= 0)
);

CREATE TABLE quest (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    reward_gold INTEGER NOT NULL,
    min_level INTEGER NOT NULL,
    CONSTRAINT quest_name_key UNIQUE (name),
    CONSTRAINT quest_reward_gold_check CHECK (reward_gold >= 0),
    CONSTRAINT quest_min_level_check CHECK (min_level >= 1)
);

-- ==============================================================================
-- 2. DUNGEON & ANALYTICS TABLES
-- ==============================================================================

CREATE TABLE dungeon (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    floor_count INTEGER NOT NULL,
    CONSTRAINT dungeon_name_key UNIQUE (name),
    CONSTRAINT dungeon_floor_count_check CHECK (floor_count >= 1)
);

CREATE TABLE dungeon_floor (
    id SERIAL PRIMARY KEY,
    dungeon_id INTEGER NOT NULL,
    sequence INTEGER NOT NULL,
    floor_type VARCHAR(20) NOT NULL,
    CONSTRAINT dungeon_floor_dungeon_id_fkey FOREIGN KEY (dungeon_id) REFERENCES dungeon(id) ON DELETE CASCADE,
    CONSTRAINT dungeon_floor_sequence_check CHECK (sequence >= 1),
    CONSTRAINT dungeon_floor_type_check CHECK (floor_type IN ('Combat', 'Boss', 'Treasure', 'Empty'))
);
CREATE INDEX idx_dungeon_floor_dungeon_id ON dungeon_floor(dungeon_id);

CREATE TABLE dungeon_result (
    id SERIAL PRIMARY KEY,
    dungeon_id INTEGER NOT NULL,
    roster_id INTEGER NOT NULL,
    result_type VARCHAR(20) NOT NULL,
    CONSTRAINT dungeon_result_dungeon_id_fkey FOREIGN KEY (dungeon_id) REFERENCES dungeon(id) ON DELETE CASCADE,
    CONSTRAINT dungeon_result_roster_id_fkey FOREIGN KEY (roster_id) REFERENCES roster(id) ON DELETE CASCADE,
    CONSTRAINT dungeon_result_type_check CHECK (result_type IN ('Victory', 'Defeat', 'Retreat'))
);
CREATE INDEX idx_dungeon_result_dungeon_id ON dungeon_result(dungeon_id);
CREATE INDEX idx_dungeon_result_roster_id ON dungeon_result(roster_id);

CREATE TABLE dungeon_log (
    id SERIAL PRIMARY KEY,
    dungeon_result_id INTEGER NOT NULL,
    sequence INTEGER NOT NULL,
    log TEXT NOT NULL,
    CONSTRAINT dungeon_log_dungeon_result_id_fkey FOREIGN KEY (dungeon_result_id) REFERENCES dungeon_result(id) ON DELETE CASCADE,
    CONSTRAINT dungeon_log_sequence_check CHECK (sequence >= 1)
);
CREATE INDEX idx_dungeon_log_dungeon_result_id ON dungeon_log(dungeon_result_id);

-- ==============================================================================
-- 3. JUNCTION / PIVOT TABLES (N-N RELATIONS)
-- ==============================================================================

CREATE TABLE character_items (
    character_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (character_id, item_id),
    CONSTRAINT character_items_character_id_fkey FOREIGN KEY (character_id) REFERENCES character(id) ON DELETE CASCADE,
    CONSTRAINT character_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    CONSTRAINT character_items_quantity_check CHECK (quantity >= 1)
);
CREATE INDEX idx_character_items_character_id ON character_items(character_id);
CREATE INDEX idx_character_items_item_id ON character_items(item_id);

CREATE TABLE character_quests (
    character_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'assigned',
    date_assigned TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (character_id, quest_id),
    CONSTRAINT character_quests_character_id_fkey FOREIGN KEY (character_id) REFERENCES character(id) ON DELETE CASCADE,
    CONSTRAINT character_quests_quest_id_fkey FOREIGN KEY (quest_id) REFERENCES quest(id) ON DELETE CASCADE,
    CONSTRAINT character_quests_status_check CHECK (status IN ('assigned', 'in_progress', 'completed'))
);
CREATE INDEX idx_character_quests_character_id ON character_quests(character_id);
CREATE INDEX idx_character_quests_quest_id ON character_quests(quest_id);