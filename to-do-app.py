# Code Logic by Ayush Prabhakhar

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILE="productivity_tasks.json"

def load_tasks():
    if os.path.exists(FILE):
        try:
            with open(FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks():
    try:
        with open(FILE,"w",encoding="utf-8") as f:
            json.dump(tasks,f,indent=2)
    except:
        pass

def filtered_tasks():
    q=search_var.get().lower().strip()
    if not q:
        return list(range(len(tasks)))
    res=[]
    for i,t in enumerate(tasks):
        s=(t["text"]+" "+t["priority"]+" "+t["due"]+" "+t["created"]).lower()
        if q in s:
            res.append(i)
    return res

def refresh():
    for r in tree.get_children():
        tree.delete(r)
    mapping.clear()
    for idx in filtered_tasks():
        t=tasks[idx]
        iid=tree.insert("",tk.END,values=(len(mapping)+1,t["text"],t["priority"],t["due"],t["created"]))
        mapping[iid]=idx

def add_task(event=None):
    text=task_var.get().strip()
    if not text:
        return
    t={"text":text,"priority":priority_var.get(),"due":due_var.get().strip(),"created":datetime.now().strftime("%Y-%m-%d %H:%M")}
    tasks.append(t)
    task_var.set("")
    due_var.set("")
    save_tasks()
    refresh()

def selected_index():
    sel=tree.selection()
    if not sel:
        return None
    iid=sel[0]
    return mapping.get(iid)

def delete_task(event=None):
    i=selected_index()
    if i is None:
        return
    try:
        tasks.pop(i)
        save_tasks()
        refresh()
    except:
        pass

def clear_all():
    if not tasks:
        return
    if messagebox.askyesno("Confirm","Clear all tasks?"):
        tasks.clear()
        save_tasks()
        refresh()

def edit_task():
    i=selected_index()
    if i is None:
        return
    top=tk.Toplevel(root)
    top.title("Edit Task")
    top.transient(root)
    frm=tk.Frame(top,padx=10,pady=10)
    frm.pack(fill="both",expand=True)
    tk.Label(frm,text="Task").grid(row=0,column=0,columnspan=2,sticky="w")
    tv=tk.StringVar(value=tasks[i]["text"])
    e1=tk.Entry(frm,textvariable=tv,width=40)
    e1.grid(row=1,column=0,columnspan=2,sticky="ew",pady=(0,8))
    tk.Label(frm,text="Priority").grid(row=2,column=0,sticky="w")
    tk.Label(frm,text="Due Date").grid(row=2,column=1,sticky="w")
    pv=tk.StringVar(value=tasks[i]["priority"])
    cb=ttk.Combobox(frm,values=["Low","Medium","High"],textvariable=pv,state="readonly",width=12)
    cb.grid(row=3,column=0,sticky="ew",pady=(0,8))
    dv=tk.StringVar(value=tasks[i]["due"])
    e2=tk.Entry(frm,textvariable=dv,width=15)
    e2.grid(row=3,column=1,sticky="ew",pady=(0,8))
    def save_edit():
        txt=tv.get().strip()
        if not txt:
            return
        tasks[i]["text"]=txt
        tasks[i]["priority"]=pv.get()
        tasks[i]["due"]=dv.get().strip()
        save_tasks()
        refresh()
        top.destroy()
    tk.Button(frm,text="Save",command=save_edit).grid(row=4,column=0,columnspan=2,sticky="ew")
    frm.columnconfigure(0,weight=1)
    frm.columnconfigure(1,weight=1)
    e1.focus_set()

def focus_search(event=None):
    search_entry.focus_set()
    return "break"

root=tk.Tk()
root.title("To-Do Productivity Manager By Ayush Prabhakhar")
root.geometry("760x560")

main=tk.Frame(root,padx=10,pady=10)
main.pack(fill="both",expand=True)

top=tk.Frame(main)
top.pack(fill="x")

tk.Label(top,text="Task").grid(row=0,column=0,sticky="w")
tk.Label(top,text="Priority").grid(row=0,column=1,sticky="w")
tk.Label(top,text="Due Date").grid(row=0,column=2,sticky="w")

task_var=tk.StringVar()
due_var=tk.StringVar()
priority_var=tk.StringVar(value="Medium")
search_var=tk.StringVar()

task_entry=tk.Entry(top,textvariable=task_var)
task_entry.grid(row=1,column=0,sticky="ew",padx=(0,5))
priority_box=ttk.Combobox(top,values=["Low","Medium","High"],textvariable=priority_var,state="readonly",width=12)
priority_box.grid(row=1,column=1,sticky="ew",padx=(0,5))
due_entry=tk.Entry(top,textvariable=due_var,width=14)
due_entry.grid(row=1,column=2,sticky="ew",padx=(0,5))
tk.Button(top,text="Add Task",command=add_task).grid(row=1,column=3,sticky="ew")

search_frame=tk.Frame(main)
search_frame.pack(fill="x",pady=(10,5))
tk.Label(search_frame,text="Search").pack(side="left")
search_entry=tk.Entry(search_frame,textvariable=search_var)
search_entry.pack(side="left",fill="x",expand=True,padx=(6,0))

mid=tk.Frame(main)
mid.pack(fill="both",expand=True)

tree=ttk.Treeview(mid,columns=("n","task","priority","due","created"),show="headings")
tree.heading("n",text="#")
tree.heading("task",text="Task")
tree.heading("priority",text="Priority")
tree.heading("due",text="Due Date")
tree.heading("created",text="Created")
tree.column("n",width=40,anchor="center")
tree.column("task",anchor="w")
tree.column("priority",width=90,anchor="center")
tree.column("due",width=110,anchor="center")
tree.column("created",width=140,anchor="center")
vs=ttk.Scrollbar(mid,orient="vertical",command=tree.yview)
tree.configure(yscroll=vs.set)
tree.pack(side="left",fill="both",expand=True)
vs.pack(side="right",fill="y")

bot=tk.Frame(main)
bot.pack(fill="x",pady=(8,0))
tk.Button(bot,text="Edit Selected",command=edit_task).pack(side="left",fill="x",expand=True,padx=(0,5))
tk.Button(bot,text="Delete Selected",command=delete_task).pack(side="left",fill="x",expand=True,padx=(0,5))
tk.Button(bot,text="Clear All",command=clear_all).pack(side="left",fill="x",expand=True)

top.columnconfigure(0,weight=1)

tasks=load_tasks()
mapping={}
refresh()

search_var.trace_add("write",lambda *a: refresh())

root.bind("<Return>",add_task)
root.bind("<Delete>",delete_task)
root.bind("<Control-f>",focus_search)

task_entry.focus_set()
root.mainloop()