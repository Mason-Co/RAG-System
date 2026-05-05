import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.doc_loader import DocumentLoader
from src.rag_system import RAGSystem


class RAGCustomTkApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RAG System - CustomTkinter")
        self.geometry("1000x700")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.documents_path = "data/documents"
        os.makedirs(self.documents_path, exist_ok=True)

        self.loader = DocumentLoader(self.documents_path)
        self.rag = RAGSystem()

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=12, pady=12)

        self.system_tab = self.tabview.add("System")
        self.documents_tab = self.tabview.add("Documents")

        self._build_system_tab()
        self._build_documents_tab()
        self.refresh_documents_list()

    def _build_system_tab(self):
        self.system_tab.grid_rowconfigure(0, weight=1)
        self.system_tab.grid_columnconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self.system_tab, state="disabled")
        self.chat_box.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=12, pady=12)

        self.question_entry = ctk.CTkEntry(
            self.system_tab,
            placeholder_text="Ask a question about the selected documents...",
        )
        self.question_entry.grid(row=1, column=0, sticky="ew", padx=(12, 6), pady=(0, 12))
        self.question_entry.bind("<Return>", lambda _event: self.ask_question())

        ask_button = ctk.CTkButton(self.system_tab, text="Ask", command=self.ask_question)
        ask_button.grid(row=1, column=1, sticky="ew", padx=(6, 12), pady=(0, 12))

    def _build_documents_tab(self):
        self.documents_tab.grid_rowconfigure(1, weight=1)
        self.documents_tab.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self.documents_tab, text="Select one or more documents to include:")
        label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.doc_listbox = tk.Listbox(
            self.documents_tab,
            selectmode=tk.MULTIPLE,
            exportselection=False,
            activestyle="none",
            bg="#1f1f1f",
            fg="#f0f0f0",
            selectbackground="#1f6aa5",
            selectforeground="#ffffff",
            borderwidth=0,
            highlightthickness=0,
        )
        self.doc_listbox.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        button_frame = ctk.CTkFrame(self.documents_tab, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 12))

        submit_button = ctk.CTkButton(button_frame, text="Submit", command=self.submit_document)
        submit_button.pack(side="left", padx=(0, 8))

        run_button = ctk.CTkButton(button_frame, text="Run", command=self.run_selected_documents)
        run_button.pack(side="left")

    def append_chat(self, speaker: str, text: str):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{speaker}: {text}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            return

        self.question_entry.delete(0, "end")
        self.append_chat("User", question)

        try:
            answer = self.rag.answer_question(question)
            self.append_chat("Assistant", answer)
        except Exception as error:
            self.append_chat("System", f"Error: {error}")

    def refresh_documents_list(self, select_name: str | None = None):
        self.doc_listbox.delete(0, "end")
        names = sorted(self.loader.list_document_names())
        for index, name in enumerate(names):
            self.doc_listbox.insert("end", name)
            if select_name and name == select_name:
                self.doc_listbox.selection_set(index)
                self.doc_listbox.see(index)

    def submit_document(self):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("Supported files", "*.txt *.pdf"),
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        filename = os.path.basename(file_path)
        target_path = os.path.join(self.documents_path, filename)

        if os.path.exists(target_path):
            should_overwrite = messagebox.askyesno(
                "Overwrite File?",
                f"{filename} already exists. Overwrite it?",
            )
            if not should_overwrite:
                return

        try:
            shutil.copy2(file_path, target_path)
            self.refresh_documents_list(select_name=filename)
            messagebox.showinfo("Success", f"Added {filename}")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to add document:\n{error}")

    def run_selected_documents(self):
        selected_indices = self.doc_listbox.curselection()
        selected_names = [self.doc_listbox.get(i) for i in selected_indices]

        if not selected_names:
            messagebox.showwarning("No Selection", "Select at least one document, then click Run.")
            return

        try:
            self.rag.set_active_documents(selected_names)
            messagebox.showinfo("Index Ready", f"Indexed {len(selected_names)} selected document(s).")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to index selected documents:\n{error}")


if __name__ == "__main__":
    app = RAGCustomTkApp()
    app.mainloop()