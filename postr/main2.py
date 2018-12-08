import tkinter
from tkinter import ttk

# Widgets
from tkinter import Tk, Label, Listbox

# Locations
from tkinter import LEFT, RIGHT, TOP, MULTIPLE, END

# Misc
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
from tkinter import filedialog


def setup(main_gui: Tk) -> Tk:
    main_gui.title('Postr')
    main_gui.geometry('600x600')
    return main_gui


def open_file_dialog() -> None:
    filename = filedialog.askopenfilename(
        initialdir='/', title='Select a file',
        filetypes=(('jpeg', '*.jpg'), ('png', '*.png'), ('All files', '*.*')),
    )

    print(filename)


def setup_interface_page(nb: ttk.Notebook) -> None:
    def setup_apis(page: ttk.Frame) -> None:
        api_box = Listbox(page, selectmode=MULTIPLE, width=15, height=8)
        apis = ['Facebook', 'Tumblr', 'Instagram', 'Twitter', 'Reddit', 'Youtube', 'Discord', 'Slack']
        list(map(lambda x: api_box.insert(END, x), apis))
        api_box.pack(side=LEFT)

    def setup_methods(page: ttk.Frame) -> None:
        method_box = Listbox(page, width=15, height=8)
        methods = ['Post Text', 'Post Picture']
        list(map(lambda x: method_box.insert(END, x), methods))
        method_box.pack(side=RIGHT)

    def setup_text_box(page: ttk.Frame) -> None:
        comment_area = ScrolledText(master=page, wrap=tkinter.WORD, width=40, height=6)
        comment_area.insert(tkinter.INSERT, 'Enter your comment here')
        comment_area.pack(side=TOP, anchor='n', pady=20, expand=True)

    def setup_file_dialog(page: ttk.Frame) -> None:
        ttk.Button(page, text='Browse a file', command=open_file_dialog).pack(side=TOP)

        file_label = Label(page, text='', width=30)
        file_label.pack(side=TOP)

    page = ttk.Frame(nb)
    page.pack()

    setup_apis(page)
    setup_methods(page)
    setup_file_dialog(page)
    setup_text_box(page)

    nb.add(page, text='Post Automation')


if __name__ == '__main__':
    # setupmain()
    root = setup(Tk())
    gui = ttk.Notebook(root)

    # Setup the interface page for post automation
    setup_interface_page(gui)

    # Setup the analytics page

    # second page
    page2 = ttk.Frame(gui)
    text = ScrolledText(page2)
    text.pack(expand=1, fill='both')
    gui.add(page2, text='Two')

    gui.pack(expand=1, fill='both')

    root.mainloop()
