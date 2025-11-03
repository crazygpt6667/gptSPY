"""Authentication Dialog for Secure File Communication Application"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTabWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
# Optional import no longer needed with Python 3.10+ union syntax
# Added import for proper type annotation of signals
from PyQt6.QtCore import pyqtBoundSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class AuthDialog(QDialog):  # type: ignore
    """Dialog for managing authentication"""
    
    # Added explicit type annotation for the signal
    authenticated: pyqtBoundSignal = pyqtSignal(str)  # Signal emitted when user authenticates
    
    # Added type annotations for all instance attributes
    email_input: QLineEdit
    password_input: QLineEdit
    phone_input: QLineEdit
    tabs: QTabWidget
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.tabs = QTabWidget()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Authentication")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Create tab widget for different auth methods
        layout.addWidget(self.tabs)
        
        # Manual signup tab
        tabs_widget: QTabWidget = self.tabs
        self.create_manual_tab(tabs_widget)
        
        # OAuth tabs
        self.create_oauth_tab(tabs_widget, "GitHub", "github")
        self.create_oauth_tab(tabs_widget, "Google", "google")
        self.create_oauth_tab(tabs_widget, "Microsoft", "microsoft")
        
        # Close button
        close_button = QPushButton("Close")
        _ = close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
    def create_manual_tab(self, parent: QTabWidget) -> None:
        """Create manual signup/login tab"""
        tab: QWidget = QWidget()
        layout = QVBoxLayout(tab)
        
        # Email input
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        layout.addWidget(self.email_input)
        
        # Password input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Phone number input
        layout.addWidget(QLabel("Phone Number (optional):"))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        layout.addWidget(self.phone_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        signup_button = QPushButton("Sign Up")
        _ = signup_button.clicked.connect(self.manual_signup)
        button_layout.addWidget(signup_button)
        
        login_button = QPushButton("Log In")
        _ = login_button.clicked.connect(self.manual_login)
        button_layout.addWidget(login_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        parent.addTab(tab, "Manual Signup")
        
    def create_oauth_tab(self, parent: QTabWidget, name: str, provider: str) -> None:
        """Create OAuth tab for a provider"""
        tab: QWidget = QWidget()
        layout = QVBoxLayout(tab)
        
        layout.addWidget(QLabel(f"Authenticate with {name}"))
        
        # OAuth button
        oauth_button = QPushButton(f"Connect with {name}")
        _ = oauth_button.clicked.connect(lambda: self.oauth_login(provider))
        layout.addWidget(oauth_button)
        layout.addStretch()
        
        parent.addTab(tab, name)
        
    def manual_signup(self):
        """Handle manual signup"""
        email = self.email_input.text()
        password = self.password_input.text()
        phone = self.phone_input.text()
        
        # Basic validation
        if not email or not password:
            QMessageBox.warning(self, "Validation Error", "Email and password are required.")
            return
            
        # Include phone number in the success message if provided
        phone_message = f" and phone number {phone}" if phone else ""
        QMessageBox.information(
            self, "Signup Success", 
            f"Account created for {email}{phone_message}. Please check your email for verification."
        )
        _ = self.authenticated.emit(email)
        self.accept()
        
    def manual_login(self):
        """Handle manual login"""
        email = self.email_input.text()
        password = self.password_input.text()
        
        # Basic validation
        if not email or not password:
            QMessageBox.warning(self, "Validation Error", "Email and password are required.")
            return
            
        # Here you would normally implement actual login logic
        # For now, we'll just simulate success
        QMessageBox.information(self, "Login Success", f"Welcome back, {email}!")
        _ = self.authenticated.emit(email)
        self.accept()
        
    def oauth_login(self, provider: str):
        """Handle OAuth login"""
        # Here you would normally implement OAuth flow
        # For now, we'll just simulate success
        QMessageBox.information(
            self, "OAuth Success", 
            f"Successfully authenticated with {provider.capitalize()}!"
        )
        _ = self.authenticated.emit(f"{provider}_user")
        self.accept()