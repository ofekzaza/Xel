import tkinter as tk
from functools import partial
from typing import Callable, Iterable, Tuple, List, Any


def _add_command(menu: tk.Menu, option: str, update_command: Callable[[str], None], are_options_colors: bool) -> None:
    if are_options_colors:
        menu.add_command(label=option, command=partial(update_command, option), background=option)
    else:
        menu.add_command(label=option, command=partial(update_command, option))


class OptionsMenu(tk.Menubutton):
    """
    tkinter menubutton, where all the options call the same command, and the only difference is the value of the options,
    like the colors menus.
    """
    def __init__(
            self,
            root: tk.Frame,
            options: Iterable[str],
            update_command: Callable[[str], None],
            are_options_colors: bool = False,
            cascade_options: List[Tuple[str, List[str]]] = [],
            **kw: Any
    ) -> None:
        """

        :param root: maser frame
        :param options: base options of the menu
        :param update_command: function to call when an option is chosen
        :param are_options_colors: are options names of colors
        :param cascade_options: sub options, see tk.menu cascade
        :param kw: see tk.Menubutton parameters
        """
        super().__init__(root, **kw)
        self.menu = tk.Menu(self, tearoff=0)
        self["menu"] = self.menu
        self.options = options
        for option in options:
            _add_command(self.menu, option, update_command, are_options_colors)

        for (name, sub_options) in cascade_options:
            sub_menu = tk.Menu(self.menu, tearoff=0)
            for sub_option in sub_options:
                _add_command(sub_menu, sub_option, update_command, are_options_colors)
            if are_options_colors:
                self.menu.add_cascade(label=name, menu=sub_menu, background=name)
            else:
                self.menu.add_cascade(label=name, menu=sub_menu)
