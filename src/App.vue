<script setup>
import { ref, computed, onMounted } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";

// Language detection and translations
const systemLanguage = navigator.language || navigator.userLanguage || "en";
const isChineseLanguage = systemLanguage.toLowerCase().startsWith("zh");

const lang = computed(() => {
  if (isChineseLanguage) {
    return {
      selectAppend: "选择/追加图片",
      deleteImage: "删除图片",
      moveUp: "上移",
      moveDown: "下移",
      convertPdf: "转换为PDF",
      statusSelected: "已选择图片: ",
      warningSelectImage: "请先选择图片！",
      warningDeleteImage: "请先选择要删除的图片！",
      successPdfSaved: "PDF 已保存到",
      titleSavePdf: "保存 PDF 文件",
      titleApp: "图片转PDF",
      orderColumn: "顺序",
      pathColumn: "图片路径",
      preview: "预览",
      noImageSelected: "选择图片后在此预览",
      converting: "正在转换...",
      selectImages: '点击"选择/追加图片"开始',
    };
  }
  return {
    selectAppend: "Select/Append Images",
    deleteImage: "Delete Image",
    moveUp: "Move Up",
    moveDown: "Move Down",
    convertPdf: "Convert to PDF",
    statusSelected: "Selected Images: ",
    warningSelectImage: "Please select images first!",
    warningDeleteImage: "Please select an image to delete!",
    successPdfSaved: "PDF saved to",
    titleSavePdf: "Save PDF File",
    titleApp: "Images to PDF",
    orderColumn: "Order",
    pathColumn: "Image Path",
    preview: "Preview",
    noImageSelected: "Select an image to preview",
    converting: "Converting...",
    selectImages: 'Click "Select/Append Images" to start',
  };
});

// State
const images = ref([]);
const selectedIndex = ref(-1);
const previewImage = ref(null);
const isConverting = ref(false);
const statusMessage = ref("");

// Functions
async function selectOrAppendImages() {
  try {
    const selected = await open({
      multiple: true,
      filters: [
        {
          name: "Images",
          extensions: ["png", "jpg", "jpeg", "bmp", "gif", "webp"],
        },
      ],
    });

    if (selected) {
      const paths = Array.isArray(selected) ? selected : [selected];
      for (const path of paths) {
        const imageInfo = await invoke("get_image_preview", {
          path: path,
          maxWidth: 400,
          maxHeight: 400,
        });
        images.value.push(imageInfo);
      }
      // Show first image preview if list was empty
      if (images.value.length === paths.length && paths.length > 0) {
        selectImage(0);
      }
    }
  } catch (error) {
    console.error("Error selecting images:", error);
    statusMessage.value = `Error: ${error}`;
  }
}

function selectImage(index) {
  selectedIndex.value = index;
  if (index >= 0 && index < images.value.length) {
    previewImage.value = images.value[index].preview;
  }
}

function deleteImage() {
  if (selectedIndex.value >= 0 && selectedIndex.value < images.value.length) {
    images.value.splice(selectedIndex.value, 1);
    if (images.value.length === 0) {
      selectedIndex.value = -1;
      previewImage.value = null;
    } else if (selectedIndex.value >= images.value.length) {
      selectImage(images.value.length - 1);
    } else {
      selectImage(selectedIndex.value);
    }
  } else {
    alert(lang.value.warningDeleteImage);
  }
}

function moveUp() {
  if (selectedIndex.value > 0) {
    const index = selectedIndex.value;
    const temp = images.value[index];
    images.value[index] = images.value[index - 1];
    images.value[index - 1] = temp;
    selectedIndex.value = index - 1;
  }
}

function moveDown() {
  if (
    selectedIndex.value >= 0 &&
    selectedIndex.value < images.value.length - 1
  ) {
    const index = selectedIndex.value;
    const temp = images.value[index];
    images.value[index] = images.value[index + 1];
    images.value[index + 1] = temp;
    selectedIndex.value = index + 1;
  }
}

async function convertToPdf() {
  if (images.value.length === 0) {
    alert(lang.value.warningSelectImage);
    return;
  }

  try {
    const savePath = await save({
      filters: [
        {
          name: "PDF",
          extensions: ["pdf"],
        },
      ],
      defaultPath: "output.pdf",
    });

    if (savePath) {
      isConverting.value = true;
      statusMessage.value = lang.value.converting;

      const imagePaths = images.value.map((img) => img.path);
      await invoke("convert_images_to_pdf", {
        imagePaths: imagePaths,
        outputPath: savePath,
      });

      statusMessage.value = `${lang.value.successPdfSaved}: ${savePath}`;
      alert(`${lang.value.successPdfSaved}\n${savePath}`);
    }
  } catch (error) {
    console.error("Error converting to PDF:", error);
    statusMessage.value = `Error: ${error}`;
    alert(`Error: ${error}`);
  } finally {
    isConverting.value = false;
  }
}

function truncatePath(path, maxLength = 50) {
  if (path.length <= maxLength) return path;
  return "..." + path.slice(-maxLength);
}

function handleContextMenu(event, index) {
  event.preventDefault();
  selectImage(index);
  // Simple context menu via confirm dialog
  if (confirm(lang.value.deleteImage + "?")) {
    deleteImage();
  }
}
</script>

<template>
  <div class="app-container">
    <!-- Header buttons -->
    <div class="button-row">
      <button @click="selectOrAppendImages" class="primary-btn">
        {{ lang.selectAppend }}
      </button>
      <button @click="deleteImage" class="secondary-btn">
        {{ lang.deleteImage }}
      </button>
    </div>

    <!-- Main content area -->
    <div class="main-content">
      <!-- Image list -->
      <div class="image-list-container">
        <div class="list-header">
          <span class="order-col">{{ lang.orderColumn }}</span>
          <span class="path-col">{{ lang.pathColumn }}</span>
        </div>
        <div class="image-list" v-if="images.length > 0">
          <div
            v-for="(image, index) in images"
            :key="index"
            class="image-item"
            :class="{ selected: selectedIndex === index }"
            @click="selectImage(index)"
            @contextmenu="handleContextMenu($event, index)"
          >
            <span class="order-col">{{ index + 1 }}</span>
            <span class="path-col" :title="image.path">{{
              truncatePath(image.name)
            }}</span>
          </div>
        </div>
        <div class="empty-list" v-else>
          <p>{{ lang.selectImages }}</p>
        </div>
      </div>

      <!-- Move buttons -->
      <div class="move-buttons">
        <button @click="moveUp" :disabled="selectedIndex <= 0">
          {{ lang.moveUp }}
        </button>
        <button
          @click="moveDown"
          :disabled="selectedIndex < 0 || selectedIndex >= images.length - 1"
        >
          {{ lang.moveDown }}
        </button>
      </div>

      <!-- Preview panel -->
      <div class="preview-container">
        <div class="preview-header">{{ lang.preview }}</div>
        <div class="preview-area">
          <img
            v-if="previewImage"
            :src="previewImage"
            alt="Preview"
            class="preview-image"
          />
          <p v-else class="no-preview">{{ lang.noImageSelected }}</p>
        </div>
      </div>
    </div>

    <!-- Convert button -->
    <button
      @click="convertToPdf"
      class="convert-btn"
      :disabled="isConverting || images.length === 0"
    >
      {{ isConverting ? lang.converting : lang.convertPdf }}
    </button>

    <!-- Status bar -->
    <div class="status-bar">
      {{
        statusMessage || lang.statusSelected + images.length
      }}
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f5f5f5;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 10px;
  gap: 10px;
}

.button-row {
  display: flex;
  gap: 10px;
}

.button-row button {
  flex: 1;
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-btn {
  background-color: #4caf50;
  color: white;
}

.primary-btn:hover {
  background-color: #45a049;
}

.secondary-btn {
  background-color: #f44336;
  color: white;
}

.secondary-btn:hover {
  background-color: #da190b;
}

.main-content {
  display: flex;
  flex: 1;
  gap: 10px;
  min-height: 0;
  border: 2px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  background-color: white;
}

.image-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 300px;
}

.list-header {
  display: flex;
  padding: 8px;
  background-color: #e0e0e0;
  font-weight: bold;
  border-bottom: 1px solid #ccc;
}

.image-list {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ddd;
}

.empty-list {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  color: #999;
}

.image-item {
  display: flex;
  padding: 8px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.1s;
}

.image-item:hover {
  background-color: #f0f0f0;
}

.image-item.selected {
  background-color: #e3f2fd;
}

.order-col {
  width: 50px;
  text-align: center;
  flex-shrink: 0;
}

.path-col {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.move-buttons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 0 10px;
}

.move-buttons button {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
  transition: background-color 0.2s;
}

.move-buttons button:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.move-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.preview-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 300px;
}

.preview-header {
  padding: 8px;
  background-color: #e0e0e0;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #ccc;
}

.preview-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #808080;
  border: 1px solid #ddd;
  overflow: hidden;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.no-preview {
  color: #ccc;
  font-style: italic;
}

.convert-btn {
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  background-color: #2196f3;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.convert-btn:hover:not(:disabled) {
  background-color: #1976d2;
}

.convert-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.status-bar {
  padding: 8px;
  background-color: #e0e0e0;
  border: 1px solid #ccc;
  font-size: 12px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    color: #f0f0f0;
    background-color: #2d2d2d;
  }

  .main-content {
    background-color: #3d3d3d;
    border-color: #555;
  }

  .list-header,
  .preview-header,
  .status-bar {
    background-color: #4d4d4d;
    border-color: #555;
  }

  .image-list,
  .empty-list {
    border-color: #555;
  }

  .image-item {
    border-color: #555;
  }

  .image-item:hover {
    background-color: #4d4d4d;
  }

  .image-item.selected {
    background-color: #1a3a5c;
  }

  .move-buttons button {
    background-color: #4d4d4d;
    border-color: #555;
    color: #f0f0f0;
  }

  .move-buttons button:hover:not(:disabled) {
    background-color: #5d5d5d;
  }

  .preview-area {
    background-color: #2d2d2d;
    border-color: #555;
  }
}
</style>
