# Image Watermarking Application

## Overview

This Python application provides a user-friendly GUI for adding watermarks to images. It allows users to easily apply customizable watermarks to multiple images(BULK) at once.

## Features

- Select input and output directories for batch processing
- Choose a custom watermark image (PNG with transparency)
- Adjust watermark opacity (0-100%)
- Resize watermark (1-100% of image size)
- Position watermark anywhere on the image
- Option to tile watermark across entire image
- Real-time preview of watermarked image
- Batch process all images in selected directory

## Requirements

- Python 3.6+
- Pillow (PIL Fork)
- tkinter (usually comes with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/image-watermarking-app.git
```
2. Navigate to the project directory:
```bash
cd image-watermarking-app
```
3. Install required packages:

```bash
pip install Pillow
```

## Usage

1. Run the script:

```bash
python watermark_app.py

```
2. Use the GUI to:
- Select input directory containing images to watermark
- Choose output directory for watermarked images
- Select watermark image (PNG format recommended)
- Adjust watermark settings (opacity, size, position)
- Toggle "Tile Watermark" for repeated pattern
- View real-time preview of changes
- Click "Process Images" to apply watermark to all images

  
![image](https://github.com/user-attachments/assets/236d4dcb-858f-439b-804d-a0340627a12b)


### Example OUTPUT Image : 
![image](https://github.com/user-attachments/assets/3872f0fd-70e3-4c1d-b408-af76fc0974c5)



## Notes

- Supported image formats: PNG, JPG, JPEG
- Watermark should be a PNG image with transparency for best results
- Processed images are saved in JPEG format
- Original images are not modified; watermarked versions are saved separately

## Contributing

Contributions, issues, and feature requests are welcome.

### TODO:
Creating web version of this application. (FLASK is more desireable) 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
