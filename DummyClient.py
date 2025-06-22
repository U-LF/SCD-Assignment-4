import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"


def send_request(method, endpoint, payload, output_text):
    try:
        url = f"{BASE_URL}{endpoint}"
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=payload)
        elif method == 'PUT':
            response = requests.put(url, json=payload)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            raise ValueError("Unsupported HTTP method")

        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Status Code: {response.status_code}\n")
        output_text.insert(tk.END, f"Response: {response.text}")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Request Error", f"Error: {str(e)}")


def create_tab_students(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Manage Students")

    form_frame = ttk.LabelFrame(frame, text="Student Operations", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Add", command=lambda: send_request('POST', "/students", {
        "name": name_entry.get()
    }, output)).grid(row=0, column=0, padx=5)

    ttk.Button(btn_frame, text="Update", command=lambda: send_request('PUT', f"/students/{id_entry.get()}", {
        "name": name_entry.get()
    }, output)).grid(row=0, column=1, padx=5)

    ttk.Button(btn_frame, text="Delete", command=lambda: send_request('DELETE', f"/students/{id_entry.get()}", None, output)).grid(row=0, column=2, padx=5)

    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=10)
    output_frame.grid(row=1, column=0, sticky="nsew")

    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.pack(fill="both", expand=True)


def create_tab_attendance(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Mark Attendance")

    form_frame = ttk.LabelFrame(frame, text="Attendance Marking", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    date_entry = ttk.Entry(form_frame)
    date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(form_frame, text="Status (present/absent):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    status_entry = ttk.Entry(form_frame)
    status_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Mark Attendance", command=lambda: send_request('POST', "/attendance", {
        "student_id": int(id_entry.get()),
        "date": date_entry.get(),
        "status": status_entry.get()
    }, output)).grid(row=0, column=0, padx=5)

    ttk.Button(btn_frame, text="Update Attendance", command=lambda: send_request('PUT', "/attendance", {
        "student_id": int(id_entry.get()),
        "date": date_entry.get(),
        "status": status_entry.get()
    }, output)).grid(row=0, column=1, padx=5)

    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=10)
    output_frame.grid(row=1, column=0, sticky="nsew")

    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.pack(fill="both", expand=True)


def create_tab_view_attendance(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="View Attendance")

    btn = ttk.Button(frame, text="Load All Attendance", command=lambda: send_request('GET', "/attendance", None, output))
    btn.pack(pady=10)

    output = scrolledtext.ScrolledText(frame, height=15, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.pack(fill="both", expand=True, padx=5, pady=5)


def main():
    root = tk.Tk()
    root.title("Attendance Management Client")
    root.geometry("600x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    create_tab_students(notebook)
    create_tab_attendance(notebook)
    create_tab_view_attendance(notebook)

    root.mainloop()


if __name__ == "__main__":
    main()
