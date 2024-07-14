import tkinter as tk
from tkinter import ttk
from databaseSetup import setup_database_and_execute_scripts
from databaseConnection import databaseConnection

def initialize_reset_database():
    setup_database_and_execute_scripts()
    return "Database has been initialized/reset successfully!"

def get_db_categories():
    cats = []
    results = []
    database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
    cats = database.getCategories()
    database.close()
    for cat in cats:
        results.append(str(cat[0])+'. '+cat[1])
    return results

def config_menu():

    def on_initialize_reset_database():
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)  # Clear previous content
        result_text.insert(tk.END, initialize_reset_database())
        result_text.config(state=tk.DISABLED)

    def on_get_categories():
        categories = get_db_categories()
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)  # Clear previous content
        result_text.insert(tk.END, "\n".join(categories))
        result_text.config(state=tk.DISABLED)

        # Update dropdown options with retrieved categories
        for idx, dropdown in enumerate(category_dropdowns):
            dropdown['menu'].delete(0, tk.END)  # Clear previous options
            for category in categories:
                dropdown['menu'].add_command(label=category, command=tk._setit(dropdown_var[idx], category))

    def return_to_start():
        root.destroy()  # Close the current window

    root = tk.Tk()
    root.title("Configuration Menu")

    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Left Frame for Buttons
    left_frame = ttk.Frame(main_frame, padding="10")
    left_frame.grid(row=0, column=0, padx=10, sticky="n")

    title_label = ttk.Label(left_frame, text="Config Menu (Demo Stub)", font=("Arial", 18))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Button(left_frame, text="Initialize/Reset Database", command=on_initialize_reset_database).grid(row=2, column=0, pady=5, padx=10, sticky="we")
    ttk.Button(left_frame, text="Get Categories", command=on_get_categories).grid(row=3, column=0, pady=5, padx=10, sticky="we")

    # Right Frame for Output with Scrollbar
    right_frame = ttk.Frame(main_frame, padding="10")
    right_frame.grid(row=0, column=1, padx=10, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(right_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Result Text (Output)
    result_text = tk.Text(right_frame, wrap="word", font=("Arial", 12), state=tk.DISABLED)
    result_text.pack(padx=10, pady=10, fill="both", expand=True)

    # Configure Scrollbar
    result_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_text.yview)

    # Bottom Frame for Return Button
    bottom_frame = ttk.Frame(root)
    bottom_frame.grid(row=1, column=0, pady=10)

    ttk.Button(bottom_frame, text="Return to Start", command=return_to_start).pack()

    # Dropdown Menus for Categories
    category_dropdowns = []
    category_labels = ["Category 1", "Category 2", "Category 3", "Category 4"]
    dropdown_var = [tk.StringVar() for _ in range(4)]

    for idx, label in enumerate(category_labels):
        ttk.Label(left_frame, text=label).grid(row=4+idx, column=0, pady=5, padx=10, sticky="w")
        dropdown = ttk.OptionMenu(left_frame, dropdown_var[idx], "Select Category", ())
        dropdown.grid(row=4+idx, column=1, pady=5, padx=10, sticky="we")
        category_dropdowns.append(dropdown)

    root.mainloop()

if __name__ == '__main__':
    config_menu()
