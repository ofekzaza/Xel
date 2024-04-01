import tkinter as tk
from tkinter import END
from typing import Callable, Optional

from tksheet import EventDataDict


def popup_input_window(
        validation: Callable[[str], bool],
        logic: Callable[[str], None],
        frame: Optional[tk.Frame] = None,
        caller: Optional[tk.Widget] = None,
        default_value: Optional[str] = None,
        background_text: str = "",
        button_text: str = "OK"
) -> None:
    """
    opens a pop up window, which allows for input receiving.
    the input is received using a entry widget
    :param validation: Validation for the input, passes the input forwards only if the validation passes
    :param logic: what to execute with the input as parameter
    :param frame: master frame of the window
    :param caller: which component called the window
    :param default_value: default value for input
    :param background_text: background text which will disappear when starting writing in the entry box
    :param button_text: text to display on the ok button
    :return: None
    """
    def get_new_name(event: Optional[EventDataDict] = None) -> object:
        data = entry.get()
        if validation(data):
            logic(data)
            window.destroy()
        return data

    def handle_background_text(event: Optional[EventDataDict] = None) -> None:
        if entry.get() == background_text:
            entry.delete(0, END)
            if default_value == entry.get():
                entry.insert(END, default_value)

    window = tk.Tk()

    if frame:
        x = frame.winfo_rootx() + (caller.winfo_x() if caller else 0)
        y = frame.winfo_rooty() + (caller.winfo_y() if caller else 0) - 50  # -50 so it will be a bit higher than caller

        # Set the window's geometry (position only)
        window.geometry(f"+{x}+{y}")

    entry = tk.Entry(window)
    entry.pack()
    if background_text:
        entry.insert(END, background_text)
    elif default_value:
        entry.insert(END, default_value)
    ok_button = tk.Button(window, text=button_text, command=get_new_name)

    entry.bind("<Button-1>", handle_background_text)
    window.bind("<Return>", get_new_name)

    ok_button.pack()
    entry.focus_set()
    window.wait_window()
