import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from email import EmailSender
import csv

class QueryWindow(tk.Toplevel):
    def __init__(self, master, db_results):
        super().__init__(master)
        self.title("QueryForm")
        self.geometry("800x400")

        self.db_results = db_results  # [(id, ext, filename, path, event, dt), ...]

        # 테이블
        columns = ("ID", "Extension", "Filename", "PATH", "Event", "Date/Time")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.populate_table()

        # 하단 기능 버튼들
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        # Export to CSV
        export_btn = tk.Button(bottom_frame, text="Export to CSV", command=self.export_to_csv)
        export_btn.grid(row=0, column=0, padx=5)

        # 이메일 입력 + 전송
        tk.Label(bottom_frame, text="Recipient Email:").grid(row=0, column=1, padx=5)
        self.email_entry = tk.Entry(bottom_frame, width=30)
        self.email_entry.grid(row=0, column=2, padx=5)

        send_btn = tk.Button(bottom_frame, text="Send Email", command=self.send_email)
        send_btn.grid(row=0, column=3, padx=5)

    def populate_table(self):
        for row in self.db_results:
            self.tree.insert("", "end", values=row)

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
            self.last_exported_file = file_path  # 저장 위치 기억

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
            # 실제 전송
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
