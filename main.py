import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Import ImageTk for preview

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
        listbox_images.delete(0, tk.END)  # Clear the listbox
        for img in images:
            listbox_images.insert(tk.END, img)  # Add each image to the listbox
        show_preview(0)  # Show preview of the first image

def show_preview(index):
    if 0 <= index < len(images):
        img_path = images[index]
        img = Image.open(img_path)
        img.thumbnail((200, 200))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)
        canvas_preview.image = img_tk  # Keep a reference to avoid garbage collection
        canvas_preview.create_image(0, 0, anchor=tk.NW, image=img_tk)

def on_listbox_select(event):
    if listbox_images.curselection():
        index = listbox_images.curselection()[0]
        show_preview(index)

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
root.geometry("600x400")  # Adjusted size to fit the preview

images = []

# 按钮和标签
btn_select = tk.Button(root, text="选择图片", command=select_images)
btn_select.pack(pady=10)

lbl_selected = tk.Label(root, text="未选择图片")
lbl_selected.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

listbox_images = tk.Listbox(frame, height=8, width=50)  # Listbox to display images
listbox_images.pack(side=tk.LEFT, padx=10)
listbox_images.bind("<<ListboxSelect>>", on_listbox_select)  # Bind selection event

canvas_preview = tk.Canvas(frame, width=200, height=200, bg="gray")  # Canvas for preview
canvas_preview.pack(side=tk.RIGHT)

btn_convert = tk.Button(root, text="转换为PDF", command=convert_to_pdf)
btn_convert.pack(pady=20)

root.mainloop()

