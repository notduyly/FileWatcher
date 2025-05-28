import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, timedelta

class QueryWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Database Query")
        self.geometry("1000x600")
        
        # Query filters frame
        filter_frame = ttk.LabelFrame(self, text="Query Filters")
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Query type filter
        ttk.Label(filter_frame, text="Query Type:").grid(row=0, column=0, padx=5, pady=5)
        self.query_type_var = tk.StringVar(value="all")
        self.query_type_combo = ttk.Combobox(filter_frame, textvariable=self.query_type_var)
        self.query_type_combo['values'] = ['All Events', 'By Event Type', 'By Extension', 'By Date']
        self.query_type_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Extension filter
        ttk.Label(filter_frame, text="File Extension:").grid(row=1, column=0, padx=5, pady=5)
        self.ext_var = tk.StringVar(value="All")
        self.ext_combo = ttk.Combobox(filter_frame, textvariable=self.ext_var)
        self.ext_combo['values'] = ['All', '.txt', '.png', '.jpg']
        self.ext_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Date filter
        ttk.Label(filter_frame, text="Date Range:").grid(row=2, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar(value="All")
        date_options = ["All", "Today", "Last 7 days", "Last 30 days"]
        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, values=date_options)
        self.date_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Search button
        ttk.Button(filter_frame, text="Search", command=self.perform_query).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Results treeview with updated columns
        columns = ("ID", "Filename", "File Path", "File Extension", 
                "Event", "Event Timestamp", "File Size", "Is Directory", "User")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Configure column headings and widths
        column_widths = {
            "ID": 20,
            "Filename": 100,
            "File Path": 200,
            "File Extension": 30,
            "Event": 50,
            "Event Timestamp": 150,
            "File Size": 50,
            "Is Directory": 50,
            "User": 80
        }
        
        for col, width in column_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom frame for export and email
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10)
        
        # Add Reset DB button
        ttk.Button(bottom_frame, text="Reset Database", 
                command=self.reset_database,
                style='Danger.TButton').pack(side="right", padx=20)  # 오른쪽에 배치
        
        # Create danger style for reset button
        danger_style = ttk.Style()
        danger_style.configure('Danger.TButton', 
                            foreground='red',
                            font=('Arial', 10, 'bold'))
        
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
        
        # Get query type
        query_type = self.query_type_var.get()
        
        # Convert query type to parameter
        if query_type == "By Event Type":
            results = self.controller.query_events(query_type="event_type")
            # Display event type statistics
            for event_type, count in results:
                self.tree.insert("", "end", values=("", "", "", "", 
                            event_type, "", "", "", f"Count: {count}"))
                
        elif query_type == "By Extension":
            results = self.controller.query_events(query_type="extension")
            # Display extension statistics
            for extension, count in results:
                self.tree.insert("", "end", values=("", "", "", 
                            extension, "", "", "", "", f"Count: {count}"))
                
        elif query_type == "By Date":
            date_range = self.date_var.get()
            start_date = None
            if date_range == "Today":
                start_date = datetime.now().strftime("%Y-%m-%d")
            elif date_range == "Last 7 days":
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            elif date_range == "Last 30 days":
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                
            results = self.controller.query_events(query_type="date", start_date=start_date)
            # Display full event details
            for event in results:
                self.tree.insert("", "end", values=event)
        
        else:  # All Events
            results = self.controller.query_events()
            # Display full event details
            for event in results:
                self.tree.insert("", "end", values=event)
        
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
    
    def reset_database(self):
        """Reset the database after confirmation"""
        if messagebox.askyesno("Confirm Reset", 
                            "Are you sure you want to reset the database?\n"
                            "This action cannot be undone!"):
            if self.controller.reset_database():
                messagebox.showinfo("Success", "Database has been reset successfully")
                self.perform_query()  # Refresh the view
            else:
                messagebox.showerror("Error", "Failed to reset database")