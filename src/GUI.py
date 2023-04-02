from tkinter import *


class SearchBar:
    root: Tk
    label: Label
    max_display: int
    data: list[str]
    entry: Entry
    listbox: Listbox or None

    def __init__(self, root, name, data):
        self.root = root

        self.label = Label(self.root, text=name, pady=20)
        self.label.pack()

        self.max_display = 5
        self.data = data

        self.entry = Entry(self.root, state='normal', width=40)
        self.entry.pack()

        self.listbox = None
        self.root.update()

        self.entry.bind("<FocusIn>", self.focus_in)
        self.entry.bind("<KeyRelease>", self.key_release)
        self.root.bind("<Button-1>", self.click_outside)

    def focus_in(self, event):
        if self.listbox:
            self.listbox.place_forget()
        self.create_listbox()

    def key_release(self, event):
        if self.listbox:
            self.update_listbox()

    def click_outside(self, event):
        if event.widget == self.entry:
            return
        else:
            self.delete_listbox()
            self.root.focus()

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

    def get_entry_item(self, event):
        selected_item = self.entry.get()
        return selected_item


class Main:
    root: Tk
    preset_data: list[str]
    ticker_data: list[str]
    search_bar: SearchBar
    preset_button: Button
    scrape_button: Button
    generate_scrape: Scrape or None
    generate_preset: Preset or None


    def __init__(self, preset_data, ticker_data):
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title("Main Screen")
        self.root.update()

        self.search_bar = SearchBar(self.root, "Preset Selection", data)

        self.preset_data = preset_data
        self.ticker_data = ticker_data

        self.preset_button = Button(self.root, text='Load Preset')
        self.scrape_button = Button(self.root, text='Scrape Live')
        self.load_button.pack()
        self.scrape_button.pack()
        self.root.update()
        self.preset_button.place(in_=self.search_bar.entry, bordermode="inside", anchor="nw", relx=0.35, rely=1.0, y=110)
        self.scrape_button.place(in_=self.load_button, bordermode="outside", anchor="nw", relx=0, rely=1.0, y=5)

        self.root.update()

        self.preset_button.bind("<Button-1>", self.load_preset)
        self.scrape_button.bind("<Button-1>", self.scrape_live)

        self.root.mainloop()

    def load_preset(self, event):
        selected_item = self.search_bar.entry.get()
        if selected_item != '':

            print("load preset")
        else:
            print("did not input a valid stock name")

    def scrape_live(self, event):
        selected_item = self.search_bar.entry.get()
        if selected_item != '':
            self.generate_scrape = Scrape(self.ticker_data)
            print("scrape live")
        else:
            print("did not input a valid stock name")


class Scrape:
    root: Tk
    data: list[str]
    search_bar: SearchBar
    number_of_articles: Entry
    saved_name: Entry
    start_button: Button

    def __init__(self, data):
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title("Scrape Live")
        self.root.update()

        self.search_bar = SearchBar(self.root, "Tickers Selection", data)

        self.data = data

        label1 = Label(self.root, text="Number of articles per ticker")
        label1.pack()
        self.number_of_articles = Entry(self.root, state='normal', width=40)
        self.number_of_articles.pack()

        label2 = Label(self.root, text="Save name")
        label2.pack()
        self.saved_name = Entry(self.root, state='normal', width=40)
        self.saved_name.pack()

        self.root.update()

        self.start_button.bind("<Button-1>", self.generate_scraping_data)

        self.root.mainloop()

    def generate_scraping_data(self):
        try:
            num_articles = int(self.number_of_articles.get())
        except ValueError:
            print("did not enter valid number of articles")
            return None

        name = self.saved_name.get()
        ticker = self.search_bar.entry.get()

        if name != '':
            # generate scraping progress
            print("generate scraping progress with", name, ticker, num_articles)
        else:
            print("did not enter valid name or ticker")
            return None







if __name__ == "__main__":


    preset = ["amour", "gloire", "pouvoir de l'instant présent", "beauté", "guerre", "action"]
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'WMT', 'V']

    main_screen = Main(preset)
