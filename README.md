# gptSPY

A cross-platform application for secure file handling and communications with steganography capabilities.

## Features

- Cross-platform compatibility (Windows, Linux, macOS)
- Modern dark-themed GUI with PyQt6
- Embed and extract encrypted connection requests within various file types (JPG, PNG, PDF, MP4)
- Listener functionality for monitoring incoming connection requests
- Authentication support (GitHub, Google, Microsoft, manual signup)
- Email and phone verification

## Requirements

- Python 3.8 or higher
- Dependencies listed in [requirements.txt](requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```
python main.py
```

## Project Structure

```
secure-connect/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── gui/                 # GUI components
│   ├── __init__.py
│   ├── main_window.py   # Main application window
│   └── auth_dialog.py   # Authentication dialog
├── core/                # Core functionality
│   ├── __init__.py
│   ├── file_handler.py  # File embedding/extraction
│   └── listener.py      # Connection listener
└── utils/               # Utility functions
    ├── __init__.py
    └── crypto_utils.py  # Cryptographic utilities
```

## Security Considerations

This application implements several security measures:

1. Data encryption using the Fernet symmetric encryption scheme
2. Steganographic techniques for concealing data within files
3. Authentication mechanisms with multiple providers
4. Secure key management (in production implementations)

## Legal and Ethical Compliance

This application is designed for legitimate security and privacy purposes. Users are responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.