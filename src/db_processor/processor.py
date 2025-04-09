from postgrest.base_request_builder import APIResponse

from .connection import DatabaseConnection

def main():
    db: DatabaseConnection = DatabaseConnection()

    try:
        response: APIResponse = db.supabase.table(table_name="players").select("*").limit(size=1).execute()
        print(response)

        with db.pg_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM players LIMIT 1")
            result = cursor.fetchone()
            print(result)

    except Exception as e:
        print(f"Connection Error: {e}")
    
    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()