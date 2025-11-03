# SecureConnect Usage Guide

## Installation

### Windows

1. Double-click `install_and_run.bat` to automatically install dependencies and start the application.

OR

1. Open Command Prompt or PowerShell
2. Navigate to the application directory
3. Run: `pip install -r requirements.txt`
4. Run: `python main.py`

### Linux/macOS

1. Open Terminal
2. Navigate to the application directory
3. Make the script executable: `chmod +x install_and_run.sh`
4. Run: `./install_and_run.sh`

OR

1. Open Terminal
2. Navigate to the application directory
3. Run: `pip3 install -r requirements.txt`
4. Run: `python3 main.py`

## Application Features

### 1. Embed Data Tab

This tab allows you to embed encrypted connection requests within files:

1. Click "Select File" to choose a file (JPG, PNG, PDF, or MP4)
2. Enter your connection request data in the text box
3. Click "Embed Data" to embed the encrypted data into the file
4. The application will create a new file with "\_embedded" appended to the name

### 2. Extract Data Tab

This tab allows you to extract connection requests from files:

1. Click "Select File" to choose a file with embedded data
2. Click "Extract Data" to retrieve the connection request
3. The extracted data will appear in the text box

### 3. Listener Tab

This tab monitors for incoming connection requests:

1. Click "Start Listener" to begin monitoring
2. Incoming connection requests will appear in the log
3. Click "Stop Listener" to stop monitoring

### 4. Settings Tab

This tab manages authentication and encryption settings:

1. Click "Manage Authentication" to set up your account
2. Choose your preferred encryption algorithm

## Security Features

- All embedded data is encrypted using industry-standard Fernet encryption
- Steganography techniques hide data within files without visibly altering them
- Multiple authentication options (manual signup, GitHub, Google, Microsoft)
- Support for email and phone verification

## Supported File Types

- Images: JPG, JPEG, PNG
- Documents: PDF
- Videos: MP4

## Troubleshooting

### ImportError: No module named ...

If you see this error, it means the required dependencies are not installed:

1. Make sure you've run `pip install -r requirements.txt`
2. If you're using a virtual environment, make sure it's activated

### Failed to embed/extract data

If you encounter issues with embedding or extracting data:

1. Make sure the file format is supported
2. Check that the file is not corrupted
3. Ensure you have read/write permissions for the file

## Legal and Ethical Compliance

This application is designed for legitimate security and privacy purposes. Users are responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.

Always obtain proper authorization before embedding data in files that you do not own or have explicit permission to modify.
