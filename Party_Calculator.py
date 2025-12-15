import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import sqlite3
from datetime import datetime

main = tk.Tk()
main.title("Party Calculator 🎉")
main.geometry("350x550")
main.configure(bg="#f0f0f0")
main.resizable(False, False)

# Database
conn = sqlite3.connect('calc.db')
conn.execute('CREATE TABLE IF NOT EXISTS history (expr TEXT, result TEXT, time TEXT)')
conn.commit()

def save(expr, res):
    conn.execute('INSERT INTO history VALUES (?, ?, ?)', (expr, res, str(datetime.now())))
    conn.commit()

def get_history():
    return conn.execute('SELECT * FROM history ORDER BY time DESC LIMIT 50').fetchall()

def clear_history():
    conn.execute('DELETE FROM history')
    conn.commit()
    messagebox.showinfo("Done", "History cleared")

# Menu
menu = tk.Menu(main)
main.config(menu=menu)

file = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file)
file.add_command(label="View History", command=lambda: show_hist())
file.add_command(label="Clear History", command=clear_history)
file.add_command(label="Exit", command=main.quit)

view = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view)
view.add_command(label="Reset", command=lambda: arrange(False))
view.add_command(label="Party!", command=lambda: party())

# Display
display = tk.Entry(main, font=("Arial", 24), justify="right", bd=10)
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

expr = ""

def click(val):
    global expr
    expr += str(val)
    display.delete(0, tk.END)
    display.insert(0, expr)

def clear():
    global expr
    expr = ""
    display.delete(0, tk.END)

def calc():
    global expr
    try:
        res = str(eval(expr))
        save(expr, res)
        display.delete(0, tk.END)
        display.insert(0, res)
        expr = res
    except:
        messagebox.showerror("Error", "Invalid")
        expr = ""
        display.delete(0, tk.END)

# Buttons
btns = ['1','2','3','/','4','5','6','*','7','8','9','-','C','0','=','+']
widgets = []

for txt in btns:
    if txt == '=':
        b = tk.Button(main, text=txt, font=("Arial", 18, "bold"), 
                     bg="#4CAF50", fg="white", command=calc)
    elif txt == 'C':
        b = tk.Button(main, text=txt, font=("Arial", 18, "bold"),
                     bg="#f44336", fg="white", command=clear)
    else:
        b = tk.Button(main, text=txt, font=("Arial", 18), bg="white",
                     command=lambda x=txt: click(x))
    widgets.append(b)

def arrange(rand=False):
    pos = [(r, c) for r in range(1, 5) for c in range(4)]
    if rand:
        random.shuffle(pos)
    for i, b in enumerate(widgets):
        r, c = pos[i]
        b.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

def party(*colors):
    global expr
    arrange(True)
    cols = colors if colors else ["#FFB6C1","#FFD700","#98FB98","#87CEEB","#DDA0DD"]
    main.configure(bg=random.choice(cols))
    display.configure(bg=random.choice(["#FFFFFF","#FFFFE0","#F0FFF0"]))
    display.delete(0, tk.END)
    display.insert(0, "Party Time!")
    expr = ""

def show_hist():
    win = tk.Toplevel(main)
    win.title("History")
    win.geometry("500x400")
    
    txt = scrolledtext.ScrolledText(win, font=("Courier", 10))
    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    hist = get_history()
    if hist:
        for expr, res, time in hist:
            txt.insert(tk.END, f"{expr} = {res}  ({time[:19]})\n")
    else:
        txt.insert(tk.END, "No history yet")
    
    txt.config(state=tk.DISABLED)

arrange(False)

party_btn = tk.Button(main, text="🎉 PARTY 🎉", font=("Arial", 14, "bold"),
                     bg="#FF1493", fg="white", command=party)
party_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

for i in range(6):
    main.grid_rowconfigure(i, weight=1)
for i in range(4):
    main.grid_columnconfigure(i, weight=1)

main.mainloop()