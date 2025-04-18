## 简介
这是一个基于 `Tkinter` 和 `Pillow` 的桌面应用程序，用于将多张图片转换为 PDF 文件。用户可以选择图片、调整顺序、预览图片，并将其导出为 PDF 文件。

## 功能
1. **选择/追加图片**  
   - 支持选择多张图片（PNG、JPG、JPEG、BMP、GIF）。
   - 可以追加图片到已选择的列表中。

2. **删除图片**  
   - 支持从列表中删除选中的图片。

3. **调整图片顺序**  
   - 支持将图片上移或下移以调整顺序。

4. **图片预览**  
   - 在右侧画布中实时预览选中的图片。

5. **转换为 PDF**  
   - 将选中的图片按顺序合并为一个 PDF 文件并保存。

6. **右键菜单**  
   - 在图片列表中右键点击图片可快速删除。

7. **状态栏**  
   - 显示当前已选择的图片数量。

## 使用方法
1. 点击 **选择/追加图片** 按钮，选择要转换的图片。
2. 在图片列表中调整图片顺序，或删除不需要的图片。
3. 在右侧画布中预览图片。
4. 点击 **转换为PDF** 按钮，选择保存路径并生成 PDF 文件。

## 系统要求
- Python 3.x
- 依赖库：
  - `tkinter`
  - `Pillow`

## 安装依赖
在终端中运行以下命令安装所需依赖：
```bash
pip install pillow
```

## 运行程序
在终端中运行以下命令启动程序：
```bash
python main.py
```

## 界面说明
- **顶部按钮**：用于选择/追加图片和删除图片。
- **左侧列表**：显示已选择的图片及其顺序。
- **右侧画布**：用于预览选中的图片。
- **底部按钮**：用于将图片转换为 PDF。
- **状态栏**：显示已选择图片的数量。

## 注意事项
- 图片将按列表中的顺序合并为 PDF。
- 如果图片为透明背景（RGBA 模式），会自动转换为 RGB 模式以兼容 PDF 格式。