import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

class HighlightTextDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("文字背景顏色示範")
        self.root.geometry("600x400")
        
        # 創建 scrolledtext 控件
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 添加一些示範文字
        sample_text = "這是一個示範如何在 scrolledtext 中為特定範圍的文字添加背景顏色的例子。\n\n您可以選擇任何範圍的文字並為其添加不同的背景顏色。"
        self.text_area.insert(tk.END, sample_text)
        
        # 創建操作框架
        control_frame = ttk.Frame(root)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # 添加顏色選擇器
        ttk.Label(control_frame, text="選擇顏色:").pack(side=tk.LEFT, padx=5)
        self.color_var = tk.StringVar(value="yellow")
        colors = ["yellow", "lightblue", "lightgreen", "pink", "lightgray"]
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var, values=colors, width=10)
        color_combo.pack(side=tk.LEFT, padx=5)
        
        # 添加高亮按鈕
        highlight_btn = ttk.Button(control_frame, text="為選取文字添加背景顏色", command=self.highlight_text)
        highlight_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加清除按鈕
        clear_btn = ttk.Button(control_frame, text="清除所有背景顏色", command=self.clear_highlights)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def highlight_text(self):
        """為選取的文字添加背景顏色"""
        # 獲取當前選擇的文字範圍
        try:
            start_pos = self.text_area.index(tk.SEL_FIRST)
            end_pos = self.text_area.index(tk.SEL_LAST)
            
            # 創建一個唯一的標籤名稱（使用位置作為標籤名的一部分）
            tag_name = f"highlight_{start_pos}_{end_pos}"
            
            # 為這個範圍添加標籤
            self.text_area.tag_add(tag_name, start_pos, end_pos)
            
            # 設置標籤的背景顏色
            color = self.color_var.get()
            self.text_area.tag_config(tag_name, background=color)
            
        except tk.TclError:
            # 如果沒有選擇文字，則不做任何操作
            pass
    
    def clear_highlights(self):
        """清除所有的背景顏色標籤"""
        # 獲取所有標籤
        all_tags = self.text_area.tag_names()
        
        # 刪除以 "highlight_" 開頭的標籤
        for tag in all_tags:
            if str(tag).startswith("highlight_"):
                self.text_area.tag_delete(tag)

# 創建主窗口並運行應用
if __name__ == "__main__":
    root = tk.Tk()
    app = HighlightTextDemo(root)
    root.mainloop()