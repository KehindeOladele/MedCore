from app.core.supabase_client import supabase


# ----- Initialize Database -----
def run_sql(sql: str):
    try:
        response = supabase.rpc(sql).execute()
        print("Database initialized successfully", response)
    
    except Exception as e:
        print(f"Error initializing database: {e}")

    # if response.get("error"):
    #     print(f"Error executing SQL: {response['error']}")


# ----- Load and Execute SQL Commands for Patients Table -----
with open("sql/profiles.sql", "r", encoding="utf-8") as f:
    for cmd in f.read().split(";"):
        if cmd.strip():
            run_sql(cmd)

# with open("sql/002_medical_records.sql") as f:
#     run_sql(f.read())


# if __name__ == "__main__":
#     run_sql()