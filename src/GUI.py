from tkinter import *

class SearchBar:
    root: Tk
    label: Label
    max_display: int
    data: list[str]
    entry: Entry
    button: Button
    listbox: Listbox or None

    def __init__(self, root, data):
        self.root = root

        self.label = Label(self.root, text="Search for stock", pady=20)
        self.label.pack()

        self.max_display = 5
        self.data = data

        self.entry = Entry(self.root, state='normal', width=40)
        self.entry.pack()

        self.button = Button(self.root, text='Search')
        self.button.pack()
        self.root.update()
        self.button.place(in_=self.entry, bordermode="outside", anchor="nw", relx=1.0, x=5)

        self.listbox = None
        self.root.update()

        self.entry.bind("<FocusIn>", self.focus_in)
        self.entry.bind("<KeyRelease>", self.key_release)
        self.button.bind("<Button-1>", self.get_graph)
        self.root.bind("<Button-1>", self.click_outside)
        self.root.bind("<Return>", self.get_graph)

    def focus_in(self, event):
        if self.listbox is None:
            self.create_listbox()

    def key_release(self, event):
        if self.listbox:
            self.update_listbox()

    def click_outside(self, event):
        if event.widget == self.entry:
            return
        else:
            self.delete_listbox()

    def create_listbox(self):
        x = self.entry.winfo_x()
        y = self.entry.winfo_y() + self.entry.winfo_height()
        w = self.entry.winfo_width()
        self.listbox = Listbox(self.root, width=w, height=self.max_display, font=("Helvetica", 12))
        self.listbox.place(x=x, y=y, width=w)
        self.update_listbox()
        self.listbox.bind("<<ListboxSelect>>", self.check_selection)

    def check_selection(self, event):
        if self.listbox:
            self.entry.delete(0, END)
            self.entry.insert(0, self.listbox.get(ANCHOR))

    def update_listbox(self):
        pattern = self.entry.get().lower()
        matches = [item for item in self.data if pattern in item.lower()]
        self.listbox.delete(0, END)
        self.listbox.insert(END, *matches[:self.max_display])

    def delete_listbox(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

    def get_graph(self, event):
        selected_item = self.entry.get()
        if selected_item != '':
            # get the graph
            print(selected_item)
        else:
            print("did not input a valid stock name")

if __name__ == "__main__":
    root = Tk()
    root.title("Stock Sentiment Analyzer")
    root.geometry('500x300')
    root.update()

    data = ["amour", "gloire", "pouvoir de l'instant présent", "beauté", "guerre", "action"]

    search_bar = SearchBar(root, data)
    root.update()

    root.mainloop()
