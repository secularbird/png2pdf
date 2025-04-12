import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # Import ttk for Treeview
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
        update_treeview()  # Update the Treeview with the new order
        show_preview(0)  # Show preview of the first image

def update_treeview():
    """Update the Treeview to display the current order of images with truncated paths."""
    treeview_images.delete(*treeview_images.get_children())  # Clear the Treeview
    max_path_length = int(treeview_images.column("Path", "width") * 0.2)  # 20% of column width
    for i, img in enumerate(images):
        truncated_path = img if len(img) <= max_path_length else f"...{img[-max_path_length:]}"
        treeview_images.insert("", "end", values=(i + 1, truncated_path))  # Add order and truncated filename

def show_preview(index):
    if 0 <= index < len(images):
        img_path = images[index]
        img = Image.open(img_path)
        canvas_width = canvas_preview.winfo_width()
        canvas_height = canvas_preview.winfo_height()
        img.thumbnail((canvas_width, canvas_height))  # Resize to fit canvas
        img_tk = ImageTk.PhotoImage(img)
        canvas_preview.image = img_tk  # Keep a reference to avoid garbage collection
        canvas_preview.delete("all")  # Clear previous image
        canvas_preview.create_image(0, 0, anchor=tk.NW, image=img_tk)

def on_canvas_resize(event):
    if treeview_images.selection():
        index = treeview_images.index(treeview_images.selection()[0])
        show_preview(index)

def on_treeview_select(event):
    selected_item = treeview_images.selection()
    if selected_item:
        index = treeview_images.index(selected_item[0])
        show_preview(index)

def move_up():
    selected_item = treeview_images.selection()
    if selected_item:
        index = treeview_images.index(selected_item[0])
        if index > 0:
            # Swap in the images list
            images[index], images[index - 1] = images[index - 1], images[index]
            update_treeview()  # Update the Treeview with the new order
            treeview_images.selection_set(treeview_images.get_children()[index - 1])  # Reselect the moved item
            show_preview(index - 1)

def move_down():
    selected_item = treeview_images.selection()
    if selected_item:
        index = treeview_images.index(selected_item[0])
        if index < len(images) - 1:
            # Swap in the images list
            images[index], images[index + 1] = images[index + 1], images[index]
            update_treeview()  # Update the Treeview with the new order
            treeview_images.selection_set(treeview_images.get_children()[index + 1])  # Reselect the moved item
            show_preview(index + 1)

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

# Configure root window to allow resizing
root.rowconfigure(1, weight=1)  # Allow resizing of the frame containing the Treeview and canvas
root.columnconfigure(0, weight=1)

images = []

# 按钮和标签
btn_select = tk.Button(root, text="选择图片", command=select_images)
btn_select.grid(row=0, column=0, pady=10, padx=10, sticky="ew")  # Expand horizontally

lbl_selected = tk.Label(root, text="未选择图片")
lbl_selected.grid(row=0, column=1, pady=10, padx=10, sticky="ew")  # Expand horizontally

frame = tk.Frame(root)
frame.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Expand in all directions
frame.rowconfigure(0, weight=1)  # Allow Treeview and Canvas to resize vertically
frame.columnconfigure(0, weight=3)  # Treeview takes more space
frame.columnconfigure(1, weight=1)  # Canvas takes less space

treeview_images = ttk.Treeview(frame, columns=("Order", "Path"), show="headings", height=8)
treeview_images.heading("Order", text="顺序")
treeview_images.heading("Path", text="图片路径")
treeview_images.column("Order", width=50, anchor="center")  # Adjust column width
treeview_images.column("Path", width=400, anchor="w")  # Adjust column width
treeview_images.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
treeview_images.bind("<<TreeviewSelect>>", on_treeview_select)  # Bind selection event

canvas_preview = tk.Canvas(frame, bg="gray")  # Canvas for preview
canvas_preview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
canvas_preview.bind("<Configure>", on_canvas_resize)  # Bind resize event

btn_frame = tk.Frame(root)  # Frame for move buttons
btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
btn_frame.columnconfigure(0, weight=1)  # Allow buttons to resize horizontally

btn_move_up = tk.Button(btn_frame, text="上移", command=move_up)  # Move Up button
btn_move_up.pack(side=tk.LEFT, padx=5)

btn_move_down = tk.Button(btn_frame, text="下移", command=move_down)  # Move Down button
btn_move_down.pack(side=tk.LEFT, padx=5)

btn_convert = tk.Button(root, text="转换为PDF", command=convert_to_pdf)
btn_convert.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")  # Expand horizontally

root.mainloop()

