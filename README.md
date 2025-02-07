# File Renamer with Image Overlay

A Python desktop application that allows you to batch rename files and automatically add text overlays to images. Built with Tkinter and Pillow, this tool provides a user-friendly interface for managing file names while preserving the original files.

## Features

- **Batch File Renaming**: Rename multiple files at once while preserving file extensions
- **Image Overlay**: Automatically adds text overlays to images with the new filename
- **Live Preview**: See how your renamed files will look before applying changes
- **Thumbnail Preview**: Visual preview of image files with overlay
- **File Count Matching**: Visual indicator ensures the number of new names matches the number of files
- **Safe Operation**: Creates copies of files instead of modifying originals
- **Organized Output**: Saves renamed files in timestamped directories
- **Support for Multiple File Types**: Works with both image and non-image files

## Requirements

- Python 3.6 or higher
- PIL (Pillow) library
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shainafees/file_renamer_thumbnail.git
cd file-renamer
```

2. Install required packages:
```bash
pip install Pillow
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Using the application:
   - Click "Browse" to select a folder containing files to rename
   - Enter new names in the text area (one name per line)
   - Use "Preview Changes" to see the proposed renaming
   - Click "Rename Files" to process the files
   - Renamed files will be saved in your Downloads folder under "Renamed Files"

## Image Overlay Features

- Semi-transparent background for text visibility
- Automatic font size scaling based on image dimensions
- Bottom-right corner positioning
- High-quality image preservation
- Supports common image formats (PNG, JPG, JPEG, GIF, BMP)

## Directory Structure

Renamed files are organized as follows:
```
Downloads/
└── Renamed Files/
    └── renamed_YYYYMMDD_HHMMSS/
        ├── renamed_file1.jpg
        ├── renamed_file2.png
        └── ...
```

## Interface Components

- **Folder Selection**: Choose the source folder containing files to rename
- **File Counts**: Display of file counts and matching status
- **New File Names**: Text area for entering new names
- **Preview**: Shows old name → new name mapping
- **Thumbnail Preview**: Displays current image with overlay
- **Action Buttons**: Preview Changes, Rename Files, and Clear All

## Customization

The application provides several customizable features:
- Font size for overlays (default: 5% of image size)
- Text position (default: bottom-right)
- Text color (default: white)
- Background opacity (default: 50%)
- JPEG quality (default: 95%)

## Error Handling

- Validates file count matches name count
- Checks for existing files before renaming
- Preserves original files
- Handles invalid image files gracefully
- Provides clear error messages

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI
