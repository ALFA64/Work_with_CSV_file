import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Fișiere CSV
file_path_students = "students.csv"
file_path_teachers = "Teachers.csv"

df = None

def read_csv_file_students():
    global df 
    try:
        df = pd.read_csv(file_path_students)
        combo_col['values'] = list(df.columns)
        setare_header(df.columns)
        view_table(df)
        combo_col.set("Selectează o coloană")
    except Exception as e:
        messagebox.showerror("Error", f"Eroare la încărcarea datelor: {e}")
        
def read_csv_file_teachers():
    global df
    try:
        df = pd.read_csv(file_path_teachers)  # Se schimbă în teachers.csv
        combo_col['values'] = list(df.columns)
        setare_header(df.columns)
        view_table(df)
        combo_col.set("Selectează o coloană")
    except Exception as e:
        messagebox.showerror("Error", f"Eroare la încărcarea datelor: {e}")


def setare_header(coloane):
    tree.delete(*tree.get_children())
    tree["columns"] = list(coloane)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor='w', width=120)

def view_table(dataframe):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def filtrare():
    column = combo_col.get()
    valoare = entry_search.get().lower().strip()
    if column and valoare:
        df_filtrat = df[df[column].astype(str).str.lower().str.contains(valoare, na=False)]
    else:
        df_filtrat = df
    view_table(df_filtrat)

def modify_value(event):
    item = tree.selection()[0]
    col = tree.identify_column(event.x).replace("#", "")
    row_idx = tree.index(item)
    
    old_value = df.iloc[row_idx, int(col) - 1]
    new_value = simpledialog.askstring(
        "Editează", 
        f"Modifică valoarea din coloana {tree['columns'][int(col)-1]}",
        initialvalue=old_value
    )
    
    if new_value is not None:
        df.iloc[row_idx, int(col)-1] = new_value
        tree.item(item, values=list(df.iloc[row_idx]))
    else:
        messagebox.showinfo("Info", "Modificarea a fost anulată")

def save_csv():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Salvează fișierul CSV"
    )
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Succes", "Fișierul CSV a fost salvat!")

def show_first_rows():
    if df is not None:
        view_table(df.head(7))
    else:
        messagebox.showwarning("Warning", "Nu există date încărcate.")

def filter_adult_students():
    if 'Varsta' in df.columns:
        filter_res = df[df['Varsta'] >= 18]
        view_table(filter_res)
    else:
        messagebox.showwarning("Warning", "Coloana 'Varsta' nu este prezentă în date.")

def plot_histogram():
    if 'Specialitate' in df.columns:
        df['Specialitate'].value_counts().plot(kind='bar')
        plt.title('Distribuția Specialităților')
        plt.xlabel('Specialitate')
        plt.ylabel('Număr de elevi')
        plt.show()
    else:
        messagebox.showwarning("Warning", "Coloana 'Specialitate' nu este prezentă în date.")

def group_by_speciality():
    if 'Specialitate' in df.columns:
        grouped = df.groupby('Specialitate').size()
        messagebox.showinfo("Grupare după Specialitate", grouped.to_string())
    else:
        messagebox.showwarning("Warning", "Coloana 'Specialitate' nu este prezentă în date.")

def combine_tables():
    global df
    try:
        # Citirea fișierelor CSV pentru studenți și profesori
        df_students = pd.read_csv(file_path_students)
        df_teachers = pd.read_csv(file_path_teachers)
        
        # Combinarea tabelelor pe baza coloanei 'specialitate'
        df = pd.merge(df_students, df_teachers, on='Specialitate', how='inner')
        
        # Actualizarea combo box cu noile coloane combinate
        combo_col['values'] = list(df.columns)
        
        # Setarea header-ului pentru tabel
        setare_header(df.columns)
        
        # Afișarea tabelului combinat
        view_table(df)
        
        # Resetarea selecției din combo box
        combo_col.set("Selectează o coloană")
    except Exception as e:
        messagebox.showerror("Error", f"Eroare la încărcarea datelor: {e}")




def drop_missing_rows():
    global df
    df.dropna(inplace=True)
    view_table(df)


def average_age_by_speciality():
    try:
        # Citește datele din fișierul CSV
        df = pd.read_csv(file_path_students)
        
        # Verifică dacă coloanele necesare există
        if 'Specialitate' in df.columns and 'Varsta' in df.columns:
            # Calcularea mediei pe specialitate
            result = df.groupby('Specialitate')['Varsta'].mean().reset_index()
            
            # Construirea mesajului pentru afișare
            message = "Vârsta medie pe specialitate:\n"
            for index, row in result.iterrows():
                message += f"- {row['Specialitate']}: {row['Varsta']:.2f} ani\n"
            
            # Afișarea rezultatului în MessageBox
            messagebox.showinfo("Vârsta Medie", message)
        else:
            messagebox.showerror("Eroare", "Coloanele 'Specialitate' și 'Varsta' nu sunt prezente în fișier.")
    except FileNotFoundError:
        messagebox.showerror("Eroare", f"Fișierul {file_path_students} nu a fost găsit.")
    except Exception as e:
        messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")



def add_salary_column():
    try:
        if 'norma_didactica' in df.columns and 'coeficient_salarial' in df.columns:
            df['salariu'] = df['norma_didactica'] * df['coeficient_salarial']

            # Verifică actualizarea combo-box
            if 'salariu' not in combo_col['values']:
                combo_col['values'] = list(df.columns)

            setare_header(df.columns)
            view_table(df)
        else:
            messagebox.showwarning("Warning", "Coloanele 'norma_didactica' și 'coeficient_salarial' nu sunt prezente!")
    except Exception as e:
        messagebox.showerror("Error", f"A apărut o eroare: {str(e)}")




def replace_missing_with_name():
    global df
    column = simpledialog.askstring("Coloana", "Introduceți numele coloanei pentru înlocuire:")
    if column in df.columns:
        df[column].fillna("Numele_Familiei", inplace=True)
        view_table(df)



def generate_wordcloud():
    if 'Specialitate' in df.columns:
        text = " ".join(speciality for speciality in df['Specialitate'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    else:
        messagebox.showwarning("Warning", "Coloana 'Specialitate' nu este prezentă în date.")

root = tk.Tk()
root.title("<<< Studiu Individual 3 >>>")
root.geometry("800x600")

frame_views = tk.Frame(root)
frame_views.pack(pady=10)

button_view_all_students = tk.Button(frame_views, text="View All Students", command=read_csv_file_students)
button_view_all_students.grid(row=0,column=0,padx=10,pady=10)


button_view_all_teacher = tk.Button(frame_views,text="View All Teachers", command=read_csv_file_teachers)
button_view_all_teacher.grid(row=0,column=1,padx=10,pady=10)

frame_filtru = tk.Frame(root)
frame_filtru.pack(pady=10)

combo_col = ttk.Combobox(frame_filtru, state="readonly")
combo_col.grid(row=0, column=0, padx=10, pady=5)

entry_search = ttk.Entry(frame_filtru)
entry_search.grid(row=0, column=1, padx=10, pady=5)

button_seach = ttk.Button(frame_filtru, text="Caută", command=filtrare)
button_seach.grid(row=0, column=2, padx=10, pady=5)

tree = ttk.Treeview(root, show="headings")
tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.bind("<Double-1>", modify_value)

frame_button = tk.Frame(root)
frame_button.pack(padx=10)

button_save = tk.Button(frame_button, text="SAVE", command=save_csv)
button_save.grid(row=0, column=0, padx=10)

button_first_rows = tk.Button(frame_button, text="Primele 7 rânduri", command=show_first_rows)
button_first_rows.grid(row=0, column=1, padx=10)

button_filter_adults = tk.Button(frame_button, text="Filtru Majorat", command=filter_adult_students)
button_filter_adults.grid(row=0, column=2, padx=10)

button_histogram = tk.Button(frame_button, text="Histogramă", command=plot_histogram)
button_histogram.grid(row=0, column=3, padx=10)

button_group_by = tk.Button(frame_button, text="Grupare Specialități", command=group_by_speciality)
button_group_by.grid(row=0, column=4, padx=10)

button_combine = tk.Button(frame_button, text="Combine Tables", command=combine_tables)
button_combine.grid(row=0, column=5, padx=10)

button_drop_missing = tk.Button(frame_button, text="Elimină valori lipsă", command=drop_missing_rows)
button_drop_missing.grid(row=0, column=6, padx=10)

button_avg_age = tk.Button(frame_button, text="Vârsta Medie", command=average_age_by_speciality)
button_avg_age.grid(row=0, column=7, padx=10)

button_add_salary = tk.Button(frame_button, text="Adaugă Salariu", command=add_salary_column)
button_add_salary.grid(row=0, column=8, padx=10)

button_replace_missing = tk.Button(frame_button, text="Înlocuire Nume", command=replace_missing_with_name)
button_replace_missing.grid(row=0, column=9, padx=10)

button_wordcloud = tk.Button(frame_button, text="WordCloud", command=generate_wordcloud)
button_wordcloud.grid(row=0, column=10, padx=10)

root.mainloop()
