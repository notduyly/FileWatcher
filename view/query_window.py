import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, timedelta

class QueryWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
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
        
        # Get results through controller
        results = self.controller.query_events(extension, start_date)
        
        # Display results
        for row in results:
            self.tree.insert("", "end", values=row)
        
        self.db_results = results

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        if self.controller.export_to_csv(file_path, self.db_results):
            messagebox.showinfo("Success", f"CSV exported to {file_path}")
            self.last_exported_file = file_path
        else:
            messagebox.showerror("Error", "Failed to export CSV")

    def send_email(self):
        recipient = self.email_entry.get()
        if not recipient:
            messagebox.showwarning("Input Error", "Please enter recipient email.")
            return
        
        if not hasattr(self, "last_exported_file"):
            messagebox.showwarning("Missing File", "Please export to CSV first.")
            return
        
        if self.controller.send_email_results(recipient, self.last_exported_file):
            messagebox.showinfo("Success", "Email sent successfully.")
        else:
            messagebox.showerror("Error", "Failed to send email.")