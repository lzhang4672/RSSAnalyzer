from tkinter import *


class SearchBar():
    root: Tk or Frame
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
        self.entry.bind("<FocusOut>", self.click_outside)

    def focus_in(self, event):
        if self.listbox:
            self.listbox.place_forget()
        self.create_listbox()

    def key_release(self, event):
        if self.listbox:
            self.update_listbox()

    def click_outside(self, event):
        self.delete_listbox()
        self.root.focus()

    def create_listbox(self):
        x = self.entry.winfo_x()
        y = self.entry.winfo_y() + self.entry.winfo_height()
        w = self.entry.winfo_width()
        self.listbox = Listbox(self.root, width=w, height=self.max_display,
                               font=("Helvetica", 12))
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


class ScrapeLive:
    root: Tk
    tickers: list[str]
    search_bar: SearchBar
    number_of_articles: Entry
    saved_name: Entry
    start_button: Button

    def __init__(self, data):
        self.root = Tk()
        self.root.geometry('500x400')
        self.root.title("Scrape Live")
        self.root.update()

        self.tickers = data

        label1 = Label(self.root, text="Number of articles per ticker", pady=20)
        label1.pack()

        self.number_of_articles = Entry(self.root, state='normal', width=40)
        self.number_of_articles.pack()

        label2 = Label(self.root, text="Save name", pady=20)
        label2.pack()

        self.saved_name = Entry(self.root, state='normal', width=40)
        self.saved_name.pack()

        self.root.update()

        self.search_bar = SearchBar(self.root, "Tickers Selection", tickers)

        self.start_button = Button(self.root, text="Start",
                                   command=self.generate_scraping_data)
        self.start_button.pack(side=BOTTOM)

        self.root.update()

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
            print("generate scraping progress with", name, ticker, num_articles)
            generate_progress = ScrapeProgress()
        else:
            print("did not enter valid name or ticker")
            return None


class LoadPreset:
    root: Tk

    def __init__(self, data):
        self.root = Tk()
        self.root.geometry('500x400')

        self.companies = data # should be a dictionary

        self.search_bar = SearchBar(self.root, "Company", self.companies)

        self.load_button = Button(self.root, text="Load", command=self.generate_listboxes)
        self.load_button.place(in_=self.search_bar.entry, bordermode="outside",
                               anchor="ne", relx=1.0, rely=0, x=40)

        label1 = Label(self.root, text="Company Details", pady=20)
        self.frame1 = Frame(self.root)
        self.scroll_bar1 = Scrollbar(self.frame1, orient=VERTICAL)
        self.listbox1 = Listbox(self.frame1, width=35, height=5, yscrollcommand=self.scroll_bar1.set)
        self.scroll_bar1.config(command=self.listbox1.yview)
        label1.pack()
        self.scroll_bar1.pack(side=RIGHT, fill=Y)
        self.frame1.pack()
        self.listbox1.pack()


        label2 = Label(self.root, text="Articles Analyzed", pady=20)
        self.frame2 = Frame(self.root)
        self.scroll_bar2 = Scrollbar(self.frame2, orient=VERTICAL)
        self.listbox2 = Listbox(self.frame2, width=35, height=5, yscrollcommand=self.scroll_bar2.set)
        label2.pack()
        self.scroll_bar2.pack(side=RIGHT, fill=Y)
        self.frame2.pack()
        self.listbox2.pack()

    def generate_listboxes(self):
        self.listbox1.insert(END, *self.companies)

        self.listbox2.insert(END, *self.companies)


class Main:
    root: Tk
    preset_data: list[str]
    ticker_data: list[str]
    search_bar: SearchBar
    preset_button: Button # these are not necessary
    scrape_button: Button

    def __init__(self, preset_data, ticker_data):
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title("Main Screen")
        self.root.update()

        self.search_bar = SearchBar(self.root, "Preset Selection", preset_data)

        self.preset_data = preset_data
        self.ticker_data = ticker_data

        self.preset_button = Button(self.root, text='Load Preset', command=self.load_preset)
        self.scrape_button = Button(self.root, text='Scrape Live', command=self.scrape_live)

        self.root.update()
        self.preset_button.place(in_=self.search_bar.entry, bordermode="inside",
                                 anchor="nw", relx=0.35, rely=1.0, y=110)
        self.scrape_button.place(in_=self.preset_button, bordermode="outside",
                                 anchor="nw", relx=0, rely=1.0, y=10)

        self.root.update()

        self.root.mainloop()

    def load_preset(self):
        selected_item = self.search_bar.entry.get()
        if selected_item != '':
            LoadPreset(self.ticker_data)
        else:
            print("did not input a valid stock name")

    def scrape_live(self):
        selected_item = self.search_bar.entry.get()
        if selected_item != '':
            ScrapeLive(self.ticker_data)
            print("scrape live")
        else:
            print("did not input a valid stock name")



if __name__ == "__main__":

    preset = ["amour", "gloire", "pouvoir de l'instant présent", "beauté", "guerre", "action"]
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'WMT', 'V']

    main_screen = Main(preset, tickers)
