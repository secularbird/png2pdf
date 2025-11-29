# Images to PDF

## Introduction
A cross-platform desktop application built with Tauri 2 and Vue 3 for converting multiple images into a PDF file. Users can select images, adjust their order, preview images, and export them as a PDF file.

## Tech Stack
- **Backend**: Tauri 2 (Rust)
- **Frontend**: Vue 3 + Vite
- **Image Processing**: image-rs
- **PDF Generation**: printpdf

## Features
1. **Select/Append Images**  
   - Supports selecting multiple images (PNG, JPG, JPEG, BMP, GIF, WebP).
   - Can append images to the existing list.

2. **Delete Images**  
   - Supports removing selected images from the list.

3. **Adjust Image Order**  
   - Supports moving images up or down to adjust their order.

4. **Image Preview**  
   - Real-time preview of selected images in the right panel.

5. **Convert to PDF**  
   - Merges selected images in order into a PDF file and saves it.

6. **Context Menu**  
   - Right-click on images in the list for quick deletion.

7. **Status Bar**  
   - Displays the count of selected images.

8. **Multi-language Support**
   - Automatically detects system language, supports Chinese and English.

9. **Dark Mode**
   - Automatically adapts to system dark/light theme.

## System Requirements
- Windows 10/11
- macOS 10.15+
- Linux (WebKit2GTK required)

## Development Setup

### Prerequisites
- Node.js 18+
- Rust 1.70+
- System dependencies (Linux):
  ```bash
  sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev
  ```

### Install Dependencies
```bash
npm install
```

### Development
```bash
npm run tauri dev
```

### Build
```bash
npm run tauri build
```

## Interface Description
- **Top Buttons**: For selecting/appending and deleting images.
- **Left List**: Displays selected images and their order.
- **Middle Buttons**: For adjusting image order.
- **Right Panel**: For previewing selected images.
- **Bottom Button**: For converting images to PDF.
- **Status Bar**: Shows the number of selected images.

## Notes
- Images will be merged into PDF in the order shown in the list.
- All images are automatically converted to RGB mode for PDF compatibility.

## Recommended IDE Setup
- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)

## License
MIT License
