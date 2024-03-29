from tkinter import *
from python_ta.contracts import check_contracts
import CSV
import GUI
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings, SEARCH_FOCUS
from StockGraphAnalyzer import StockGraphAnalyzer
from GraphVisualizer import GraphVisualizer
from StockInfo import get_tickers
import os

# constants

SCRAPE_CACHE_ROOT = './scrape_cache/'
PRESETS_ROOT = './data/presets/'


# top level functions

def get_file_names_from_path(path: str) -> list[str]:
    """Returns all file names in the specified path. This function removes the hidden files associated in the directory.

    Preconditions:
        - path is a valid path
    """
    ret = []
    for file_name in os.listdir(path):
        if not file_name.startswith('.'):
            # make sure it isn't a hidden file (hidden files start with .)
            ret += [file_name]
    return ret


def get_live_ticker_presets() -> dict[str, list[dict[str, str]]]:
    """Returns a dictionary of the ticker presets with the key being the file name and the value being the parsed
    csv file """
    ret = {}
    files = get_file_names_from_path(PRESETS_ROOT)
    for file_name in files:
        if file_name not in ret:
            ret[file_name] = CSV.read_file(PRESETS_ROOT + file_name)
    return ret


class SearchBar:
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
        self.listbox = Listbox(self.root, width=w, height=self.max_display,
                               font=("Helvetica", 12))
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
        - tickers_presets: a dictionary containing the preset file name as the key and the parsed csv file as the key
    Private Instance Attributes:
        - _root: a TK window that will be created in the initializer
        - _search_bar: a SearchBar provided with a list of ticker names
        - _focus_search_bar: a SearchBar provided with a list of available focus options
        - _number_of_articles: an Entry that saves the user input of number of articles to process
        - _start_button: a Button to start the scraping
        - _saved_name is a Entry that saves the user input of the name of the saved scraping process
    """
    _root: Tk
    tickers_presets: dict[str, list[dict[str, str]]]
    _search_bar: SearchBar
    _focus_search_bar: SearchBar
    _number_of_articles: Entry
    saved_name: Entry
    _start_button: Button

    @check_contracts
    def __init__(self, tickers_presets: dict[str, list[dict[str, str]]]):
        self.root = Tk()
        self.root.geometry('500x400')
        self.root.title("Scrape Live")
        self.root.update()

        self.tickers_presets = tickers_presets

        label1 = Label(self.root, text="Number of articles per ticker", pady=20)
        label1.pack()

        self.number_of_articles = Entry(self.root, state='normal', width=40)
        self.number_of_articles.pack()

        label2 = Label(self.root, text="Save name", pady=20)
        label2.pack()

        self.saved_name = Entry(self.root, state='normal', width=40)
        self.saved_name.pack()

        self.root.update()

        self._search_bar = SearchBar(self.root, "Tickers Selection", list(tickers_presets.keys()))

        self._focus_search_bar = SearchBar(self.root, "Focus Selection", list(SEARCH_FOCUS.keys()))

        self.start_button = Button(self.root, text="Start",
                                   command=self.generate_scraping_data)
        self.start_button.pack(side=BOTTOM)

        self.root.update()

        self.root.mainloop()

    @check_contracts
    def generate_scraping_data(self) -> None:
        try:
            num_articles = int(self.number_of_articles.get())
        except ValueError:
            print("Did not enter valid number of articles")
            return None

        name = self.saved_name.get()
        ticker_preset = self._search_bar.entry.get()
        focus_preset = self._focus_search_bar.entry.get()
        if name != '' and ticker_preset in self.tickers_presets and focus_preset in SEARCH_FOCUS:
            ticker_rows = self.tickers_presets[ticker_preset]
            tickers = []
            # add tickers to the list
            for row in ticker_rows:
                tickers += [row['Ticker']]
            # load settings
            live_settings = StockAnalyzerSettings(id=name + '_cache.csv', articles_per_ticker=num_articles,
                                                     use_cache=False,
                                                     search_focus=focus_preset)
            analyzer = StockAnalyzer(tickers, live_settings)
            stock_graph_analyzer = StockGraphAnalyzer(analyzer)
            # generate the graph
            stock_graph_analyzer.generate_graph()
            # run preprocessed algorithms
            stock_graph_analyzer.run_preprocessed_algorithms()
            graph_visualizer = GraphVisualizer(default_settings.id, stock_graph_analyzer)
            graph_visualizer.show_graph()

        else:
            print("Did not enter valid name or ticker")
            return None

class MainMenu:
    """
    A class representing the Main Menu pop-up window.

    Instance Attributes:
        - cache_preset_data is a list of cached preset data
        - ticker_preset_data is a dictionary with ticker preset file names as the key and the parsed csv files as the
          value
    Private Instance Attributes:
        - _root: a Tk window that is created in the initializer
        - _ticker_preset: a list of preset file names
        - _search_bar is a SearchBar provided with preset data
        - _preset_button is a Button that loads a cached preset file
        - _scrape_button is a Button that starts a live scrape event
    """
    _root: Tk
    cache_preset_data: list[str]
    ticker_preset_data: dict[str, list[dict[str, str]]]
    _ticker_preset: list[str]
    _search_bar: SearchBar
    _preset_button: Button
    _scrape_button: Button

    @check_contracts
    def __init__(self):
        self._root = Tk()
        self._root.geometry('500x300')
        self._root.title("StocksConnectionAnalyzer")
        self._root.update()

        self.cache_preset_data = get_file_names_from_path(SCRAPE_CACHE_ROOT)
        self.ticker_preset_data = get_live_ticker_presets()

        self._search_bar = SearchBar(self._root, "Preset Selection", self.cache_preset_data)

        self._preset_button = Button(self._root, text='Load Preset', command=self.load_preset)
        self._scrape_button = Button(self._root, text='Scrape Live', command=self.scrape_live)

        self._root.update()
        self._preset_button.place(in_=self._search_bar.entry, bordermode="inside",
                                 anchor="nw", relx=0.35, rely=1.0, y=110)
        self._scrape_button.place(in_=self._preset_button, bordermode="outside",
                                 anchor="nw", relx=0, rely=1.0, y=10)

        self._root.update()

        self._root.mainloop()

    def load_preset(self):
        """
        If the entry is valid, then opens up the LoadPreset window.
        """
        selected_item = self._search_bar.entry.get()
        if selected_item in self.cache_preset_data:
            # load settings
            default_settings = StockAnalyzerSettings(id=selected_item, articles_per_ticker=10,
                                                     use_cache=True,
                                                     search_focus='Stock')
            tickers = get_tickers()
            analyzer = StockAnalyzer(tickers, default_settings)
            stock_graph_analyzer = StockGraphAnalyzer(analyzer)
            # generate the graph
            stock_graph_analyzer.generate_graph()
            # run preprocessed algorithms
            stock_graph_analyzer.run_preprocessed_algorithms()
            graph_visualizer = GraphVisualizer(default_settings.id, stock_graph_analyzer)
            graph_visualizer.show_graph()

    def scrape_live(self):
        """
        If entry is valid, then opens up the ScrapeLive window.
        """
        ScrapeLive(self.ticker_preset_data)


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod(verbose=True)

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['tkinter', 'CSV', 'GUI', 'StockAnalyzer', 'StockGraphAnalyzer', 'StockInfo', 'os'],
        'allowed-io': ['StockAnalyzer._save_cache',
                       'StockAnalyzer._analyze_stock',
                       'StockAnalyzer._build_data',
                       'StockAnalyzer.__init__'],
        'max-nested-blocks': 10
    })
