import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os

class QueryWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Database Query")
        self.geometry("1000x600")
        
        # Query filters frame
        filter_frame = ttk.LabelFrame(self, text="Query Filters")
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Event type filter
        ttk.Label(filter_frame, text="Event Type:").grid(row=0, column=0, padx=5, pady=5)
        self.event_type_var = tk.StringVar(value="All")
        self.event_type_combo = ttk.Combobox(filter_frame, textvariable=self.event_type_var)
        self.event_type_combo['values'] = ['All', 'created', 'modified', 'deleted']
        self.event_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.event_type_combo.bind('<<ComboboxSelected>>', lambda e: self.perform_query())
        
        # Extension filter
        ttk.Label(filter_frame, text="File Extension:").grid(row=1, column=0, padx=5, pady=5)
        self.ext_var = tk.StringVar(value="All")
        self.ext_combo = ttk.Combobox(filter_frame, textvariable=self.ext_var)
        self.ext_combo['values'] = ['All', '.txt', '.png', '.jpg', '.py']
        self.ext_combo.grid(row=1, column=1, padx=5, pady=5)
        self.ext_combo.bind('<<ComboboxSelected>>', lambda e: self.perform_query())
        
        # Date filter
        ttk.Label(filter_frame, text="Date Range:").grid(row=2, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar(value="All")
        date_options = ["All", "Today", "Last 7 days", "Last 30 days"]
        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.date_var, values=date_options)
        self.date_combo.grid(row=2, column=1, padx=5, pady=5)
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.perform_query())

        # Search button
        ttk.Button(filter_frame, text="Search", command=self.perform_query).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Results treeview with simplified columns
        cols = ("Filename", "Extension", "Path", "Event", "Timestamp")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        # Configure columns like setup_window.py
        self.tree.column("Filename", width=75, anchor=tk.W)
        self.tree.column("Extension", width=75, anchor=tk.W)
        self.tree.column("Path", width=400, anchor=tk.W)
        self.tree.column("Event", width=100, anchor=tk.W)
        self.tree.column("Timestamp", width=150, anchor=tk.W)
        
        # Set column headings
        for col in cols:
            self.tree.heading(col, text=col)

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
        self.__email_entry = ttk.Entry(bottom_frame, width=30)
        self.__email_entry.pack(side="left", padx=5)
        
        ttk.Button(bottom_frame, text="Send Email", 
                command=self.send_email).pack(side="left", padx=5)
        
        # Initial query
        self.perform_query()
    
    def perform_query(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filter values
        filters = {
            'event_type': self.event_type_var.get(),
            'extension': self.ext_var.get(),
            'date_range': self.date_var.get()
        }
        print(f"Applied filters: {filters}")
        
        # Get results through controller
        results = self.controller.get_filtered_events(filters)
        print(f"Query returned {len(results) if results else 0} results")
        
        if results:
            for event in results:
                try:
                    file_path = event[2]  # 데이터베이스에서 가져온 전체 경로
                    filename = os.path.basename(file_path)
                    extension = os.path.splitext(filename)[1] or "(none)"
                    
                    # 현재 작업 디렉토리 기준으로 경로 표시
                    display_path = file_path.replace(os.getcwd() + os.sep, '')
                    
                    self.tree.insert('', 0, values=(
                        filename,
                        extension,
                        display_path,  # 상대 경로로 표시
                        event[4],      # event_type
                        event[5]       # timestamp
                    ))
                except Exception as e:
                    print(f"Error processing event: {e}")
    
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
        recipient = self.__email_entry.get()
        if not recipient:
            messagebox.showwarning("Input Error", "Please enter recipient email.")
            return
        
        if not hasattr(self, "last_exported_file"):
            messagebox.showwarning("Missing File", "Please export to CSV first.")
            return
        
        if self.__myController.send_email_results(recipient, self.__last_exported_file):
            messagebox.showinfo("Success", "Email sent successfully.")
        else:
            messagebox.showerror("Error", "Failed to send email.")
    
    def reset_database(self):
        if messagebox.askyesno("Confirm Reset", 
                            "Are you sure you want to reset the database?\n"
                            "This action cannot be undone!"):
            if self.controller.reset_database():
                messagebox.showinfo("Success", "Database has been reset successfully")
                self.perform_query()
            else:
                messagebox.showerror("Error", "Failed to reset database")