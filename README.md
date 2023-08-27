# Image Editor Application

![GitHub](https://img.shields.io/github/license/luckmanqasim/image-editor)

The Image Editor App is a Python-based desktop application that allows users to load, edit, and save images. It provides a user-friendly graphical interface for performing various image processing tasks, such as applying filters, adjusting colors, and enhancing image quality.
The Image Editor Application is a Python GUI program built using the Tkinter library. It allows users to load images, apply various filters and enhancements, and save their edited images. This README provides an overview of the application, how to use it, and how to contribute.

![Application Screenshot](screenshot.png?raw=true)

## Features

### 1. Image Loading

**Import Image:** Users can import images from their local storage. Supported file formats include PNG and JPG.

### 2. Image Editing

#### Filters

**Blur:** Apply a blur filter to the image.
**Contour:** Add a contour effect to the image.
**Detail:** Enhance fine details in the image.
**Edge Enhance:** Highlight edges in the image.
**Emboss:** Create an embossed appearance.
**Sharpen:** Improve image sharpness.
**Smooth:** Apply a smoothing effect.

#### Colors

**Black and White:** Convert the image to grayscale.
**Invert:** Invert the colors of the image.
**Equalize:** Adjust the color balance for optimal contrast.

#### Transformations

**Flip:** Flip the image horizontally.
**Mirror:** Create a mirror image effect.

### 3. Image Enhancement

**Box Blur:** Adjust the intensity of the box blur effect.
**Gaussian Blur:** Control the strength of the Gaussian blur.
**Color:** Modify the color saturation of the image.
**Contrast:** Enhance or reduce image contrast.
**Brightness:** Adjust image brightness.
**Sharpness:** Improve image sharpness.

### 4. Pixabay Integration

**Search:** Search for images on Pixabay using keywords.
**Import:** Import Pixabay images directly into the editor for editing.

### 5. User Interface Customization

**Appearance Mode:** Choose between Light, Dark, or System theme modes.
**UI Scaling:** Adjust the UI scaling for optimal viewing.

### 6. Undo Functionality

**Undo:** Revert to previous image states by pressing Ctrl + Z.

### 7. Image Saving

**Save Image:** Save edited images in PNG or JPG format.
**Save Image As:** Choose a new file name and location for saving images.

## Cache System

The Image Editor App includes a cache system implemented in the cache.py module. This cache system helps optimize the application's performance and manage downloaded images efficiently. Here's how it works:

**Initialization:** The cache system is initiated when the Image Editor App starts. It sets up a cache directory and a JSON file to store data.

**Storing Data:** When new data, such as downloaded images and links, needs to be cached, it's organized and added to the JSON file.

**Retrieving Data:** The cache system can retrieve data associated with a specific query (e.g., Pixabay image search) from the JSON file. This data includes image paths and links.

**Cache Expiration:** The cache system automatically removes old data from the JSON file if it's older than 24 hours. This helps maintain a clean and up-to-date cache.

**Usage in the App:** The Image Editor App uses the cache system to store and retrieve Pixabay image data, optimizing the search and import process.

## Getting Started

### Prerequisites

Before running the Image Editor Application, make sure you have the following dependencies installed:

- Python (>=3.6)
- tkinter (usually included with Python, no additional installation required)
- CustomTkinter
- PIL (Python Imaging Library)
- requests
- Pixabay API Key (for Pixabay integration)

## Installation

1. Clone the GitHub repository:

```bash
git clone https://github.com/your-username/image-editor.git
```

2. Navigate to the project directory:

```bash
cd image-editor
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root and add your Pixabay API key as follows:

```
PIXABAY_API_KEY=your_api_key_here
```

## Usage

1. Run the Image Editor App:

```bash
python app.py
```

2. Use the app to import images, apply filters, enhance images, and save your edited images.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
This application was built using [Tkinter](https://docs.python.org/3/library/tkinter.html) and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the GUI.
Pixabay integration powered by the [Pixabay API](https://pixabay.com/api/docs/).