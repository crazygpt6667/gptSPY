"""Main Window for Secure File Communication Application"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextEdit, QFileDialog, QLabel,
    QTabWidget, QGroupBox, QComboBox,
    QMessageBox
)
from PyQt6.QtCore import pyqtSlot
from core.file_handler import FileHandler
from core.listener import ConnectionListener
from gui.auth_dialog import AuthDialog
import os
from typing import TYPE_CHECKING, Callable, TypeVar, cast

if TYPE_CHECKING:
    pass

# Define type variable for decorator with more specific bound
F = TypeVar('F', bound=Callable[..., object])

# Properly typed decorator for pyqtSlot with specific types instead of Any
def typed_pyqtSlot(*args: object, **kwargs: object) -> Callable[[F], F]:
    """Typed version of pyqtSlot decorator"""
    return cast(Callable[[F], F], pyqtSlot(*args, **kwargs))

class MainWindow(QMainWindow):  # type: ignore
    """Main application window with tabs for different functionalities"""
    
    def __init__(self):
        super().__init__()
        self.file_handler: FileHandler = FileHandler()
        self.listener: ConnectionListener = ConnectionListener()
        self.tabs: QTabWidget = QTabWidget()  # Explicitly type the tabs attribute
        
        # Type annotations for attributes initialized outside __init__
        self.embed_file_label: QLabel
        self.embed_file_button: QPushButton
        self.data_input: QTextEdit
        self.embed_button: QPushButton
        self.extract_file_label: QLabel
        self.extract_file_button: QPushButton
        self.extract_button: QPushButton
        self.data_output: QTextEdit
        self.listener_toggle: QPushButton
        self.listener_status: QLabel
        self.connection_log: QTextEdit
        self.auth_button: QPushButton
        self.encryption_combo: QComboBox
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("SecureConnect - Secure File Communication")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_embed_tab()
        self.create_extract_tab()
        self.create_listener_tab()
        self.create_settings_tab()
        
        # Apply dark theme
        self.apply_dark_theme()
        
    def create_embed_tab(self):
        """Create the embed data tab"""
        embed_tab: QWidget = QWidget()
        layout = QVBoxLayout(embed_tab)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QHBoxLayout(file_group)
        
        self.embed_file_label = QLabel("No file selected")
        self.embed_file_button = QPushButton("Select File")
        _ = self.embed_file_button.clicked.connect(self.select_embed_file)
        
        file_layout.addWidget(self.embed_file_label)
        file_layout.addWidget(self.embed_file_button)
        
        # Data input group
        data_group = QGroupBox("Connection Request Data")
        data_layout = QVBoxLayout(data_group)
        
        self.data_input = QTextEdit()
        self.data_input.setPlaceholderText("Enter connection request data to embed...")
        data_layout.addWidget(self.data_input)
        
        # Embed button
        self.embed_button = QPushButton("Embed Data")
        _ = self.embed_button.clicked.connect(self.embed_data)
        
        # Add to layout
        layout.addWidget(file_group)
        layout.addWidget(data_group)
        layout.addWidget(self.embed_button)
        layout.addStretch()
        
        self.tabs.addTab(embed_tab, "Embed Data")
        
    def create_extract_tab(self):
        """Create the extract data tab"""
        extract_tab: QWidget = QWidget()
        layout = QVBoxLayout(extract_tab)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QHBoxLayout(file_group)
        
        self.extract_file_label = QLabel("No file selected")
        self.extract_file_button = QPushButton("Select File")
        _ = self.extract_file_button.clicked.connect(self.select_extract_file)
        
        file_layout.addWidget(self.extract_file_label)
        file_layout.addWidget(self.extract_file_button)
        
        # Extract button
        self.extract_button = QPushButton("Extract Data")
        _ = self.extract_button.clicked.connect(self.extract_data)
        
        # Data output
        self.data_output = QTextEdit()
        self.data_output.setPlaceholderText("Extracted data will appear here...")
        self.data_output.setReadOnly(True)
        
        # Add to layout
        layout.addWidget(file_group)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.data_output)
        layout.addStretch()
        
        self.tabs.addTab(extract_tab, "Extract Data")
        
    def create_listener_tab(self):
        """Create the listener tab"""
        listener_tab: QWidget = QWidget()
        layout = QVBoxLayout(listener_tab)
        
        # Listener controls
        controls_layout = QHBoxLayout()
        
        self.listener_toggle = QPushButton("Start Listener")
        self.listener_toggle.setCheckable(True)
        _ = self.listener_toggle.clicked.connect(self.toggle_listener)
        
        status_label = QLabel("Listener Status:")
        self.listener_status = QLabel("Stopped")
        
        controls_layout.addWidget(self.listener_toggle)
        controls_layout.addWidget(status_label)
        controls_layout.addWidget(self.listener_status)
        controls_layout.addStretch()
        
        # Connection log
        self.connection_log = QTextEdit()
        self.connection_log.setPlaceholderText("Connection requests will appear here...")
        self.connection_log.setReadOnly(True)
        
        # Add to layout
        layout.addLayout(controls_layout)
        layout.addWidget(QLabel("Connection Requests:"))
        layout.addWidget(self.connection_log)
        layout.addStretch()
        
        self.tabs.addTab(listener_tab, "Listener")
        
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_tab: QWidget = QWidget()
        layout = QVBoxLayout(settings_tab)
        
        # Authentication group
        auth_group = QGroupBox("Authentication")
        auth_layout = QVBoxLayout(auth_group)
        
        self.auth_button = QPushButton("Manage Authentication")
        _ = self.auth_button.clicked.connect(self.open_auth_dialog)
        auth_layout.addWidget(self.auth_button)
        
        # Encryption settings
        encryption_group = QGroupBox("Encryption")
        encryption_layout = QVBoxLayout(encryption_group)
        
        encryption_layout.addWidget(QLabel("Encryption Algorithm:"))
        self.encryption_combo = QComboBox()
        self.encryption_combo.addItems(["AES-256-GCM", "ChaCha20-Poly1305"])
        encryption_layout.addWidget(self.encryption_combo)
        
        # Add to layout
        layout.addWidget(auth_group)
        layout.addWidget(encryption_group)
        layout.addStretch()
        
        self.tabs.addTab(settings_tab, "Settings")
        
    def apply_dark_theme(self):
        """Apply a dark theme to the application"""
        dark_stylesheet = """
        QMainWindow, QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #3c3f41;
            border: 1px solid #555555;
            padding: 5px;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #4c4f51;
        }
        QPushButton:pressed {
            background-color: #2c2f31;
        }
        QTextEdit {
            background-color: #3c3f41;
            border: 1px solid #555555;
            color: #ffffff;
        }
        QGroupBox {
            border: 1px solid #555555;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
        }
        QTabWidget::pane {
            border: 1px solid #555555;
        }
        QTabBar::tab {
            background: #3c3f41;
            border: 1px solid #555555;
            padding: 5px;
        }
        QTabBar::tab:selected {
            background: #4c4f51;
        }
        """
        self.setStyleSheet(dark_stylesheet)
        
    def setup_connections(self):
        """Set up signal-slot connections"""
        _ = self.listener.connection_received.connect(self.on_connection_received)
        
    @typed_pyqtSlot(str)
    def on_connection_received(self, data: str):
        """Handle received connection data"""
        self.connection_log.append(f"{data}\n")
        
    def select_embed_file(self):
        """Open file dialog to select file for embedding"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File for Embedding", "",
            "Image Files (*.jpg *.jpeg *.png);;PDF Files (*.pdf);;Video Files (*.mp4);;All Files (*)"
        )
        
        if file_path:
            self.embed_file_label.setText(os.path.basename(file_path))
            self.embed_file_path: str = file_path
            
    def select_extract_file(self):
        """Open file dialog to select file for extraction"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File for Extraction", "",
            "Image Files (*.jpg *.jpeg *.png);;PDF Files (*.pdf);;Video Files (*.mp4);;All Files (*)"
        )
        
        if file_path:
            self.extract_file_label.setText(os.path.basename(file_path))
            self.extract_file_path: str = file_path
            
    def embed_data(self):
        """Embed data into selected file"""
        if not hasattr(self, 'embed_file_path'):
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")
            return
            
        data = self.data_input.toPlainText()
        if not data:
            QMessageBox.warning(self, "No Data", "Please enter data to embed.")
            return
            
        try:
            output_path = self.file_handler.embed_data(self.embed_file_path, data)
            QMessageBox.information(
                self, "Success", 
                f"Data embedded successfully!\nOutput file: {output_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to embed data: {str(e)}")
            
    def extract_data(self):
        """Extract data from selected file"""
        if not hasattr(self, 'extract_file_path'):
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")
            return
            
        try:
            extracted_data = self.file_handler.extract_data(self.extract_file_path)
            self.data_output.setPlainText(extracted_data)
            QMessageBox.information(self, "Success", "Data extracted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract data: {str(e)}")
            
    def toggle_listener(self):
        """Toggle the connection listener"""
        if self.listener_toggle.isChecked():
            try:
                self.listener.start()
                self.listener_toggle.setText("Stop Listener")
                self.listener_status.setText("Running")
            except Exception as e:
                self.listener_toggle.setChecked(False)
                QMessageBox.critical(self, "Error", f"Failed to start listener: {str(e)}")
        else:
            self.listener.stop()
            self.listener_toggle.setText("Start Listener")
            self.listener_status.setText("Stopped")
            
    def open_auth_dialog(self) -> None:
        """Open authentication management dialog"""
        dialog = AuthDialog(self)
        _ = dialog.authenticated.connect(self.on_authenticated)
        dialog.exec()
        
    def on_authenticated(self, user: str):
        """Handle successful authentication"""
        QMessageBox.information(self, "Authentication", f"Successfully authenticated as {user}")