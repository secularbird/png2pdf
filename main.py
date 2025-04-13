import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # Import ttk for Treeview
from PIL import Image, ImageTk  # Import ImageTk for preview

def update_status_bar():
    """Update the status bar with the count of selected and appended images."""
    status_bar.config(text=f"已选择图片: {len(images)}")

def select_images():
    # 弹出多选文件对话框
    file_paths = filedialog.askopenfilenames(
        title="选择图片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_paths:
        images.clear()
        images.extend(file_paths)
        update_treeview()  # Update the Treeview with the new order
        show_preview(0)  # Show preview of the first image
        update_status_bar()  # Update status bar

def append_images():
    """Append selected images to the existing list."""
    file_paths = filedialog.askopenfilenames(
        title="追加图片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_paths:
        images.extend(file_paths)  # Append new images to the existing list
        update_treeview()  # Update the Treeview with the new order
        update_status_bar()  # Update status bar

def delete_image(index=None):
    """Delete the selected or specified image from the list."""
    if index is None:
        selected_item = treeview_images.selection()
        if selected_item:
            index = treeview_images.index(selected_item[0])
        else:
            messagebox.showwarning("警告", "请先选择要删除的图片！")
            return
    del images[index]  # Remove the image from the list
    update_treeview()
    canvas_preview.delete("all")  # Clear the preview if an image is deleted

def update_treeview():
    """Update the Treeview to display the current order of images with action buttons."""
    treeview_images.delete(*treeview_images.get_children())  # Clear the Treeview
    max_path_length = int(treeview_images.column("Path", "width") * 0.2)  # 20% of column width
    for i, img in enumerate(images):
        truncated_path = img if len(img) <= max_path_length else f"...{img[-max_path_length:]}"
        treeview_images.insert("", "end", values=(i + 1, truncated_path, ""))  # Add order, truncated filename, and placeholder
    update_action_buttons()

def update_action_buttons():
    """Place action buttons in the Treeview."""
    for i, item in enumerate(treeview_images.get_children()):
        bbox = treeview_images.bbox(item, column=2)  # Get bounding box for the action column
        if bbox:
            x, y, width, height = bbox
            btn_delete = tk.Button(treeview_images, text="删除", command=lambda idx=i: delete_image(idx))
            btn_delete.place(x=x + 5, y=y + 2, width=40, height=height - 4)

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

def move_up(index=None):
    """Move the selected or specified image up in the list."""
    if index is None:
        selected_item = treeview_images.selection()
        if selected_item:
            index = treeview_images.index(selected_item[0])
        else:
            return
    if index > 0:
        images[index], images[index - 1] = images[index - 1], images[index]
        update_treeview()
        treeview_images.selection_set(treeview_images.get_children()[index - 1])
        show_preview(index - 1)

def move_down(index=None):
    """Move the selected or specified image down in the list."""
    if index is None:
        selected_item = treeview_images.selection()
        if selected_item:
            index = treeview_images.index(selected_item[0])
        else:
            return
    if index < len(images) - 1:
        images[index], images[index + 1] = images[index + 1], images[index]
        update_treeview()
        treeview_images.selection_set(treeview_images.get_children()[index + 1])
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

def show_context_menu(event):
    """Show the context menu for Treeview."""
    selected_item = treeview_images.identify_row(event.y)
    if selected_item:
        treeview_images.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)

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

btn_append = tk.Button(root, text="追加图片", command=append_images)  # New button to append images
btn_append.grid(row=0, column=1, pady=10, padx=10, sticky="ew")  # Expand horizontally

btn_delete = tk.Button(root, text="删除图片", command=lambda: delete_image())  # Delete Image button
btn_delete.grid(row=0, column=2, pady=10, padx=10, sticky="ew")  # Expand horizontally

frame = tk.Frame(root)
frame.grid(row=1, column=0, columnspan=4, sticky="nsew")  # Expand in all directions
frame.rowconfigure(0, weight=1)  # Allow Treeview and Canvas to resize vertically
frame.columnconfigure(0, weight=3)  # Treeview takes more space
frame.columnconfigure(1, weight=1)  # Canvas takes less space

treeview_images = ttk.Treeview(frame, columns=("Order", "Path", "Actions"), show="headings", height=8)
treeview_images.heading("Order", text="顺序")
treeview_images.heading("Path", text="图片路径")
treeview_images.heading("Actions", text="操作")
treeview_images.column("Order", width=50, anchor="center")  # Adjust column width
treeview_images.column("Path", width=400, anchor="w")  # Adjust column width
treeview_images.column("Actions", width=150, anchor="center")  # Adjust column width
treeview_images.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
treeview_images.bind("<<TreeviewSelect>>", on_treeview_select)  # Bind selection event
treeview_images.bind("<Button-3>", show_context_menu)  # Bind right-click for context menu

canvas_preview = tk.Canvas(frame, bg="gray")  # Canvas for preview
canvas_preview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
canvas_preview.bind("<Configure>", on_canvas_resize)  # Bind resize event

btn_frame = tk.Frame(root)  # Frame for move buttons
btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
btn_frame.columnconfigure(0, weight=1)  # Allow buttons to resize horizontally

btn_move_up = tk.Button(btn_frame, text="上移", command=move_up)  # Move Up button
btn_move_up.pack(side=tk.LEFT, padx=5)

btn_move_down = tk.Button(btn_frame, text="下移", command=move_down)  # Move Down button
btn_move_down.pack(side=tk.LEFT, padx=5)

btn_convert = tk.Button(root, text="转换为PDF", command=convert_to_pdf)
btn_convert.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="ew")  # Expand horizontally

# Add a status bar at the bottom of the window
status_bar = tk.Label(root, text="已选择图片: 0", anchor="w", relief="sunken")
status_bar.grid(row=4, column=0, columnspan=4, sticky="ew")  # Expand horizontally

# Create a context menu for the Treeview
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="删除图片", command=lambda: delete_image())

root.mainloop()

