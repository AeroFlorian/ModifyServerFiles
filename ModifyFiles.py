import re
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import uu
import os

files = []
dest = ""

def modify_file(path, dir_path):
    print(f"Path is {path}")
    print(f"Destination is {dir_path}")
    try:
        lines_E = []
        lines_K = []
        lines_D = []
        with open(path) as file:
            for line in file:
                if re.match(r'^E\d{10}.*$', line):
                    lines_E.append(line)
                elif re.match(r'^KTN\d{4}[^#]*$', line):
                    lines_K.append(line)
                elif len(line):
                    lines_D.append(line)
        output = []
        if len(lines_E) != len(lines_K) or len(lines_E) == 0:
            os.system(f"copy {path} {dir_path}")
            return "Deja Fait"
        for line in lines_D:
            output.append(line)

        for line_E, line_K in zip(lines_E, lines_K):
            product_E = line_E.split(' ')[0][1:]
            product_K = [l for l in line_K.split(' ') if len(l)][1]
            line_K = line_K.replace(product_K + ' ' * (len(product_E) + 1), f"{product_K}#{product_E}")

            output.append(line_K)
            output.append(line_E)
        print(f"Output: {output}")
        d = dir_path + "\\" + path.split("\\")[-1]
        print(f'Dest: {d}')
        with open(dir_path + "\\" + path.split("\\")[-1], 'w') as file:
            file.writelines(output)
        return "Termine"
    except:
        return "Erreur"

def convert(event):
    global dest
    if not dest:
        tk.messagebox.showerror("Erreur", f"Le dossier de destination \nn'est pas présent")
        return
    for child in result_box.get_children():
        if result_box.item(child)['values'][1] != "Termine":
            res = modify_file(result_box.item(child)['values'][0], result_box.item(child)['values'][2])
            result_box.insert("", 'end',
                              values=(result_box.item(child)['values'][0], res, result_box.item(child)['values'][2]),
                              tags=res.replace(' ', ''))
            result_box.delete(child)


def load_file(event):
    ff = filedialog.askopenfiles()
    result_box.tag_configure("Pret", background='lightyellow')
    result_box.tag_configure("Termine", background='lightgreen')
    result_box.tag_configure("DejaFait", background='lightgreen')
    result_box.tag_configure("Erreur", background='red')
    for f in ff:
        if f.name not in files:
            files.append(f.name.replace('/', '\\'))
            result_box.insert('', 'end', text='', values=(
                f.name.replace('/', '\\'), "Pret", dest), tags="Pret")
        else:
            tk.messagebox.showerror("Erreur", f"Le fichier\n{f.name}\nest déjà présent")

def load_dir(event):
    global dest
    dest = filedialog.askdirectory().replace('/', '\\')

    for item in result_box.get_children():
        result_box.insert("", 'end', values=(result_box.item(item)['values'][0], result_box.item(item)['values'][1], dest), tags=result_box.item(item)['values'][1])
        result_box.delete(item)



if __name__ == "__main__":
    uu.decode('fs_ico_encoded', 'fs.ico')
    window = tk.Tk()
    s = ttk.Style()


    # workaround for row coloring
    def fixed_map(option):
        return [elm for elm in s.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
    s.map('Treeview', foreground=fixed_map('foreground'),
          background=fixed_map('background'))
    # end workaround
    window.title('ModifyServerFiles')
    window.wm_iconbitmap('fs.ico')
    window.iconbitmap('fs.ico')
    window.state('zoomed')
    result_box = ttk.Treeview(master=window, height=25)
    result_box["columns"] = ("Chemin", "Etat", "Destination")
    conversion = tk.Button(master=window, text="Conversion")

    ajouter = tk.Button(master=window, text="Ajouter Fichier")
    destination = tk.Button(master=window, text="Dossier de destination")
    ajouter.bind("<Button-1>", load_file)
    destination.bind("<Button-1>", load_dir)
    conversion.bind("<Button-1>", convert)


    result_box.column("#0", width=10, minwidth=10, stretch=tk.NO)
    result_box.column("Chemin", width=600, minwidth=400,
                      stretch=tk.YES, anchor="c")
    result_box.column("Etat", width=100, minwidth=100,
                      stretch=tk.NO, anchor="c")
    result_box.column("Destination", width=600, minwidth=400,
                      stretch=tk.YES, anchor="c")
    result_box.heading('#0', text='', anchor=tk.CENTER)
    result_box.heading('Chemin', text='Chemin', anchor=tk.CENTER)
    result_box.heading('Etat', text='Etat', anchor=tk.CENTER)
    result_box.heading('Destination', text='Destination', anchor=tk.CENTER)
    result_box.place(y=50, height=window.winfo_height()*3/4, width=window.winfo_width())

    result_box.pack()
    destination.pack()
    ajouter.pack()
    conversion.pack()
    sb = tk.Scrollbar(window, orient=tk.VERTICAL)
    sb.pack(side=tk.RIGHT, fill=tk.Y)

    result_box.config(yscrollcommand=sb.set)
    sb.config(command=result_box.yview)
    window.mainloop()


