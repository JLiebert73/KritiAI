"""
PM-KISAN District Registry Database Manager (`pm_kisan_registry.py`)
Manages the static/local SQLite database (`pm_kisan_registry.db`) representing the district's PM-KISAN registry
for District Agriculture Officers (DAO) to perform automated algorithmic triage and field verification routing.
"""

import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = "pm_kisan_registry.db"


def init_and_seed_registry(db_path: str = DB_PATH) -> None:
    """
    Initializes the local SQLite database and seeds it with a realistic district PM-KISAN registry
    containing pre-processed Prithvi-EO-2.0-tiny-TL Cultivation Consistency Scores.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pm_kisan_farms (
        khasra_id TEXT PRIMARY KEY,
        farmer_name TEXT NOT NULL,
        district TEXT NOT NULL,
        state TEXT NOT NULL,
        village_block TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        area_hectares REAL NOT NULL,
        consistency_score REAL NOT NULL,
        status TEXT NOT NULL,
        last_audited TEXT NOT NULL
    )
    """)
    
    # Check if records already exist
    cursor.execute("SELECT COUNT(*) FROM pm_kisan_farms")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_farms = [
            # Bottom 5% Anomaly Pool (Red Flagged: High Probability Fallow / Urbanized)
            ("102/B", "Bikash Das", "Kamrup", "Assam", "Rangia Block", 26.1520, 91.7410, 1.45, 0.2450, "Anomaly Flagged — Triage Pool", "2026-07-15 10:15:00"),
            ("115/P", "Ranjan Medhi", "Kamrup", "Assam", "Palashbari Block", 26.1840, 91.7920, 2.10, 0.3120, "Anomaly Flagged — Triage Pool", "2026-07-15 10:16:00"),
            
            # Top 95% Verified Cultivation Pool (Scores >= 0.70)
            ("101/A", "Arun Sharma", "Kamrup", "Assam", "Kamrup North Block", 26.1450, 91.7370, 1.25, 0.9871, "Verified Active Cultivation", "2026-07-15 10:14:00"),
            ("103/C", "Prabhat Kalita", "Kamrup", "Assam", "Kamrup North Block", 26.1480, 91.7390, 0.95, 0.9654, "Verified Active Cultivation", "2026-07-15 10:14:30"),
            ("104/D", "Hitesh Deka", "Kamrup", "Assam", "Rangia Block", 26.1550, 91.7450, 1.80, 0.9420, "Verified Active Cultivation", "2026-07-15 10:15:15"),
            ("105/E", "Monami Saikia", "Kamrup", "Assam", "Boko Block", 26.1620, 91.7520, 1.10, 0.9780, "Verified Active Cultivation", "2026-07-15 10:15:30"),
            ("106/F", "Debajit Gogoi", "Kamrup", "Assam", "Chaygaon Block", 26.1680, 91.7590, 2.30, 0.9125, "Verified Active Cultivation", "2026-07-15 10:15:45"),
            ("107/G", "Ritul Barman", "Kamrup", "Assam", "Kamrup North Block", 26.1710, 91.7630, 1.05, 0.8950, "Verified Active Cultivation", "2026-07-15 10:16:10"),
            ("108/H", "Ananya Sarma", "Kamrup", "Assam", "Palashbari Block", 26.1750, 91.7680, 1.65, 0.9540, "Verified Active Cultivation", "2026-07-15 10:16:25"),
            ("109/I", "Kishore Roy", "Kamrup", "Assam", "Rangia Block", 26.1790, 91.7740, 1.35, 0.9310, "Verified Active Cultivation", "2026-07-15 10:16:40"),
            ("110/J", "Dipankar Bhuyan", "Kamrup", "Assam", "Boko Block", 26.1820, 91.7790, 0.85, 0.9680, "Verified Active Cultivation", "2026-07-15 10:16:55"),
            ("111/K", "Suren Dutta", "Kamrup", "Assam", "Chaygaon Block", 26.1860, 91.7840, 1.95, 0.8840, "Verified Active Cultivation", "2026-07-15 10:17:10"),
            ("112/L", "Hemanta Talukdar", "Kamrup", "Assam", "Kamrup North Block", 26.1910, 91.7890, 1.50, 0.9720, "Verified Active Cultivation", "2026-07-15 10:17:25"),
            ("113/M", "Mridul Nath", "Kamrup", "Assam", "Rangia Block", 26.1950, 91.7940, 1.15, 0.9190, "Verified Active Cultivation", "2026-07-15 10:17:40"),
            ("114/N", "Gitika Baruah", "Kamrup", "Assam", "Palashbari Block", 26.1980, 91.7980, 2.40, 0.9610, "Verified Active Cultivation", "2026-07-15 10:17:55"),
            ("116/Q", "Manas Boro", "Kamrup", "Assam", "Boko Block", 26.2040, 91.8050, 1.20, 0.9480, "Verified Active Cultivation", "2026-07-15 10:18:10"),
            ("117/R", "Niren Kachari", "Kamrup", "Assam", "Chaygaon Block", 26.2080, 91.8100, 1.75, 0.9350, "Verified Active Cultivation", "2026-07-15 10:18:25"),
            ("118/S", "Upasana Baishya", "Kamrup", "Assam", "Kamrup North Block", 26.2120, 91.8150, 0.90, 0.9810, "Verified Active Cultivation", "2026-07-15 10:18:40"),
            ("119/T", "Jitu Patgiri", "Kamrup", "Assam", "Rangia Block", 26.2160, 91.8200, 1.60, 0.9240, "Verified Active Cultivation", "2026-07-15 10:18:55"),
            ("120/U", "Sanjoy Hazarika", "Kamrup", "Assam", "Palashbari Block", 26.2200, 91.8250, 1.40, 0.9570, "Verified Active Cultivation", "2026-07-15 10:19:10")
        ]
        
        cursor.executemany("""
        INSERT OR REPLACE INTO pm_kisan_farms 
        (khasra_id, farmer_name, district, state, village_block, lat, lon, area_hectares, consistency_score, status, last_audited)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_farms)
        conn.commit()
        
    conn.close()


def get_all_farms(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """
    Returns all registered farms sorted automatically by Cultivation Consistency Score from lowest to highest.
    """
    init_and_seed_registry(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pm_kisan_farms ORDER BY consistency_score ASC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_farm_by_id(khasra_id: str, db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Retrieves a single farm by its Survey Number (khasra_id).
    """
    init_and_seed_registry(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pm_kisan_farms WHERE khasra_id = ?", (khasra_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}


def update_farm_status(khasra_id: str, new_status: str, db_path: str = DB_PATH) -> bool:
    """
    Updates the administrative status of a target farm (e.g., 'Pending Field Audit').
    """
    init_and_seed_registry(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE pm_kisan_farms SET status = ? WHERE khasra_id = ?", (new_status, khasra_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


if __name__ == "__main__":
    init_and_seed_registry()
    print("PM-KISAN Registry initialized successfully.")
