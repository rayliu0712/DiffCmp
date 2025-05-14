from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import *
from tkinter.ttk import *
import difflib


class DiffChecker(Tk):
    def __init__(self):
        super().__init__()
        self.title("Diff Checker")

        # 設置界面
        self.setup_ui()

        # 在所有元件都放置好後，更新視窗並設定最小尺寸
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def setup_ui(self):
        """設置使用者介面"""
        # 設置主要容器框架
        main_frame = Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        # 設置頂部控制區域
        control_frame = Frame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))

        # 建立比較按鈕
        self.compare_btn = Button(control_frame, text="高亮比較差異", command=self.compare_texts)
        self.compare_btn.pack(side="left")

        # 設置內容區域框架
        content_frame = Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # 左側框架
        lframe = Frame(content_frame)
        lframe.pack(fill="both", expand=True, side="left", padx=(0, 5))

        Label(lframe, text="原始文字").pack(anchor="w", pady=(0, 5))

        self.text1 = ScrolledText(lframe, width=50, height=20, font=("Consolas", 10))
        self.text1.pack(fill="both", expand=True)

        # 右側框架
        rframe = Frame(content_frame)
        rframe.pack(fill="both", expand=True, side="left", padx=(5, 0))

        Label(rframe, text="比較文字").pack(anchor="w", pady=(0, 5))

        self.text2 = ScrolledText(rframe, width=50, height=20, font=("Consolas", 10))
        self.text2.pack(fill="both", expand=True)

    def compare_texts(self):
        """比較兩個文字區域中的內容並高亮差異"""
        try:
            # 獲取文字內容
            text1_content = self.text1.get("1.0", "end-1c")
            text2_content = self.text2.get("1.0", "end-1c")

            # 清除先前的標記
            for text_widget in [self.text1, self.text2]:
                for tag in text_widget.tag_names():
                    if tag != "sel":  # 保留 selection 標記
                        text_widget.tag_remove(tag, "1.0", "end")

            # 創建 tag 用於高亮差異
            self.text1.tag_configure("diff_delete", background="#ffdddd")
            self.text2.tag_configure("diff_insert", background="#ddffdd")

            # 執行字元級別的差異對比
            matcher = difflib.SequenceMatcher(None, text1_content, text2_content)

            # 處理差異並高亮
            for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
                if opcode == 'equal':
                    continue

                # 高亮文字
                if opcode in ['replace', 'delete']:
                    self.highlight_text(self.text1, i1, i2, "diff_delete")

                if opcode in ['replace', 'insert']:
                    self.highlight_text(self.text2, j1, j2, "diff_insert")

        except Exception as e:
            print(f"比較時發生錯誤: {str(e)}")

    def highlight_text(self, text_widget, start_index, end_index, tag_name):
        """高亮指定文字區域"""
        # 將字元索引轉換為 Tkinter 文字索引
        start_row, start_col = self.index_to_position(text_widget, start_index)
        end_row, end_col = self.index_to_position(text_widget, end_index)

        text_widget.tag_add(tag_name, f"{start_row}.{start_col}", f"{end_row}.{end_col}")

    def index_to_position(self, text_widget, index):
        """將字元索引轉換為行列位置"""
        text = text_widget.get("1.0", "end-1c")

        if index >= len(text):
            # 如果索引超出範圍，返回文本末尾位置
            return self.get_line_col(text, len(text))

        return self.get_line_col(text, index)

    def get_line_col(self, text, index):
        """計算指定字元索引的行列位置"""
        lines = text[:index].split('\n')
        line = len(lines)
        col = len(lines[-1])
        return line, col


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app = DiffChecker()
        app.mainloop()
