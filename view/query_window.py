import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from email import EmailSender
from model.db_handler import (fetch_all_events, fetch_event_by_type, 
                            fetch_event_by_extension, fetch_event_by_after_date)
import csv
from datetime import datetime, timedelta

class QueryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Database Query")
        self.geometry("800x600")
        
        # Query filters frame
        filter_frame = ttk.LabelFrame(self, text="Query Filters")
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Extension filter
        ttk.Label(filter_frame, text="File Extension:").grid(row=0, column=0, padx=5, pady=5)
        self.ext_var = tk.StringVar(value="All")
        self.ext_combo = ttk.Combobox(filter_frame, textvariable=self.ext_var)
        self.ext_combo['values'] = ['All', '.txt', '.png', '.jpg']
        self.ext_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Date filter
        ttk.Label(filter_frame, text="Date Range:").grid(row=1, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar(value="All")
        date_options = ["All", "Today", "Last 7 days", "Last 30 days"]
        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, values=date_options)
        self.date_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Search button
        ttk.Button(filter_frame, text="Search", command=self.perform_query).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results treeview
        columns = ("ID", "Filename", "Extension", "Timestamp", "Size", "Event")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom frame for export and email
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10)
        
        ttk.Button(bottom_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side="left", padx=5)
        
        ttk.Label(bottom_frame, text="Email:").pack(side="left", padx=5)
        self.email_entry = ttk.Entry(bottom_frame, width=30)
        self.email_entry.pack(side="left", padx=5)
        
        ttk.Button(bottom_frame, text="Send Email", 
                  command=self.send_email).pack(side="left", padx=5)
        
        # Initial query
        self.perform_query()
    
    def perform_query(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get filter values
        extension = None if self.ext_var.get() == "All" else self.ext_var.get()
        date_range = self.date_var.get()
        
        # Get date filter
        start_date = None
        if date_range == "Today":
            start_date = datetime.now().strftime("%Y-%m-%d")
        elif date_range == "Last 7 days":
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        elif date_range == "Last 30 days":
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Fetch results based on filters
        if start_date:
            results = fetch_event_by_after_date(start_date)
        else:
            results = fetch_all_events()
            
        # Filter by extension if needed
        if extension:
            results = [r for r in results if r[2] == extension]  # Assuming extension is at index 2
            
        # Display results
        for row in results:
            self.tree.insert("", "end", values=row)
        
        self.db_results = results  # Store for export/email
    
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Extension", "Filename", "PATH", "Event", "Date/Time"])
                for row in self.db_results:
                    writer.writerow(row)
            messagebox.showinfo("Success", f"CSV exported to {file_path}")
            self.last_exported_file = file_path

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def send_email(self):
        recipient = self.email_entry.get()
        if not recipient:
            messagebox.showwarning("Input Error", "Please enter recipient email.")
            return
        
        if not hasattr(self, "last_exported_file"):
            messagebox.showwarning("Missing File", "Please export to CSV first.")
            return
        
        try:
            sender = EmailSender(sender_email="your@email.com", password="your_app_password")
            subject = "File Watcher Query Result"
            body = "Please find the attached CSV file of the query result."

            success = sender.send_email_with_attachment(
                recipient_email=recipient,
                subject=subject,
                body=body,
                attachment_path=self.last_exported_file
            )
            
            if success:
                messagebox.showinfo("Success", "Email sent successfully.")
            else:
                messagebox.showerror("Failure", "Failed to send email.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error sending email: {e}")