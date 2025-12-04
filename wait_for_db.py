#!/usr/bin/env python
import os
import sys
import time
import psycopg2

def wait_for_db():
    """Ждем пока база данных будет готова"""
    db_config = {
        'host': os.getenv('DB_HOST', 'db'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'lesson_db'),
        'user': os.getenv('DB_USER', 'lesson_user'),
        'password': os.getenv('DB_PASSWORD', 'lesson_pass'),
    }
    
    print("Waiting for database to be ready...")
    
    for i in range(30):  # 30 попыток по 2 секунды = 60 секунд максимум
        try:
            conn = psycopg2.connect(**db_config)
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError as e:
            if i % 5 == 0:  # Сообщаем каждые 5 попыток
                print(f"Attempt {i+1}/30: Database not ready yet...")
            time.sleep(2)
    
    print("Failed to connect to database after 30 attempts")
    return False

if __name__ == "__main__":
    if wait_for_db():
        sys.exit(0)
    else:
        sys.exit(1)