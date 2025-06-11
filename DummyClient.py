import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"

def send_request(endpoint, payload, output_text):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Status Code: {response.status_code}\n")
        output_text.insert(tk.END, f"Response: {response.text}")
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Request Error", f"Error: {str(e)}")

def create_tab_register(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Register Player")
    
    form_frame = ttk.LabelFrame(frame, text="Player Registration", padding=(10, 5))
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    # Configure grid weights
    form_frame.columnconfigure(1, weight=1)
    for i in range(4):
        form_frame.rowconfigure(i, weight=1)

    ttk.Label(form_frame, text="Player ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    
    ttk.Label(form_frame, text="Player Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    
    ttk.Button(btn_frame, text="Register", command=lambda: submit_registration(id_entry, name_entry, output)).pack(padx=5, pady=5)
    
    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=(10, 5))
    output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def submit_registration(id_entry, name_entry, output):
        data = {"user_id": id_entry.get(), "name": name_entry.get()}
        send_request("/register", data, output)

def create_tab_board(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Submit Board")
    
    form_frame = ttk.LabelFrame(frame, text="Board Submission", padding=(10, 5))
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    form_frame.columnconfigure(1, weight=1)
    for i in range(4):
        form_frame.rowconfigure(i, weight=1)

    ttk.Label(form_frame, text="Player ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    
    ttk.Label(form_frame, text="Board (comma separated):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    board_entry = ttk.Entry(form_frame)
    board_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    
    ttk.Button(btn_frame, text="Submit Board", command=lambda: submit_board(id_entry, board_entry, output)).pack(padx=5, pady=5)
    
    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=(10, 5))
    output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def submit_board(id_entry, board_entry, output):
        data = {"id": id_entry.get(), "board": board_entry.get()}
        send_request("/submit_board", data, output)

def create_tab_turn(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Take Turn")
    
    form_frame = ttk.LabelFrame(frame, text="Mark Number", padding=(10, 5))
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    form_frame.columnconfigure(1, weight=1)
    for i in range(4):
        form_frame.rowconfigure(i, weight=1)

    ttk.Label(form_frame, text="Player ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    
    ttk.Label(form_frame, text="Number:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    number_entry = ttk.Entry(form_frame)
    number_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    
    ttk.Button(btn_frame, text="Mark Number", command=lambda: submit_turn(id_entry, number_entry, output)).pack(padx=5, pady=5)
    
    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=(10, 5))
    output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def submit_turn(id_entry, number_entry, output):
        data = {"id": id_entry.get(), "number": number_entry.get()}
        send_request("/take_turn", data, output)

def create_tab_win(notebook):
    frame = ttk.Frame(notebook, padding=10)
    notebook.add(frame, text="Declare Win")
    
    form_frame = ttk.LabelFrame(frame, text="Win Declaration", padding=(10, 5))
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    form_frame.columnconfigure(1, weight=1)
    for i in range(3):
        form_frame.rowconfigure(i, weight=1)

    ttk.Label(form_frame, text="Player ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    ttk.Button(btn_frame, text="Declare Win", command=lambda: submit_win(id_entry, output)).pack(padx=5, pady=5)
    
    output_frame = ttk.LabelFrame(frame, text="Server Response", padding=(10, 5))
    output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    output = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
    output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def submit_win(id_entry, output):
        data = {"id": id_entry.get()}
        send_request("/declare_win", data, output)

def main():
    root = tk.Tk()
    root.title("Multiplayer Bingo Client")
    root.geometry("500x500")
    
    # Apply modern theme
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure style
    style.configure("TLabel", padding=5)
    style.configure("TButton", padding=5)
    style.configure("TLabelframe", padding=5)
    style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
    
    # Create notebook with tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create tabs
    create_tab_register(notebook)
    create_tab_board(notebook)
    create_tab_turn(notebook)
    create_tab_win(notebook)
    
    # Status bar
    status_var = tk.StringVar(value="Ready")
    status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()

if __name__ == "__main__":
    main()