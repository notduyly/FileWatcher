import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os

class QueryWindow(tk.Toplevel):
    def __init__(self, master, theController):
        super().__init__(master)
        self.__myController = theController
        self.title("Database Query")
        self.geometry("1000x600")
        
        # Query filters frame
        filter_frame = ttk.LabelFrame(self, text="Query Filters")
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Event type filter
        ttk.Label(filter_frame, text="Event Type:").grid(row=0, column=0, padx=5, pady=5)
        self.__myEventTypeVar = tk.StringVar(value="All")
        self.__myEventTypeCombo = ttk.Combobox(filter_frame, textvariable=self.__myEventTypeVar)
        self.__myEventTypeCombo['values'] = ['All', 'created', 'modified', 'deleted']
        self.__myEventTypeCombo.grid(row=0, column=1, padx=5, pady=5)
        self.__myEventTypeCombo.bind('<<ComboboxSelected>>', lambda e: self.__perform_query())
        
        # Extension filter
        ttk.Label(filter_frame, text="File Extension:").grid(row=1, column=0, padx=5, pady=5)
        self.__myExtVar = tk.StringVar(value="All")
        self.__myExtCombo = ttk.Combobox(filter_frame, textvariable=self.__myExtVar)
        self.__myExtCombo['values'] = self.__myController.get_available_extensions()
        self.__myExtCombo.grid(row=1, column=1, padx=5, pady=5)
        self.__myExtCombo.bind('<<ComboboxSelected>>', lambda e: self.__perform_query())
        
        # Date filter
        ttk.Label(filter_frame, text="Date Range:").grid(row=2, column=0, padx=5, pady=5)
        self.__myDateVar = tk.StringVar(value="All")
        date_options = ["All", "Today", "Last 7 days", "Last 30 days"]
        self.__myDateCombo = ttk.Combobox(filter_frame, textvariable=self.__myDateVar, values=date_options)
        self.__myDateCombo.grid(row=2, column=1, padx=5, pady=5)
        self.__myDateCombo.bind('<<ComboboxSelected>>', lambda e: self.__perform_query())

        # Search button
        ttk.Button(filter_frame, text="Search", 
                  command=self.__perform_query).grid(row=3, column=0, columnspan=2, pady=10)

        # Results treeview with simplified columns
        cols = ("Filename", "Extension", "Path", "Event", "Timestamp")
        self.__myTree = ttk.Treeview(self, columns=cols, show='headings')
        
        # Configure columns like setup_window.py
        self.__myTree.column("Filename", width=75, anchor=tk.W)
        self.__myTree.column("Extension", width=75, anchor=tk.W)
        self.__myTree.column("Path", width=400, anchor=tk.W)
        self.__myTree.column("Event", width=100, anchor=tk.W)
        self.__myTree.column("Timestamp", width=150, anchor=tk.W)
        
        # Set column headings
        for col in cols:
            self.__myTree.heading(col, text=col)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.__myTree.yview)
        self.__myTree.configure(yscrollcommand=scrollbar.set)
        
        self.__myTree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom frame for export and email
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10)
        
        # Add Reset DB button
        ttk.Button(bottom_frame, text="Reset Database", 
                command=self.reset_database,
                style='Danger.TButton').pack(side="right", padx=20)
        
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
        self.__perform_query()
    
    def __perform_query(self):
        """Perform database query with current filters and refresh extension list"""
        # Clear existing items
        for item in self.__myTree.get_children():
            self.__myTree.delete(item)
        
        # Update extension list
        current_ext = self.__myExtVar.get()
        extensions = self.__myController.get_available_extensions()
        self.__myExtCombo['values'] = extensions
        if current_ext in extensions:
            self.__myExtVar.set(current_ext)
        else:
            self.__myExtVar.set('All')
        
        # Get filter values
        filters = {
            'event_type': self.__myEventTypeVar.get(),
            'extension': self.__myExtVar.get(),
            'date_range': self.__myDateVar.get()
        }
        print(f"Applied filters: {filters}")
        
        results = self.__myController.get_filtered_events(filters)
        print(f"Query returned {len(results) if results else 0} results")
        
        if results:
            for event in results:
                try:
                    file_path = event[2]
                    filename = os.path.basename(file_path)
                    extension = os.path.splitext(filename)[1] or "(none)"
                    display_path = file_path.replace(os.getcwd() + os.sep, '')
                    
                    self.__myTree.insert('', 0, values=(
                        filename,
                        extension,
                        display_path,
                        event[4],
                        event[5]
                    ))
                except Exception as e:
                    print(f"Error processing event: {e}")
    
        self.__db_results = results

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        if self.__myController.export_to_csv(file_path, self.__db_results):
            messagebox.showinfo("Success", f"CSV exported to {file_path}")
            self.__last_exported_file = file_path
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
            if self.__myController.reset_database():
                messagebox.showinfo("Success", "Database has been reset successfully")
                self.__perform_query()
            else:
                messagebox.showerror("Error", "Failed to reset database")