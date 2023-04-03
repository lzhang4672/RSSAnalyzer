from tkinter import *


class SearchBar():
    """
    A class representing a search bar, and the functions will mimic a search bar behaviour
    (ie. when the search bar has been clicked on, a drop-down list of suggestions will pop up.
    when information has been properly entered into the search bar, the drop-down list of suggestions
    should be deleted.)

    Instance Attributes:
    - root is a Tk window that is already be created before SearchBar is initialized.
    - label is a Label. This is the name of the SearchBar and will appear as a header on top of the search bar.
    - data is a list of strings that SearchBar uses to give suggested results
    - entry is a Entry. This is the interactive search bar where the user can enter information into.
    - listbox is a Listbox of possible suggestions
    """
    root: Tk
    label: Label
    data: list[str]
    entry: Entry
    listbox: Listbox or None

    def __init__(self, root, name, data):
        self.root = root

        self.label = Label(self.root, text=name, pady=20)
        self.label.pack()

        self.data = data

        self.entry = Entry(self.root, state='normal', width=40)
        self.entry.pack()

        self.listbox = None
        self.root.update()

        self.entry.bind("<FocusIn>", self.focus_in)
        self.entry.bind("<KeyRelease>", self.key_release)
        self.entry.bind("<FocusOut>", self.click_outside)

    def focus_in(self, event):
        """
        Checks if a listbox is already displayed. If a listbox is already displayed, it will be deleted.
        and a new one will be created. Calls create_listbox to create the listbox automatically called when
        the user clicks into entry.
        """
        if self.listbox:
            self.listbox.place_forget()
        self.create_listbox()

    def key_release(self, event):
        """
        If the user types anything into entry, the listbox will update its suggested results to
        a new list of possible results automatically called when the user types anything into entry.
        """
        if self.listbox:
            self.update_listbox()

    def click_outside(self, event):
        """
        Delete the listbox and reset the focus state of root automatically called when the user clicks
        another widget on root.
        """
        self.delete_listbox()
        self.root.focus()

    def create_listbox(self):
        """
        Create a listbox that contains possible suggestions directly underneath the entry.
        """
        x = self.entry.winfo_x()
        y = self.entry.winfo_y() + self.entry.winfo_height()
        w = self.entry.winfo_width()
        self.listbox = Listbox(self.root, width=w, height=5, font=("Helvetica", 12))
        self.listbox.place(x=x, y=y, width=w)
        self.update_listbox()
        self.listbox.bind("<<ListboxSelect>>", self.check_selection)

    def check_selection(self, event):
        """
        If the user selects any item in the listbox, the entry will be filled in automatically.
        """
        if self.listbox:
            self.entry.delete(0, END)
            self.entry.insert(0, self.listbox.get(ANCHOR))

    def update_listbox(self):
        """
        The listbox will filter out unwanted results based on what the user has typed into the entry.
        (ie. if the user types the letter "A" the suggestions without "A" will be filtered out)
        """
        pattern = self.entry.get().lower()
        matches = [item for item in self.data if pattern in item.lower()]
        self.listbox.delete(0, END)
        self.listbox.insert(END, *matches[:self.max_display])

    def delete_listbox(self):
        """
        If there is a existing listbox, it will be deleted.
        """
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None


class DisplayList:
    """
    A class representing a list of items to display, with a corresponding scroll bar on the left of the
    listbox.

    Instance Attributes:
    - root is a Tk window that is already be created before DisplayList is initialized.
    - frame is a Frame that will be created on root, and acts as a platform for scrollbar and listbox.
    This is so the user can create multiple DispayLists in one root.
    - scrollbar is a Scrollbar that interacts with listbox
    - listbox is a Listbox of returned results
    """
    root: Tk
    frame: Frame
    scrollbar: Scrollbar
    listbox: Listbox

    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)

        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = Listbox(self.frame, width=35, height=5, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.frame.pack()
        self.listbox.pack()


class ScrapeLive:
    """
    A class representing the Scraping Live pop-up Tk window.

    Instance Attributes:
    - root is a TK window that will be created in the initializer
    - search_bar is a SearchBar provided with a list of ticker names
    - number_of_articles is a Entry that saves the user input of number of articles to process
    - saved_name is a Entry that saves the user input of the name of the saved scraping process
    - start_button is a Button to start the scraping
    """
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
        """
        Checks if user entered all valid entries into num_articles, saved_name, and tickers,
        and respectfully runs the live scraping results.
        """
        try:
            num_articles = int(self.number_of_articles.get())
        except ValueError:
            print("did not enter valid number of articles")
            return None

        name = self.saved_name.get()
        ticker = self.search_bar.entry.get()

        if name != '':
            generate_progress = ScrapeProgress()
            # this should be redirected to the live pygame display. able to use name, ticker, and num articles as variables
        else:
            print("did not enter valid name or ticker")
            return None


class LoadPreset:
    """
    A class representing a display of the loaded results from scraping.

    Instance Attributes:
    - root is a Tk window that will be created in the initalizer
    - search_bar is a SearchBar provided with company names
    - load_button is a Button to display the loaded results
    - display_company_details is a DisplayList of company details such as the
    ticker symbol, industry, sentiment score...
    - display_articles_analyzed is a DisplayList of the articles processed during scraping
    - display_analyzed_data is a DisplayList of data processed during scraping
    """
    root: Tk
    companies: list[str]
    search_bar: SearchBar
    load_button: Button
    display_company_details: DisplayList
    display_articles_analyzed: DisplayList
    display_analyzed_data: DisplayList

    def __init__(self, data):
        self.root = Tk()
        self.root.geometry('600x600')

        self.companies = data  # should be a dictionary

        self.search_bar = SearchBar(self.root, "Company", self.companies)

        self.load_button = Button(self.root, text="Load", command=self.generate_listboxes)
        self.load_button.place(in_=self.search_bar.entry, bordermode="outside",
                               anchor="ne", relx=1.0, rely=0, x=40)

        label1 = Label(self.root, text="Company Details", pady=20)
        label1.pack()

        self.display_company_details = DisplayList(self.root)

        label2 = Label(self.root, text="Articles Analyzed", pady=20)
        label2.pack()
        self.display_articles_analyzed = DisplayList(self.root)

        label3 = Label(self.root, text="Analyzed Data", pady=20)
        label3.pack()
        self.display_analyzed_data = DisplayList(self.root)

    def generate_listboxes(self):
        """
        Display listboxes after load_button has been clicked. If the company entered is not valid,
        no results should be displayed.
        """
        self.display_company_details.listbox.insert(END, *self.companies)
        # self.companies should be replaced with the results of company details from stock analyzer.py or sentiment analyzer.py in list[str]
        self.display_articles_analyzed.listbox.insert(END, *self.companies)
        # self.companies should be replaced with results of analyzed articles from stock analyzer.py or sentiment analyzer in list[str]
        self.display_analyzed_data.listbox.insert(END, *self.companies)
        # self.companies should be replaced with analyzed data from graph.py or stockgraphanalyzer.py in list[str]


class Main:
    """
    A class representing the Main Menu pop-up window.

    Instance Attributes:
    - root is a Tk window that is created in the initializer
    - preset_data is a list of preset data
    - ticker_data is a list of tickers avaliable
    - search_bar is a SearchBar provided with preset data
    - preset_button is a Button that opens LoadedResults window
    - scrape_button is a Button that opens ScrapeLlive window
    """
    root: Tk
    preset_data: list[str]
    ticker_data: list[str]
    search_bar: SearchBar
    preset_button: Button
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
        """
        If the entry is valid, then opens up the LoadPreset window.
        """
        selected_item = self.search_bar.entry.get()
        if selected_item != '':
            LoadPreset(self.ticker_data)
        else:
            print("did not input a valid stock name")

    def scrape_live(self):
        """
        If entry is valid, then opens up the ScrapeLive window.
        """
        selected_item = self.search_bar.entry.get()
        if selected_item != '':
            ScrapeLive(self.ticker_data)
        else:
            print("did not input a valid stock name")


if __name__ == "__main__":
    preset = ["amour", "gloire", "pouvoir de l'instant présent", "beauté", "guerre", "action"]
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'WMT', 'V']

    main_screen = Main(preset, tickers)
