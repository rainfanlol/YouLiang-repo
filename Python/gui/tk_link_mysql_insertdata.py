import tkinter as tk
import mysql.connector
class PartManager:
    def __init__(self):
        # Create database connection and cursor
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="****",
            database="testdb"
        )
        self.cursor = self.conn.cursor()
         # Create parts table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                part_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                part_name VARCHAR(255),
                part_description VARCHAR(255),
                part_count INT(11)
            )
        ''')
         # Create GUI
        self.scale = 1.2
        self.font_scale = 14  # 字體放大倍數
        self.root = tk.Tk()
        self.root.title("Part Manager")
         # Scale the size of the window
        self.window_width = 400
        self.window_height = 600
        screen_width = self.root.winfo_screenwidth()  # 螢幕寬度
        screen_height = self.root.winfo_screenheight()  # 螢幕高度
        x = int((screen_width - self.window_width) / 2)  # 計算視窗左上角的x座標
        y = int((screen_height - self.window_height) / 2)  # 計算視窗左上角的y座標
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x, y))  # 設定視窗大小和位置
        self.root.resizable(0, 0)  # 固定大小
         # Create part name label and entry field
        tk.Label(self.root, text="Part Name:", font=("Helvetica", int(self.font_scale*self.scale))).grid(row=0, column=0, padx=5, pady=5)
        self.part_name_entry = tk.Entry(self.root, font=("Helvetica", int(self.font_scale*self.scale)))
        self.part_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
         # Create part description label and entry field
        tk.Label(self.root, text="Part Description:", font=("Helvetica", int(self.font_scale*self.scale))).grid(row=1, column=0, padx=5, pady=5)
        self.part_description_entry = tk.Entry(self.root, font=("Helvetica", int(self.font_scale*self.scale)))
        self.part_description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
         # Create part count label and entry field
        tk.Label(self.root, text="Part Count:", font=("Helvetica", int(self.font_scale*self.scale))).grid(row=2, column=0, padx=5, pady=5)
        self.part_count_entry = tk.Entry(self.root, font=("Helvetica", int(self.font_scale*self.scale)))
        self.part_count_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
         # Create add part button
        add_part_button = tk.Button(self.root, text="Add Part", command=self.add_part, font=("Helvetica", int(self.font_scale*self.scale)))
        add_part_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # 水平置中並且左右邊緣也置中
         # Create parts listbox
        self.parts_listbox = tk.Listbox(self.root, font=("Helvetica", int(self.font_scale*self.scale)))
        self.parts_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.refresh_parts_list()
         # Create exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Helvetica", int(self.font_scale*self.scale)))
        exit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # 水平置中並且左右邊緣也置中
        self.root.mainloop()
    def add_part(self):
        part_name = self.part_name_entry.get()
        part_description = self.part_description_entry.get()
        part_count = int(self.part_count_entry.get())
         # Insert part into database
        self.cursor.execute('''
            INSERT INTO parts (part_name, part_description, part_count)
            VALUES (%s, %s, %s)
        ''', (part_name, part_description, part_count))
        self.conn.commit()
         # Clear entry fields and refresh parts list
        self.part_name_entry.delete(0, tk.END)
        self.part_description_entry.delete(0, tk.END)
        self.part_count_entry.delete(0, tk.END)
        self.refresh_parts_list()
    def refresh_parts_list(self):
        self.parts_listbox.delete(0, tk.END)
        self.cursor.execute('SELECT * FROM parts')
        parts = self.cursor.fetchall()
        for part in parts:
            self.parts_listbox.insert(tk.END, f"{part[0]} - {part[1]} ({part[3]})")
if __name__ == "__main__":
    part_manager = PartManager()