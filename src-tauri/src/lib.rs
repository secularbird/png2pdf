use base64::{engine::general_purpose::STANDARD, Engine};
use printpdf::{
    ColorBits, ColorSpace, Image, ImageTransform, ImageXObject, Mm, PdfDocument,
    PdfLayerReference, Px,
};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{BufWriter, Cursor};

// Alias the image crate types we need
use ::image::DynamicImage;
use ::image::GenericImageView;
use ::image::ImageFormat;

#[derive(Debug, Serialize, Deserialize)]
pub struct ImageInfo {
    pub path: String,
    pub name: String,
    pub preview: String,
}

#[tauri::command]
fn get_image_preview(path: &str, max_width: u32, max_height: u32) -> Result<ImageInfo, String> {
    let img = ::image::open(path).map_err(|e| format!("Failed to open image: {}", e))?;

    // Create thumbnail
    let thumbnail = img.thumbnail(max_width, max_height);

    // Encode to PNG bytes
    let mut png_data = Cursor::new(Vec::new());
    thumbnail
        .write_to(&mut png_data, ImageFormat::Png)
        .map_err(|e| format!("Failed to encode image: {}", e))?;

    let base64_preview = STANDARD.encode(png_data.into_inner());

    let name = std::path::Path::new(path)
        .file_name()
        .and_then(|n| n.to_str())
        .unwrap_or("unknown")
        .to_string();

    Ok(ImageInfo {
        path: path.to_string(),
        name,
        preview: format!("data:image/png;base64,{}", base64_preview),
    })
}

#[tauri::command]
fn convert_images_to_pdf(image_paths: Vec<String>, output_path: &str) -> Result<String, String> {
    if image_paths.is_empty() {
        return Err("No images provided".to_string());
    }

    // Load all images first to get dimensions
    let images: Vec<DynamicImage> = image_paths
        .iter()
        .map(|path| ::image::open(path).map_err(|e| format!("Failed to open {}: {}", path, e)))
        .collect::<Result<Vec<_>, _>>()?;

    // Create PDF document with first image dimensions
    let first_img = &images[0];
    let (width, height) = first_img.dimensions();
    let (doc, page1, layer1) = PdfDocument::new(
        "Images to PDF",
        Mm(width as f32 * 0.264583),
        Mm(height as f32 * 0.264583),
        "Layer 1",
    );

    // Add first image
    add_image_to_layer(
        doc.get_page(page1).get_layer(layer1),
        first_img,
        width,
        height,
    )?;

    // Add remaining images
    for img in images.iter().skip(1) {
        let (img_width, img_height) = img.dimensions();
        let (page, layer) = doc.add_page(
            Mm(img_width as f32 * 0.264583),
            Mm(img_height as f32 * 0.264583),
            "Layer 1",
        );
        add_image_to_layer(
            doc.get_page(page).get_layer(layer),
            img,
            img_width,
            img_height,
        )?;
    }

    // Save PDF
    let file = File::create(output_path).map_err(|e| format!("Failed to create file: {}", e))?;
    let mut writer = BufWriter::new(file);
    doc.save(&mut writer)
        .map_err(|e| format!("Failed to save PDF: {}", e))?;

    Ok(format!("PDF saved to {}", output_path))
}

fn add_image_to_layer(
    layer: PdfLayerReference,
    img: &DynamicImage,
    width: u32,
    height: u32,
) -> Result<(), String> {
    // Convert image to RGB8 format
    let rgb_img = img.to_rgb8();
    let raw_data = rgb_img.into_raw();

    let image_data = Image::from(ImageXObject {
        width: Px(width as usize),
        height: Px(height as usize),
        color_space: ColorSpace::Rgb,
        bits_per_component: ColorBits::Bit8,
        interpolate: true,
        image_data: raw_data,
        image_filter: None,
        smask: None,
        clipping_bbox: None,
    });

    let transform = ImageTransform {
        translate_x: Some(Mm(0.0)),
        translate_y: Some(Mm(0.0)),
        rotate: None,
        scale_x: Some(width as f32 * 0.264583),
        scale_y: Some(height as f32 * 0.264583),
        dpi: None,
    };

    image_data.add_to_layer(layer.clone(), transform);

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            get_image_preview,
            convert_images_to_pdf
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
