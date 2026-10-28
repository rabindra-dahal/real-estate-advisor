from app.infrastructure.sqlite_repo import SQLiteRepository

def read_system_logs():
    print(" Extracting Live Advisor Logs from SQLite Repository...")
    sqlite_repo = SQLiteRepository()
    
    with sqlite_repo.SessionLocal() as session:
        from app.infrastructure.sqlite_repo import DBAdviceLog
        logs = session.query(DBAdviceLog).order_by(DBAdviceLog.timestamp.desc()).all()
        
        if not logs:
            print(" No interaction logs found in the database.")
            return
            
        for log in logs[:3]:  # Display the top 3 most recent interactions
            print(f"\n[ID: {log.id}] | Timestamp: {log.timestamp}")
            print(f" Question: {log.question}")
            print(f" Provider: {log.provider_used.upper()}")
            print(f" Advice Rendered:\n{log.answer}\n" + "-"*50)

if __name__ == "__main__":
    read_system_logs()
