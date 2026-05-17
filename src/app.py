#!/usr/bin/env python3
"""
数据可视化工具 - 从CSV生成图表
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import tkinter as tk

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_DEP = True
except ImportError:
    HAS_DEP = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("数据可视化工具 v1.0")
        root.geometry("900x700")
        self.df = None
        self.file = None
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#00695c", height=50)
        f.pack(fill="x")
        tk.Label(f, text="📈 数据可视化工具", font=("Arial",14,"bold"),
                 fg="white", bg="#00695c").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 顶部控制
        cf = tk.Frame(main)
        cf.pack(fill="x", pady=5)
        tk.Button(cf, text="选择CSV文件", command=self.load_file,
                  bg="#00695c", fg="white", padx=15).pack(side="left", padx=5)
        
        tk.Label(cf, text="图表类型：").pack(side="left", padx=(20,5))
        self.chart_type = ttk.Combobox(cf, values=["折线图","柱状图","散点图","饼图"],
                                        state="readonly", width=10)
        self.chart_type.set("折线图")
        self.chart_type.pack(side="left", padx=5)
        
        tk.Button(cf, text="生成图表", command=self.plot,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=15).pack(side="left", padx=20)
        
        # 列选择
        lf = tk.Frame(main)
        lf.pack(fill="x", pady=10)
        tk.Label(lf, text="X轴：").pack(side="left")
        self.x_col = ttk.Combobox(lf, state="readonly", width=15)
        self.x_col.pack(side="left", padx=5)
        tk.Label(lf, text="Y轴：").pack(side="left", padx=(20,5))
        self.y_col = ttk.Combobox(lf, state="readonly", width=15)
        self.y_col.pack(side="left", padx=5)
        
        # 图表区域
        self.canvas_frame = tk.Frame(main, bg="white", relief="groove", bd=2)
        self.canvas_frame.pack(fill="both", expand=True, pady=10)
        
        self.status = tk.Label(main, text="请选择CSV文件",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def load_file(self):
        if not HAS_DEP:
            messagebox.showerror("缺少依赖", "请运行：pip install pandas matplotlib")
            return
        f = filedialog.askopenfilename(title="选择CSV文件",
             filetypes=[("CSV文件","*.csv *.tsv")])
        if f:
            self.file = f
            self.df = pd.read_csv(f)
            cols = self.df.columns.tolist()
            self.x_col["values"] = cols
            self.y_col["values"] = cols
            if cols:
                self.x_col.set(cols[0])
                self.y_col.set(cols[1] if len(cols) > 1 else cols[0])
            self.status.config(text=f"已加载：{Path(f).name}（{len(self.df)}行）")
    
    def plot(self):
        if self.df is None:
            messagebox.showwarning("提示", "请先加载CSV文件")
            return
        
        x = self.x_col.get()
        y = self.y_col.get()
        ct = self.chart_type.get()
        
        try:
            # 清除旧图表
            for w in self.canvas_frame.winfo_children():
                w.destroy()
            
            fig, ax = plt.subplots(figsize=(8, 5))
            
            if ct == "折线图":
                ax.plot(self.df[x], self.df[y], marker="o")
            elif ct == "柱状图":
                ax.bar(self.df[x], self.df[y])
            elif ct == "散点图":
                ax.scatter(self.df[x], self.df[y])
            elif ct == "饼图":
                ax.pie(self.df[y], labels=self.df[x], autopct="%1.1f%%")
            
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"{y} vs {x}")
            ax.grid(True, alpha=0.3)
            
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            self.status.config(text=f"✅ 图表已生成")
        except Exception as e:
            messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
