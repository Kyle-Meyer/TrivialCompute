import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname='trivialCompute',
    user='postgres',
    password='postgres',
    host='localhost'
)
cur = conn.cursor()

# Functions to interact with the database
def get_categories():
    cur.execute("SELECT id, name FROM categories")
    return cur.fetchall()

def get_questions_by_category(category):
    cur.execute("SELECT id, question, answer FROM questions WHERE category=%s", (category,))
    return cur.fetchall()

def get_category_name_by_category_id(category_id):
    cur.execute("SELECT name FROM categories WHERE id=%s", (category_id,))
    return cur.fetchall()

def add_category(name):
    try:
        cur.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Category added successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to add category: {e}")
        conn.rollback()

def add_question(question, answer, category):
    try:
        cur.execute("INSERT INTO questions (question, answer, category) VALUES (%s, %s, %s)", (question, answer, category))
        conn.commit()
        messagebox.showinfo("Success", "Question added successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to add question: {e}")
        conn.rollback()

def remove_question(question_id):
    try:
        cur.execute("DELETE FROM questions WHERE id=%s", (question_id,))
        conn.commit()
        messagebox.showinfo("Success", "Question removed successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to remove question: {e}")
        conn.rollback()

def remove_category(category_id): 
    try:
        name = get_category_name_by_category_id(category_id)[0][0]
        cur.execute("DELETE FROM questions WHERE category=%s", (name,)) 
        cur.execute("DELETE FROM categories WHERE id=%s", (category_id,)) 
        conn.commit() 
        messagebox.showinfo("Success", "Category and associated questions removed successfully!") 
    except psycopg2.Error as e: 
        messagebox.showerror("Error", f"Failed to remove category and associated questions: {e}") 
        conn.rollback() 

# Main application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Database Manager")
        self.geometry("1280x720")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Frame for categories
        self.category_frame = ttk.Frame(self, padding="10")
        self.category_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Load and display the image (Replace with your smaller image file path)
        self.image = tk.PhotoImage(file="brainwavebuilder.png")
        self.image_label = tk.Label(self.category_frame, image=self.image)
        self.image_label.pack(pady=10)

        # Frame for category actions
        self.action_frame = ttk.Frame(self, padding="10")
        self.action_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.display_categories_button = ttk.Button(self.category_frame, text="Display Categories", command=self.display_categories)
        self.display_categories_button.pack(pady=10)
                
        self.add_category_button = ttk.Button(self.category_frame, text="Add Category", command=self.show_add_category)
        self.add_category_button.pack(pady=10)
        
        self.category_list = tk.Listbox(self.category_frame, font=('Arial', 12))
        self.category_list.pack(pady=10)
        self.category_list.bind('<<ListboxSelect>>', self.on_category_select)

        self.remove_category_button = ttk.Button(self.category_frame, text="Remove Category", command=self.show_remove_category) 
        self.remove_category_button.pack(pady=10) 

        self.selected_category = None 

    def display_categories(self):
        self.category_list.delete(0, tk.END)
        categories = get_categories()
        for id, name in categories:
            self.category_list.insert(tk.END, f"{id}: {name}")

    def on_category_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_category = event.widget.get(index).split(':')[1].strip()
            self.display_questions(self.selected_category)

    def display_questions(self, category):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        
        questions = get_questions_by_category(category)
        ttk.Label(self.action_frame, text=f"Questions for {category}:", font=('Arial', 14)).pack(pady=10)
        
        # Create a frame with a scrollbar and listbox for questions 
        listbox_frame = ttk.Frame(self.action_frame) 
        listbox_frame.pack(fill=tk.BOTH, expand=True) 
        scrollbar = ttk.Scrollbar(listbox_frame) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        self.question_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=('Arial', 12)) 
        self.question_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
        scrollbar.config(command=self.question_listbox.yview) 

        for question_id, question, answer in questions: 
            self.question_listbox.insert(tk.END, f"ID: {question_id}")
            self.question_listbox.insert(tk.END, f"Q: {question}")
            self.question_listbox.insert(tk.END, f"A: {answer}")
            self.question_listbox.insert(tk.END, "\n")

        self.add_question_button = ttk.Button(self.action_frame, text="Add Question", command=self.show_add_question) 
        self.add_question_button.pack(pady=10) 

        self.remove_question_button = ttk.Button(self.action_frame, text="Remove Question", command=self.show_remove_question) 
        self.remove_question_button.pack(pady=10) 

    def show_add_category(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.action_frame, text="Enter new category name:", font=('Arial', 14)).pack(pady=10)
        self.new_category_entry = ttk.Entry(self.action_frame, font=('Arial', 12))
        self.new_category_entry.pack(pady=10)
        
        self.submit_category_button = ttk.Button(self.action_frame, text="Submit", command=self.submit_category)
        self.submit_category_button.pack(pady=10)
    
    def submit_category(self):
        category_name = self.new_category_entry.get()
        if category_name:
            add_category(category_name)
            self.new_category_entry.delete(0, tk.END)
            self.display_categories()
        else:
            messagebox.showerror("Error", "Category name cannot be empty!")

    def show_add_question(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy() 
        
        ttk.Label(self.action_frame, text="Enter new question:", font=('Arial', 14)).pack(pady=10)
        self.new_question_entry = ttk.Entry(self.action_frame, font=('Arial', 12))
        self.new_question_entry.pack(pady=10)
        
        ttk.Label(self.action_frame, text="Enter answer:", font=('Arial', 14)).pack(pady=10)
        self.new_answer_entry = ttk.Entry(self.action_frame, font=('Arial', 12))
        self.new_answer_entry.pack(pady=10)
        
        self.submit_question_button = ttk.Button(self.action_frame, text="Submit", command=self.submit_question)
        self.submit_question_button.pack(pady=10)
    
    def submit_question(self):
        question_text = self.new_question_entry.get()
        answer_text = self.new_answer_entry.get()
        if question_text and answer_text:
            add_question(question_text, answer_text, self.selected_category)
            self.display_questions(self.selected_category)
        else:
            messagebox.showerror("Error", "Question and answer cannot be empty!")
    
    def show_remove_question(self):
        selected_question = simpledialog.askinteger("Remove Question", "Enter the ID of the question to remove:")
        if selected_question is not None:
            remove_question(selected_question)
            self.display_questions(self.selected_category)

    def show_remove_category(self): 
        category_id = simpledialog.askinteger("Remove Category", "Enter the ID of the category to remove:") 
        if category_id is not None: 
            remove_category(category_id) 
            self.display_categories() 
            self.selected_category = None 
            for widget in self.action_frame.winfo_children(): 
                widget.destroy() 

if __name__ == "__main__": 
    app = App() 
    app.mainloop()