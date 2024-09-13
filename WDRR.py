import tkinter as tk
from tkinter import messagebox

class TableFrame(tk.Frame):
    def __init__(self, master=None, table_data=None):
        super().__init__(master)
        self.table_data = table_data
        self.dca_value = 0
        self.dcb_value = 0
        self.dcc_value = 0
        self.create_widgets()
        self.locked = False

    def create_widgets(self):
        interface_label = tk.Label(self, text="L'interface de l'entrer")
        interface_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.table_entries = []

        for i, row_data in enumerate(self.table_data):
            cell_data_1 = row_data[0]
            cell_label_1 = tk.Label(self, text=cell_data_1, borderwidth=1, relief="solid", fg="black")
            cell_label_1.grid(row=i + 1, column=0, sticky="nsew")

            cell_entry = tk.Entry(self, textvariable=tk.StringVar(value=row_data[1]), borderwidth=1, relief="solid",
                                  fg="black", disabledforeground="black")
            cell_entry.grid(row=i + 1, column=1, sticky="nsew")
            self.table_entries.append(cell_entry)

            self.grid_rowconfigure(i + 1, weight=1)

        self.new_table_canvas_a = tk.Canvas(self, borderwidth=1, relief="solid", bg="white", height=20)
        self.new_table_canvas_a.grid(row=len(self.table_data) + 2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.new_table_canvas_a.grid_remove()

        self.new_table_canvas_b = tk.Canvas(self, borderwidth=1, relief="solid", bg="white", height=20)
        self.new_table_canvas_b.grid(row=len(self.table_data) + 4, column=0, columnspan=2, sticky="nsew", pady=10)
        self.new_table_canvas_b.grid_remove()

        self.new_table_canvas_c = tk.Canvas(self, borderwidth=1, relief="solid", bg="white", height=20)
        self.new_table_canvas_c.grid(row=len(self.table_data) + 6, column=0, columnspan=2, sticky="nsew", pady=10)
        self.new_table_canvas_c.grid_remove()

        self.new_table_canvas_output = tk.Canvas(self, borderwidth=1, relief="solid", bg="white", height=20)
        self.new_table_canvas_output.grid(row=len(self.table_data) + 8, column=0, columnspan= 21 , sticky="nsew", pady=10)
        self.new_table_canvas_output.grid_remove()

        label_a = tk.Label(self, text="file d'attent A:")
        label_a.grid(row=len(self.table_data) + 1, column=0, columnspan=2, sticky="nsew")

        label_b = tk.Label(self, text="Tfile d'attent B:")
        label_b.grid(row=len(self.table_data) + 3, column=0, columnspan=2, sticky="nsew")

        label_c = tk.Label(self, text="file d'attent C:")
        label_c.grid(row=len(self.table_data) + 5, column=0, columnspan=2, sticky="nsew")

        label_output = tk.Label(self, text="Interface de sortie:")
        label_output.grid(row=len(self.table_data) + 7, column=0, columnspan=2, sticky="nsew")

        self.add_column_button = tk.Button(self, text="+", command=self.add_column, state=tk.NORMAL)
        self.add_column_button.grid(row=len(self.table_data) + 9, column=0, columnspan=2, sticky="nsew")

        self.drr_button = tk.Button(self, text="DRR", command=self.show_dc_frame)
        self.drr_button.grid(row=len(self.table_data) + 10, column=0, columnspan=2, sticky="nsew")

    def show_dc_frame(self):
        if not self.locked:
            dc_frame = DcFrame(self.master, self.set_dc_values)

    def set_dc_values(self, dca, dcb, dcc):
        self.dca_value = dca
        self.dcb_value = dcb
        self.dcc_value = dcc
        self.calculate_stats()

    def add_column(self):
        if not self.locked:
            new_column_index = len(self.table_data[0])
            new_column_index += 1
            self.grid_columnconfigure(new_column_index, weight=1)

            for i, row_data in enumerate(self.table_data):
                while len(row_data) <= new_column_index:
                    row_data.append('')

                cell_data = row_data[new_column_index]
                cell_entry = tk.Entry(self, textvariable=tk.StringVar(value=cell_data), borderwidth=1, relief="solid",
                                      fg="black", disabledforeground="black")
                cell_entry.grid(row=i + 1, column=new_column_index, sticky="nsew")
                self.table_entries.append(cell_entry)

    def calculate_stats(self):
        if not self.locked:
            column_values_arrive = [entry.get() for entry in self.table_entries[::len(self.table_data)]]

            if '' in column_values_arrive:
                messagebox.showwarning("Missing Data", "Please fill in all cells in the 'Les temps d\'arrive' column.")
                return

            for i in range(1, 5):
                for entry in self.table_entries[i::len(self.table_data)]:
                    if entry.get() == '':
                        entry.insert(0, '/')

            column_values_arrive = [entry.get() for entry in self.table_entries[::len(self.table_data)]]

            values_a = [entry.get() for entry in self.table_entries[1::len(self.table_data)] if entry.get() != '/']
            values_b = [entry.get() for entry in self.table_entries[2::len(self.table_data)] if entry.get() != '/']
            values_c = [entry.get() for entry in self.table_entries[3::len(self.table_data)] if entry.get() != '/']

            arr_a = [column_values_arrive[i] for i, entry in enumerate(self.table_entries[1::len(self.table_data)]) if entry.get() != '/']
            arr_b = [column_values_arrive[i] for i, entry in enumerate(self.table_entries[2::len(self.table_data)]) if entry.get() != '/']
            arr_c = [column_values_arrive[i] for i, entry in enumerate(self.table_entries[3::len(self.table_data)]) if entry.get() != '/']

            sum_of_abc = len(values_a) + len(values_b) + len(values_c)

            tmp = float(''.join(column_values_arrive[0]))
            dca, dcb, dcc = 0, 0, 0

            i, j, k, l = 0, 0, 0, 0

            F = [0] * sum_of_abc
            while l < int(sum_of_abc):
                dca += self.dca_value
                dcb += self.dcb_value
                dcc += self.dcc_value
                print(f'dca{dca}')
                print(f'dcb{dcb}')
                print(f'dcc{dcc}')
                while dca != 0 and i < len(values_a) and int(values_a[i]) <= dca:
                    if float(arr_a[i]) > tmp:
                        dca = 0
                        break
                    else:
                        tmp += int(values_a[i]) / 1000
                        F[l] = 'A(' + values_a[i] + ')'
                        dca -= int(values_a[i])
                        l += 1
                        i += 1

                while dcb != 0 and j < len(values_b) and int(values_b[j]) <= dcb:
                    if float(arr_b[j]) > tmp:
                        dcb = 0
                        break
                    else:
                        F[l] = 'B(' + values_b[j] + ')'
                        tmp += int(values_b[j]) / 1000
                        dcb -= int(values_b[j])
                        l += 1
                        j += 1

                while dcc != 0 and k < len(values_c) and int(values_c[k]) <= dcc:
                    if float(arr_c[k]) > tmp:
                        dcc = 0
                        break
                    else:
                        F[l] = 'C (' + values_c[k] + ')'
                        tmp += int(values_c[k]) / 1000
                        dcc -= int(values_c[k])
                        l += 1
                        k += 1
                print(f'dca{dca}')
                print(f'dcb{dcb}')
                print(f'dcc{dcc}')

            self.locked = True
            self.add_column_button.config(state=tk.DISABLED)

            for entry in self.table_entries:
                entry.config(state=tk.DISABLED)

            self.display_new_table(self.new_table_canvas_a, list(reversed(values_a)), "Files d'attente A:")
            self.display_new_table(self.new_table_canvas_b, list(reversed(values_b)), "Files d'attente B:")
            self.display_new_table(self.new_table_canvas_c, list(reversed(values_c)), "Files d'attente C:")
            self.display_new_table(self.new_table_canvas_output, list(reversed(F)), "Interface de sortie:")

    def display_new_table(self, canvas, values, table_name):
        canvas.delete("all")
        canvas.config(height=20)

        if isinstance(values, int):
           values = [values]

        for i, value in enumerate(values):
            x1 = i * 48
            x2 = (i + 1) * 48
            center_x = (x1 + x2) // 2
            center_y = canvas.winfo_reqheight() // 2

            canvas.create_line(x1, 0, x1, 20, fill="black")
            canvas.create_text(center_x, center_y, text=f"{value}", anchor=tk.CENTER, font=("Helvetica", 10))

        canvas.grid()
        canvas.update()

        label = tk.Label(self, text=f"{table_name}: {', '.join(map(str, values))}")
        label.grid(row=len(self.table_data) + 1, column=0, columnspan=2, sticky="nsew")
        label.grid_remove()

class DcFrame(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.create_widgets()

    def create_widgets(self):
        dc_label_a = tk.Label(self, text="Set DCA value:")
        dc_label_a.grid(row=0, column=0, padx=10, pady=10)
        self.dc_entry_a = tk.Entry(self)
        self.dc_entry_a.grid(row=0, column=1, padx=10, pady=10)

        dc_label_b = tk.Label(self, text="Set DCB value:")
        dc_label_b.grid(row=1, column=0, padx=10, pady=10)
        self.dc_entry_b = tk.Entry(self)
        self.dc_entry_b.grid(row=1, column=1, padx=10, pady=10)

        dc_label_c = tk.Label(self, text="Set DCC value:")
        dc_label_c.grid(row=2, column=0, padx=10, pady=10)
        self.dc_entry_c = tk.Entry(self)
        self.dc_entry_c.grid(row=2, column=1, padx=10, pady=10)

        apply_button = tk.Button(self, text="Apply", command=self.apply_dc)
        apply_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.pack()

    def apply_dc(self):
        dca_value = self.dc_entry_a.get()
        dcb_value = self.dc_entry_b.get()
        dcc_value = self.dc_entry_c.get()

        if dca_value.isdigit() and dcb_value.isdigit() and dcc_value.isdigit():
            self.callback(int(dca_value), int(dcb_value), int(dcc_value))
            self.destroy()
        else:
            messagebox.showwarning("Invalid Input", "Values must be positive integers.")

if __name__ == "__main__":
    table_data = [
        ['Les temps d\'arrive', '1'],
        ['A', ''],
        ['B', ''],
        ['C', '']
    ]

    root = tk.Tk()

    root.title("Table Frame Example")

    table_frame = TableFrame(root, table_data=table_data)
    table_frame.pack(expand=True, fill="both")

    root.mainloop()
