#!/usr/bin/env python3
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import *
from tkinter.ttk import *
from typing import Callable, Optional
from difflib import SequenceMatcher

DEFAULT_TEXTAREA_WIDTH, DEFAULT_TEXTAREA_HEIGHT = 30, 15
HIGHLIGHT_ADDITION = "#79FF79"
HIGHLIGHT_DELETION = "#FF7575"
HIGHLIGHT_MODIFIED = "#FFE153"

type RowCol = tuple[int, int]


class TextArea(ScrolledText):
    def __init__(self, master: Misc):
        font = Font(master, family="Consolas")
        super().__init__(master, width=DEFAULT_TEXTAREA_WIDTH, height=DEFAULT_TEXTAREA_HEIGHT, font=font)
        self._on_modify = None

    @property
    def text(self) -> str:
        return self.get("1.0", "end-1c")

    @text.setter
    def text(self, new_text: str) -> None:
        self.clear_text()
        self.insert(INSERT, new_text)

    def clear_text(self) -> None:
        self.delete("1.0", END)

    @property
    def on_modify(self) -> Optional[Callable]:
        return self._on_modify

    @on_modify.setter
    def on_modify(self, callback: Optional[Callable]) -> None:
        self._on_modify = callback

        if callback is None:
            self.unbind("<<Modified>>")
        else:
            def func(event) -> None:
                if self.edit_modified():
                    callback()
                    self.edit_modified(False)

            self.bind("<<Modified>>", func)

    def highlight(self, bgcolor: str, start_rc: RowCol, end_rc: Optional[RowCol] = None) -> None:
        lines = self.text.splitlines()

        if end_rc is None:
            end_rc = (len(lines), len(lines[-1]))

        for row in range(start_rc[0], end_rc[0] + 1):
            l = f"{row}.0"
            r = f"{row}.{len(lines[row - 1])}"

            if row == start_rc[0]:
                l = f"{row}.{start_rc[1]}"
            if row == end_rc[0]:
                r = f"{row}.{end_rc[1]}"

            tag = f"highlight_{l}_{r}"
            self.tag_add(tag, l, r)
            self.tag_config(tag, background=bgcolor)

    def clear_highlights(self) -> None:
        for tag in self.tag_names():
            if tag.startswith("highlight_"):
                self.tag_delete(tag)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("差異比較器")
        self.setup_ui()

        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def setup_ui(self):
        lframe = Frame(self, padding=10)
        lframe.pack(fill="both", expand=True, side="left")

        label1 = Label(lframe, text="原始文字")
        label1.pack(anchor="w", pady=(0, 10))

        self.textarea1 = TextArea(lframe)
        self.textarea1.on_modify = self.compare
        self.textarea1.pack(fill="both", expand=True, pady=(0, 10))

        btn1 = Button(lframe, text="清除", command=self.textarea1.clear_text)
        btn1.pack(anchor="w")

        #

        rframe = Frame(self, padding=10)
        rframe.pack(fill="both", expand=True, side="left")

        label2 = Label(rframe, text="比較文字")
        label2.pack(anchor="w", pady=(0, 10))

        self.textarea2 = TextArea(rframe)
        self.textarea2.on_modify = self.compare
        self.textarea2.pack(fill="both", expand=True, pady=(0, 10))

        btn2 = Button(rframe, text="清除", command=self.textarea2.clear_text)
        btn2.pack(anchor="w")

    def compare(self):
        self.textarea1.clear_highlights()
        self.textarea2.clear_highlights()

        lines1 = self.textarea1.text.splitlines()
        lines2 = self.textarea2.text.splitlines()

        n1 = len(lines1)
        n2 = len(lines2)

        for i, (ln1, ln2) in enumerate(zip(lines1, lines2)):
            row = i + 1
            matcher = SequenceMatcher(None, ln1, ln2)

            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                match tag:
                    case "equal":
                        pass
                    case "insert":
                        self.textarea2.highlight(HIGHLIGHT_ADDITION, (row, j1), (row, j2))
                    case "delete":
                        self.textarea1.highlight(HIGHLIGHT_DELETION, (row, i1), (row, i2))
                    case "replace":
                        self.textarea1.highlight(HIGHLIGHT_MODIFIED, (row, i1), (row, i2))
                        self.textarea2.highlight(HIGHLIGHT_MODIFIED, (row, j1), (row, j2))

        if n1 < n2:  # insert
            self.textarea2.highlight(HIGHLIGHT_ADDITION, (n1 + 1, 0))
        elif n1 > n2:  # delete
            self.textarea1.highlight(HIGHLIGHT_DELETION, (n2 + 1, 0))


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    finally:
        root = App()
        root.mainloop()
