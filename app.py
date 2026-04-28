import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from src.rag_system import RAGSystem
from src.doc_loader import DocumentLoader
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil
import os

class RAGDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG System")
        self.root.geometry("950x700")

        self.loader = DocumentLoader("data/documents")
        self.rag = RAGSystem()  # initially no documents loaded

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # ---------- System tab ----------
        self.system_tab = ttk.Frame(notebook)
        notebook.add(self.system_tab, text="System")

        self.chat_box = ScrolledText(self.system_tab, wrap="word", state="disabled", height=28)
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)

        bottom = ttk.Frame(self.system_tab)
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        self.question_var = tk.StringVar()
        self.question_entry = ttk.Entry(bottom, textvariable=self.question_var)
        self.question_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.question_entry.bind("<Return>", lambda e: self.ask_question())

        ask_btn = ttk.Button(bottom, text="Ask", command=self.ask_question)
        ask_btn.pack(side="right")

        # ---------- Documents tab ----------
        self.docs_tab = ttk.Frame(notebook)
        notebook.add(self.docs_tab, text="Documents")

        ttk.Label(self.docs_tab, text="Select documents to include:").pack(anchor="w", padx=10, pady=(10, 6))

        self.listbox = tk.Listbox(self.docs_tab, selectmode=tk.MULTIPLE, exportselection=False, height=18)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for name in sorted(self.loader.list_document_names()):
            self.listbox.insert(tk.END, name)

        run_btn = ttk.Button(self.docs_tab, text="Run", command=self.apply_selected_documents)
        run_btn.pack(padx=10, pady=(0, 12), anchor="w")

        submit_btn = ttk.Button(self.docs_tab, text="Submit", command=self.submit_document)
        submit_btn.pack(padx=10, pady=(0, 8), anchor="w")

    def append_chat(self, speaker, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, f"{speaker}: {text}\n\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see(tk.END)

    def ask_question(self):
        q = self.question_var.get().strip()
        if not q:
            return
        self.question_var.set("")
        self.append_chat("User", q)
        try:
            answer = self.rag.answer_question(q)
            self.append_chat("Assistant", answer)
        except Exception as e:
            self.append_chat("System", f"Error: {e}")

    def apply_selected_documents(self):
        selected_indices = self.listbox.curselection()
        selected_names = [self.listbox.get(i) for i in selected_indices]

        if not selected_names:
            messagebox.showwarning("No Selection", "Please select at least one document.")
            return

        try:
            # implement this method in RAGSystem
            self.rag.set_active_documents(selected_names)
            messagebox.showinfo("Success", f"Indexed {len(selected_names)} selected document(s).")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_document(self):
        file_path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[
                ("Supported files", "*.txt *.pdf"),
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return  # user canceled

        src = Path(file_path)
        dest_dir = Path("data/documents")
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name

        # Optional: prevent silent overwrite
        if dest.exists():
            overwrite = messagebox.askyesno(
                "File exists",
                f"{src.name} already exists. Overwrite?"
            )
            if not overwrite:
                return

        try:
            shutil.copy2(src, dest)
            self.refresh_document_list(select_name=src.name)
            messagebox.showinfo("Success", f"Added: {src.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add file:\n{e}")

    def refresh_document_list(self, select_name=None):
        self.listbox.delete(0, "end")
        names = sorted(self.loader.list_document_names())
        for i, name in enumerate(names):
            self.listbox.insert("end", name)
            if select_name and name == select_name:
                self.listbox.selection_set(i)
                self.listbox.see(i)

if __name__ == "__main__":
    root = tk.Tk()
    app = RAGDesktopApp(root)
    root.mainloop()