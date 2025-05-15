#!/usr/bin/env python3
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.ttk import *

from typing import Callable
from difflib import SequenceMatcher
from collections import deque

""" CUSTOMIZABLE TEXTAREA """

DEFAULT_W, DEFAULT_H = 30, 15
FONTFAMILY = "Consolas"
BG_ADDITION = "#79FF79"
BG_DELETION = "#FF7575"
BG_MODIFIED = "#FFE153"

""" CUSTOMIZABLE TEXTAREA"""


class TextArea(ScrolledText):
    def __init__(self, master: Misc):
        font = Font(master, family=FONTFAMILY)
        super().__init__(master, width=DEFAULT_W, height=DEFAULT_H, font=font)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop)

    def drop(self, event) -> None:
        path: str = event.data
        print("[]", path)

        if " " in path:
            stack = deque()
            for c in path:
                if c == "{":
                    stack.append(1)
                elif c == "}":
                    stack.pop()
                elif c == " " and not stack:
                    messagebox.showerror("差異比較", "不支援拖放多個檔案")
                    path = ""
                    break

        if path:
            path = path.strip("{}")
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                self.clear_text()
                self.insert("1.0", content)
            except UnicodeDecodeError:
                messagebox.showerror("差異比較", "Unicode 解碼錯誤")

    @property
    def lines(self) -> list[str]:
        return self.get("1.0", "end-1c").splitlines()

    def clear_text(self) -> None:
        self.delete("1.0", "end")

    def on_modify(self, callback: Callable) -> None:
        def func(_) -> None:
            if self.edit_modified():
                callback()
                self.edit_modified(False)
        self.bind("<<Modified>>", func)

    def highlight(self, bgcolor: str, row: int, start: int, end: int) -> None:
        start = f"{row}.{start}"
        end = f"{row}.{end}"

        tag = f"highlight_{start}_{end}"
        self.tag_add(tag, start, end)
        self.tag_config(tag, background=bgcolor)

    def clear_highlights(self) -> None:
        for tag in self.tag_names():
            if tag.startswith("highlight_"):
                self.tag_delete(tag)


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("差異比較")
        self.setup_ui()

        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def setup_ui(self):
        lframe = Frame(self, padding=10)
        lframe.pack(fill="both", expand=True, side="left")

        label1 = Label(lframe, text="原始文字")
        label1.pack(anchor="w", pady=(0, 10))

        self.textarea1 = TextArea(lframe)
        self.textarea1.on_modify(self.compare)
        self.textarea1.pack(fill="both", expand=True, pady=(0, 10))

        clsbtn1 = Button(lframe, text="清除", command=self.textarea1.clear_text)
        clsbtn1.pack(anchor="w")

        #

        rframe = Frame(self, padding=10)
        rframe.pack(fill="both", expand=True, side="left")

        label2 = Label(rframe, text="比較文字")
        label2.pack(anchor="w", pady=(0, 10))

        self.textarea2 = TextArea(rframe)
        self.textarea2.on_modify(self.compare)
        self.textarea2.pack(fill="both", expand=True, pady=(0, 10))

        clsbtn2 = Button(rframe, text="清除", command=self.textarea2.clear_text)
        clsbtn2.pack(anchor="w")

    def compare(self):
        self.textarea1.clear_highlights()
        self.textarea2.clear_highlights()

        lines1 = self.textarea1.lines
        lines2 = self.textarea2.lines

        n1 = len(lines1)
        n2 = len(lines2)

        for i in range(max(n1, n2)):
            row = i + 1
            matcher = SequenceMatcher(None, lines1[i] if i < n1 else "", lines2[i] if i < n2 else "")

            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                match tag:
                    case "equal":
                        pass
                    case "insert":
                        self.textarea2.highlight(BG_ADDITION, row, j1, j2)
                    case "delete":
                        self.textarea1.highlight(BG_DELETION, row, i1, i2)
                    case "replace":
                        self.textarea1.highlight(BG_MODIFIED, row, i1, i2)
                        self.textarea2.highlight(BG_MODIFIED, row, j1, j2)


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    finally:
        root = App()
        root.mainloop()
