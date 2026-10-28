import sys
from app.infrastructure.sqlite_repo import SQLiteRepository

def display_error_dashboard():
    sqlite_repo = SQLiteRepository()
    args = sys.argv[1:]
    
    if not args:
        # --- Overview Mode: Print Dashboard Table Layout ---
        print("\n Loading Recent Middleware System Anomalies from SQLite...")
        errors = sqlite_repo.get_recent_errors(limit=10)
        
        if not errors:
            print(" Clean Health Bill: No runtime crashes recorded in your application logs.")
            return

        header_format = "| {:<38} | {:<7} | {:<20} | {:<40} |"
        row_format    = "| {:<38} | {:<7} | {:<20} | {:<40} |"
        divider = "+" + "-"*40 + "+" + "-"*9 + "+" + "-"*22 + "+" + "-"*42 + "+"
        
        print(divider)
        print(header_format.format("TRACKING ID", "METHOD", "ENDPOINT", "ERROR MESSAGE SUMMARY"))
        print(divider)
        
        for err in errors:
            truncated_path = err.endpoint[:20] + "..." if len(err.endpoint) > 20 else err.endpoint
            truncated_msg = err.error_message[:37] + "..." if len(err.error_message) > 37 else err.error_message
            print(row_format.format(err.log_id, err.method, truncated_path, truncated_msg))
            
        print(divider)
        print("\n Tip: Run 'python read_errors.py <id>' to view detailed trace specs.")
        print(" Maintenance: Run 'python read_errors.py --clear' to wipe logging registers clean.")

    elif args[0] == "--clear":
        # --- Maintenance Mode: Truncate All Error Logs ---
        print("\n  Initiating bulk eviction protocol over error logging schemas...")
        try:
            purged_records = sqlite_repo.clear_all_error_logs()
            print(f" Success: Purged {purged_records} error trace profiles completely from storage indexes.")
        except Exception as e:
            print(f" Abort: Critical maintenance sequence failure: {str(e)}")

    else:
        # --- Detailed Mode: Look Up Specific Tracking Code Trace ---
        target_id = args[0]
        print(f"\n Searching for Tracking ID: {target_id}...")
        error_record = sqlite_repo.get_error_by_id(target_id)
        
        if not error_record:
            print(f" Error log signature matching ID '{target_id}' could not be located.")
            return
            
        print("=" * 80)
        print(f" ERROR AUDIT TRACE LOG | {error_record.log_id}")
        print("=" * 80)
        print(f" Timestamp: {error_record.timestamp}")
        print(f" Location:  {error_record.method} {error_record.endpoint}")
        print(f"  Summary:   {error_record.error_message}")
        print("-" * 80)
        print(" STACK TRACE DEEP DIVE:")
        print(error_record.stack_trace)
        print("=" * 80)

if __name__ == "__main__":
    display_error_dashboard()
