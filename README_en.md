## Introduction
This is a desktop application based on `Tkinter` and `Pillow` for converting multiple images into a PDF file. Users can select images, adjust their order, preview them, and export them as a PDF file.

## Features
1. **Select/Add Images**  
   - Supports selecting multiple images (PNG, JPG, JPEG, BMP, GIF).
   - Allows adding images to the already selected list.

2. **Delete Images**  
   - Supports deleting selected images from the list.

3. **Adjust Image Order**  
   - Allows moving images up or down to adjust their order.

4. **Image Preview**  
   - Real-time preview of the selected image on the right canvas.

5. **Convert to PDF**  
   - Combines the selected images into a single PDF file in order and saves it.

6. **Context Menu**  
   - Right-click on an image in the list to quickly delete it.

7. **Status Bar**  
   - Displays the current number of selected images.

## Usage
1. Click the **Select/Add Images** button to choose the images to convert.
2. Adjust the order of images in the list or delete unnecessary ones.
3. Preview the images on the right canvas.
4. Click the **Convert to PDF** button, choose a save path, and generate the PDF file.

## System Requirements
- Python 3.x
- Dependencies:
  - `tkinter`
  - `Pillow`

## Install Dependencies
Run the following command in the terminal to install the required dependencies:
```bash
pip install pillow
```

## Run the Program
Run the following command in the terminal to start the program:
```bash
python main.py
```

## Interface Description
- **Top Buttons**: For selecting/adding images and deleting images.
- **Left List**: Displays the selected images and their order.
- **Right Canvas**: For previewing the selected image.
- **Bottom Button**: For converting images to a PDF.
- **Status Bar**: Displays the number of selected images.

## Notes
- Images will be merged into a PDF in the order they appear in the list.
- If an image has a transparent background (RGBA mode), it will be automatically converted to RGB mode to ensure compatibility with the PDF format.
