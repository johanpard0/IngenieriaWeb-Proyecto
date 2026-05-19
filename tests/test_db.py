from sqlalchemy import text
from backend.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
        )

        tables = result.fetchall()

        print("Conexión exitosa a PostgreSQL")
        print("Tablas encontradas:")

        for table in tables:
            print("-", table[0])

except Exception as e:
    print("Error al conectar con PostgreSQL:")
    print(e)