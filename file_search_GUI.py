import tkinter as tk
import os

class Searcher:
    def __init__(self, root):
        self.master = root
        self.master.title('File searching application')
        self.mainframe = tk.Frame(self.master, padx=40, pady=20)
        self.mainframe.grid(column=0, row=0, sticky='nsew')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # create widgets
        self.extension_label = tk.Label(self.mainframe, text='Enter extension: ')
        self.directory_label = tk.Label(self.mainframe, text='Enter directory: ')
        self.results_label = tk.Label(self.mainframe, text='Total results: ')
        self.directory = tk.StringVar()
        self.directory_entry = tk.Entry(self.mainframe, textvariable=self.directory)
        self.extension = tk.StringVar()
        self.extension_entry = tk.Entry(self.mainframe, textvariable=self.extension)
        self.search_button = tk.Button(self.mainframe, text='Search', command=self.search_for_results)
        self.clear_button = tk.Button(self.mainframe, text='Clear search results', command=self.clear_search_results)
        self.results_text_box = tk.Text(self.mainframe)
        self.results_total_label = tk.Label(self.mainframe, text='Total results: ')
        self.total_results = tk.StringVar()
        self.results_total_count = tk.Label(self.mainframe, textvariable=self.total_results)
        self.scroll_bar = tk.Scrollbar(self.mainframe, orient='vertical', command=self.results_text_box.yview)

        # place widgets on the screen
        self.extension_label.grid(      column=0, row=0, pady=5, sticky='w')
        self.extension_entry.grid(      column=1, row=0, pady=5, sticky='w')
        self.directory_label.grid(      column=0, row=1, pady=5, sticky='w')
        self.directory_entry.grid(      column=1, row=1, pady=5, sticky='w')
        self.results_total_label.grid(  column=0, row=2, pady=5, sticky='w')
        self.results_total_count.grid(  column=1, row=2, pady=5, sticky='w')
        self.search_button.grid(        column=0, row=3, pady=5, sticky='ew', columnspan=2)
        self.clear_button.grid(         column=0, row=4, pady=5, sticky='ew', columnspan=2)
        self.results_text_box.grid(     column=0, row=5, pady=5, sticky='nsew', columnspan=2, padx=20)
        self.scroll_bar.grid(           column=0, row=5, pady=5, sticky='nsw')

        # adjust some settings
        self.total_results.set('N/A')
        self.extension_entry.focus_set()
        self.directory_entry.configure(width=100)
        self.master.bind('<Return>', self.search_for_results)
        self.results_text_box.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.configure(width=16)
        self.results_text_box.configure(wrap='char')

    def search_for_results(self, *args):
        self.clear_search_results()
        ext = self.extension.get()
        dir = self.directory.get()
        if not os.path.isdir(dir):
            self.insert_in_text_box('Invalid search directory.')
            return
        self.insert_in_text_box("Searching '{}' for all files with the '{}' extension...".format(dir, ext))
        results = self.search_folder(dir, ext)
        count = 0
        for result in results:
            count+=1
            self.insert_in_text_box('({}) {}'.format(count, result))
        self.total_results.set(count)
        self.insert_in_text_box('Finished.')
        if count==0:
            self.insert_in_text_box('No results found.')
            return

    def search_folder(self, folder, extension):
        items = os.listdir(folder)
        for item in items:
            full_item = os.path.join(folder, item)
            if os.path.isdir(full_item):
                yield from self.search_folder(full_item, extension)
            elif full_item.lower().endswith(extension):
                yield full_item

    def insert_in_text_box(self, text):
        self.results_text_box.configure(state='normal')
        text = text + '\n\n'
        self.results_text_box.insert('end', text)
        self.master.update()
        self.results_text_box.configure(state='disabled')

    def clear_search_results(self):
        self.results_text_box.configure(state='normal')
        self.results_text_box.delete('1.0', 'end')
        self.master.update()

        self.results_text_box.configure(state='disabled')


def main():
    root = tk.Tk()
    Searcher(root)
    root.mainloop()


if __name__ == '__main__':
    main()