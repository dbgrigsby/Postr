import tkinter
from tkinter.ttk import Notebook

# Widgets
from tkinter import Tk, Listbox, Frame, Button

# Locations
from tkinter import LEFT, TOP, MULTIPLE, END, BOTTOM

# Misc Widgets
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
from tkinter import filedialog


def setup(main_gui: Tk) -> Tk:
    main_gui.title('Postr')
    main_gui.geometry('600x600')
    return main_gui


def setup_apis(page: Frame) -> Listbox:
    page_l = Frame(page)
    page_l.pack(side=LEFT, padx=20)

    api_box = Listbox(page_l, selectmode=MULTIPLE, width=15, height=8, font=('Times', 16))
    apis = ['Facebook', 'Tumblr', 'Instagram', 'Twitter', 'Reddit', 'Youtube', 'Discord', 'Slack']
    list(map(lambda x: api_box.insert(END, x), apis))
    api_box.pack(side=LEFT)
    return api_box


def setup_text_box(page: Frame) -> ScrolledText:
    comment_area = ScrolledText(master=page, wrap=tkinter.WORD, width=40, height=6)
    comment_area.insert(tkinter.INSERT, 'Enter your comment here')
    comment_area.pack(side=TOP, anchor='n', pady=20, expand=True)
    return comment_area


class GUI():
    def __init__(self) -> None:
        # setupmain()
        self.root = setup(Tk())
        self.gui = Notebook(self.root)

        # Setup the posting page
        page1 = Frame(self.gui)
        page1.pack()

        self.api_box = setup_apis(page1)
        self.setup_automation_buttons(page1)
        # self.text_box = setup_text_box(page1)
        # self.file_button = self.setup_file_dialog(page1)
        # self.filepath = ''
        self.gui.add(page1, text='Post Automation')

        # Setup the analytics page
        page2 = Frame(self.gui)
        text = ScrolledText(page2)
        text.pack(expand=1, fill='both')
        self.gui.add(page2, text='Two')

        # Pack out gui
        self.gui.pack(expand=1, fill='both')

    def setup_automation_buttons(self, page: Frame) -> None:
        page_l = Frame(page)
        page_l.pack(side=LEFT)

        Button(page_l, text='Post text', command=self.post_text).pack(side=TOP)
        Button(page_l, text='Post picture w/text', command=self.post_pic).pack(side=BOTTOM, anchor='s')

    def post_text(self) -> None:
        pass

    def post_pic(self) -> None:
        pass

    def setup_file_dialog(self, page: Frame) -> Button:
        b = Button(page, text='Browse a file', command=self.open_file_dialog)
        b.pack(side=TOP)
        return b

    def open_file_dialog(self) -> None:
        filename = filedialog.askopenfilename(
            initialdir='/', title='Select a file',
            filetypes=(('jpeg', '*.jpg'), ('png', '*.png'), ('All files', '*.*')),
        )
        self.filepath = filename


if __name__ == '__main__':
    g = GUI()
    g.root.mainloop()
