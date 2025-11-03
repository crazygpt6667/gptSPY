#!/usr/bin/env python3
"""
Cross-Platform Secure File Communication Application
Main Application Entry Point
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('secureconnect.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("SecureConnect")
        app.setApplicationVersion("1.0.0")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Log application start
        logger.info("SecureConnect application started")
        
        # Execute application
        exit_code = app.exec()
        
        # Log application exit
        logger.info("SecureConnect application exited")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        if 'app' in locals():
            QMessageBox.critical(None, "Error", f"Failed to start application: {e}")
        else:
            print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()