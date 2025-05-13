import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class GameStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин игр")
        self.root.geometry("800x600")
        
        self.api_url = "http://localhost:8000/games"
        
        self.create_widgets()
        self.load_games()
    
    def create_widgets(self):
        
        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Title", "Price", "Genre"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Price", text="Цена")
        self.tree.heading("Genre", text="Жанр")
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=200)
        self.tree.column("Price", width=100)
        self.tree.column("Genre", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
       
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        
        ttk.Button(button_frame, text="Обновить", command=self.load_games).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Добавить игру", command=self.add_game_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить игру", command=self.delete_game).pack(side=tk.LEFT, padx=5)
    
    def load_games(self):
        try:
            response = requests.get(self.api_url)
            games = response.json()
            
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            
            for game in games:
                self.tree.insert("", tk.END, values=(
                    game["id"],
                    game["title"],
                    f"${game['price']:.2f}",
                    game["genre"]
                ))
        except Exception as e:
            messagebox.showerror("ошибка!а", f" {str(e)}")
    
    def add_game_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новую игру")
        
        
        ttk.Label(dialog, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        title_entry = ttk.Entry(dialog)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Цена:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        price_entry = ttk.Entry(dialog)
        price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        genre_entry = ttk.Entry(dialog)
        genre_entry.grid(row=2, column=1, padx=5, pady=5)
        
        
        def submit():
            try:
                game_data = {
                    "id": max(game["id"] for game in requests.get(self.api_url).json()) + 1,
                    "title": title_entry.get(),
                    "price": float(price_entry.get()),
                    "genre": genre_entry.get()
                }
                
                response = requests.post(self.api_url, json=game_data)
                if response.status_code == 200:
                    self.load_games()
                    dialog.destroy()
            except Exception as e:
                messagebox.showerror("ОШибкА!", f": {str(e)}")
        
        ttk.Button(dialog, text="Добавить", command=submit).grid(row=3, column=0, columnspan=2, pady=10)
    
    def delete_game(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Какую игру удалить")
            return
        
        game_id = self.tree.item(selected_item)["values"][0]
        
        try:
            
            response = requests.get(self.api_url)
            games = response.json()
            
            
            updated_games = [game for game in games if game["id"] != game_id]
            
           
            global games_db
            games_db = updated_games
            
            self.load_games()
            messagebox.showinfo("Ошибка", "Игра удалена")
        except Exception as e:
            messagebox.showerror("ОШибка", f" {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameStoreApp(root)
    root.mainloop()