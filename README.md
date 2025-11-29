# 图片转PDF / Images to PDF

## 简介
这是一个基于 Tauri 2 和 Vue 3 的跨平台桌面应用程序，用于将多张图片转换为 PDF 文件。用户可以选择图片、调整顺序、预览图片，并将其导出为 PDF 文件。

## 技术栈
- **后端**: Tauri 2 (Rust)
- **前端**: Vue 3 + Vite
- **图片处理**: image-rs
- **PDF生成**: printpdf

## 功能
1. **选择/追加图片**  
   - 支持选择多张图片（PNG、JPG、JPEG、BMP、GIF、WebP）。
   - 可以追加图片到已选择的列表中。

2. **删除图片**  
   - 支持从列表中删除选中的图片。

3. **调整图片顺序**  
   - 支持将图片上移或下移以调整顺序。

4. **图片预览**  
   - 在右侧面板中实时预览选中的图片。

5. **转换为 PDF**  
   - 将选中的图片按顺序合并为一个 PDF 文件并保存。

6. **右键菜单**  
   - 在图片列表中右键点击图片可快速删除。

7. **状态栏**  
   - 显示当前已选择的图片数量。

8. **多语言支持**
   - 自动检测系统语言，支持中文和英文。

9. **深色模式**
   - 自动适配系统深色/浅色主题。

## 系统要求
- Windows 10/11
- macOS 10.15+
- Linux (需要 WebKit2GTK)

## 开发环境配置

### 前置要求
- Node.js 18+
- Rust 1.70+
- 系统依赖 (Linux):
  ```bash
  sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev
  ```

### 安装依赖
```bash
npm install
```

### 开发运行
```bash
npm run tauri dev
```

### 构建应用
```bash
npm run tauri build
```

## 界面说明
- **顶部按钮**：用于选择/追加图片和删除图片。
- **左侧列表**：显示已选择的图片及其顺序。
- **中间按钮**：用于调整图片顺序。
- **右侧面板**：用于预览选中的图片。
- **底部按钮**：用于将图片转换为 PDF。
- **状态栏**：显示已选择图片的数量。

## 注意事项
- 图片将按列表中的顺序合并为 PDF。
- 所有图片会自动转换为 RGB 模式以兼容 PDF 格式。

## 推荐 IDE 配置
- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)

## 许可证
MIT License
