import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def select_images():
    # 弹出多选文件对话框
    file_paths = filedialog.askopenfilenames(
        title="选择图片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_paths:
        images.clear()
        images.extend(file_paths)
        lbl_selected.config(text=f"已选择 {len(images)} 张图片")

def convert_to_pdf():
    if not images:
        messagebox.showwarning("警告", "请先选择图片！")
        return

    img_list = []
    for img_path in images:
        img = Image.open(img_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img_list.append(img)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="保存 PDF 文件"
    )
    if save_path:
        img_list[0].save(save_path, save_all=True, append_images=img_list[1:])
        messagebox.showinfo("成功", f"PDF 已保存到\n{save_path}")

# 主窗口
root = tk.Tk()
root.title("图片转PDF")
root.geometry("300x200")

images = []

# 按钮和标签
btn_select = tk.Button(root, text="选择图片", command=select_images)
btn_select.pack(pady=10)

lbl_selected = tk.Label(root, text="未选择图片")
lbl_selected.pack(pady=5)

btn_convert = tk.Button(root, text="转换为PDF", command=convert_to_pdf)
btn_convert.pack(pady=20)

root.mainloop()

