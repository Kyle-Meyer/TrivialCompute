import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import psycopg2
from PIL import Image, ImageTk
import base64
import io
from databaseSetup import setup_database_and_execute_scripts

# Database connection
def db_connect():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname='trivialCompute',user='postgres',password='postgres',host='localhost')
        conn.autocommit = True
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Functions to interact with the database
def get_categories(cur):
    cur.execute("SELECT id, name FROM categories")
    return cur.fetchall()

def get_questions_by_category(cur, category):
    cur.execute("SELECT id, question, answer, \"imageBase64\" FROM questions WHERE category=%s", (category,))
    return cur.fetchall()

def get_category_name_by_category_id(cur, category_id):
    cur.execute("SELECT name FROM categories WHERE id=%s", (category_id,))
    return cur.fetchall()

def add_category(cur, conn, name):
    try:
        cur.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        messagebox.showinfo("Success", "Category added successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to add category: {e}")
        conn.rollback()

def add_question(cur, conn, question, answer, category, imageBase64):
    try:
        cur.execute("INSERT INTO questions (question, answer, category, \"imageBase64\") VALUES (%s, %s, %s, %s)", (question, answer, category, imageBase64))
        messagebox.showinfo("Success", "Question added successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to add question: {e}")
        conn.rollback()

def remove_question(cur, conn, question_id):
    try:
        cur.execute("DELETE FROM questions WHERE id=%s", (question_id,))
        messagebox.showinfo("Success", "Question removed successfully!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Failed to remove question: {e}")
        conn.rollback()

def remove_category(cur, conn, category_id): 
    try:
        name = get_category_name_by_category_id(cur,category_id)[0][0]
        cur.execute("DELETE FROM questions WHERE category=%s", (name,)) 
        cur.execute("DELETE FROM categories WHERE id=%s", (category_id,)) 
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
        self.conn = db_connect()

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

        self.display_categories_button = ttk.Button(self.category_frame, text="Initialize/Reset Database", command=self.init_db)
        self.display_categories_button.pack(pady=10)

        self.display_categories_button = ttk.Button(self.category_frame, text="Display Categories", command=self.display_categories)
        self.display_categories_button.pack(pady=10)

        self.category_list = tk.Listbox(self.category_frame, font=('Arial', 12))
        self.category_list.pack(pady=10)
        self.category_list.bind('<<ListboxSelect>>', self.on_category_select)
                
        self.add_category_button = ttk.Button(self.category_frame, text="Add Category", command=self.show_add_category)
        self.add_category_button.pack(pady=10)

        self.remove_category_button = ttk.Button(self.category_frame, text="Remove Category", command=self.show_remove_category) 
        self.remove_category_button.pack(pady=10) 

        self.selected_category = None 

    def init_db(self):
        setup_database_and_execute_scripts()
        self.conn = db_connect()
        self.display_categories()

    def display_categories(self):
        if self.conn == None:
            messagebox.showerror("Error", "Database connection error. Try resetting it.")
        else:
            self.category_list.delete(0, tk.END)
            categories = get_categories(self.conn[1])
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
        
        questions = get_questions_by_category(self.conn[1], category)
        ttk.Label(self.action_frame, text=f"Questions for {category}:", font=('Arial', 14)).pack(pady=10)
        
        # Create a frame with a scrollbar and canvas for questions
        canvas_frame = ttk.Frame(self.action_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        # Create a scrollable window on the canvas
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)

        for child in scrollable_frame.winfo_children():
            child.configure(background="white")

        # Insert questions and images into the scrollable frame
        for question_id, question, answer, imageBase64 in questions:
            question_frame = ttk.Frame(scrollable_frame)
            question_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(question_frame, text=f"ID: {question_id}", font=('Arial', 12)).pack(anchor=tk.W)
            ttk.Label(question_frame, text=f"Q: {question}", font=('Arial', 12)).pack(anchor=tk.W)
            ttk.Label(question_frame, text=f"A: {answer}", font=('Arial', 12)).pack(anchor=tk.W)
            
            # Handle image display
            if imageBase64:
                image_data = base64.b64decode(imageBase64)
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(image)
                image_label = ttk.Label(question_frame, image=photo)
                image_label.pack(pady=5)
                image_label.photo = photo  # Keep a reference to avoid garbage collection
        
        self.add_question_button = ttk.Button(self.action_frame, text="Add Question", command=self.show_add_question) 
        self.add_question_button.pack(pady=10) 

        self.remove_question_button = ttk.Button(self.action_frame, text="Remove Question", command=self.show_remove_question) 
        self.remove_question_button.pack(pady=10)

    def show_add_category(self):
        if self.conn == None:
            messagebox.showerror("Error", "Database connection error. Try resetting it.")
        else:
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
            add_category(self.conn[1], self.conn[0], category_name)
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
        
        self.upload_button = ttk.Button(self.action_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.image_label = ttk.Label(self.action_frame)
        self.image_label.pack(pady=10)
        
        self.delete_image_button = ttk.Button(self.action_frame, text="Delete Image", command=self.delete_image, state=tk.DISABLED)
        self.delete_image_button.pack(pady=10)
        
        self.submit_question_button = ttk.Button(self.action_frame, text="Submit", command=self.submit_question)
        self.submit_question_button.pack(side=tk.BOTTOM, pady=10)

        self.image_base64 = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as img_file:
                img_data = img_file.read()
                self.image_base64 = base64.b64encode(img_data).decode('utf-8')
                
            self.show_image_thumbnail(file_path)
            self.upload_button.pack_forget()  # Hide the upload button
            self.delete_image_button.config(state=tk.NORMAL)
            self.delete_image_button.pack(pady=10)  # Ensure delete button is visible

    def show_image_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.photo = photo

    def delete_image(self):
        self.image_base64 = None
        self.image_label.config(image='')
        self.delete_image_button.pack_forget()  # Hide the delete button
        self.upload_button.pack(pady=10)  # Show the upload button
        self.submit_question_button.pack(side=tk.BOTTOM, pady=10)  # Ensure submit button is at the bottom

    def submit_question(self):
        question_text = self.new_question_entry.get()
        answer_text = self.new_answer_entry.get()
        
        if question_text and answer_text:
            # Save the question along with its image
            add_question(self.conn[1], self.conn[0], question_text, answer_text, self.selected_category, self.image_base64)
            self.display_questions(self.selected_category)
                
            # Update the UI immediately after submission
            self.display_questions(self.selected_category)
            self.update_idletasks()  # Ensure UI is updated
        else:
            messagebox.showerror("Error", "Question and answer cannot be empty!")


    def show_remove_question(self):
        selected_question = simpledialog.askinteger("Remove Question", "Enter the ID of the question to remove:")
        if selected_question is not None:
            remove_question(self.conn[1], self.conn[0], selected_question)
            self.display_questions(self.selected_category)

    def show_remove_category(self): 
        if self.conn == None:
            messagebox.showerror("Error", "Database connection error. Try resetting it.")
        else:
            category_id = simpledialog.askinteger("Remove Category", "Enter the ID of the category to remove:") 
            if category_id is not None: 
                remove_category(self.conn[1], self.conn[0], category_id) 
                self.display_categories() 
                self.selected_category = None 
                for widget in self.action_frame.winfo_children(): 
                    widget.destroy() 

if __name__ == "__main__": 
    app = App() 
    app.mainloop()