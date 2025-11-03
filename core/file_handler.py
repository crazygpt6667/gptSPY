"""
File Handler Module for Secure File Communication Application
Handles embedding and extracting encrypted data within various file formats
"""

import os
from cryptography.fernet import Fernet
import base64
from stegano import lsb
from PIL import Image
import tempfile
import shutil


class FileHandler:
    """Handles secure embedding and extraction of data in files"""
    
    def __init__(self):
        # Generate a key for encryption (in production, this should be derived from user password)
        self.key: bytes = Fernet.generate_key()
        self.cipher_suite: Fernet = Fernet(self.key)
        
    def embed_data(self, file_path: str, data: str) -> str:
        """
        Embed encrypted data into a file
        
        Args:
            file_path (str): Path to the file to embed data into
            data (str): Data to embed
            
        Returns:
            str: Path to the output file with embedded data
        """
        # Encrypt the data
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        encoded_data = base64.b64encode(encrypted_data).decode()
        
        # Determine file type and handle accordingly
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png']:
            return self._embed_in_image(file_path, encoded_data)
        elif file_ext == '.pdf':
            return self._embed_in_pdf(file_path, encoded_data)
        elif file_ext == '.mp4':
            return self._embed_in_video(file_path, encoded_data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
            
    def extract_data(self, file_path: str) -> str:
        """
        Extract encrypted data from a file
        
        Args:
            file_path (str): Path to the file to extract data from
            
        Returns:
            str: Decrypted extracted data
        """
        # Determine file type and handle accordingly
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png']:
            encoded_data = self._extract_from_image(file_path)
        elif file_ext == '.pdf':
            encoded_data = self._extract_from_pdf(file_path)
        elif file_ext == '.mp4':
            encoded_data = self._extract_from_video(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
            
        # Decrypt the data
        try:
            encrypted_data = base64.b64decode(encoded_data.encode())
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
            
    def _embed_in_image(self, image_path: str, data: str) -> str:
        """
        Embed data in an image file using LSB steganography
        
        Args:
            image_path (str): Path to the image file
            data (str): Data to embed
            
        Returns:
            str: Path to the output image with embedded data
        """
        # For PNG files, we need to convert to RGB mode first
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Save to temporary file if needed
        temp_path = None
        if image_path.lower().endswith('.png'):
            temp_path = tempfile.mktemp(suffix='.png')
            _ = image.save(temp_path, format='PNG')
            image_path = temp_path
            
        # Hide data in image
        secret_image = lsb.hide(image_path, data)
        
        # Generate output path
        base, _ = os.path.splitext(image_path)
        output_path = f"{base}_embedded.png"
        
        # Save the image with embedded data
        _ = secret_image.save(output_path)
        
        # Clean up temporary file if used
        if temp_path and os.path.exists(temp_path):
            _ = os.remove(temp_path)
            
        return output_path
        
    def _extract_from_image(self, image_path: str) -> str:
        """
        Extract data from an image file
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Extracted data
        """
        # Reveal data from image
        hidden_data = lsb.reveal(image_path)
        if hidden_data is None:
            raise ValueError("No hidden data found in image")
        return hidden_data
        
    def _embed_in_pdf(self, pdf_path: str, data: str) -> str:
        """
        Embed data in a PDF file (placeholder implementation)
        
        Args:
            pdf_path (str): Path to the PDF file
            data (str): Data to embed
            
        Returns:
            str: Path to the output PDF with embedded data
        """
        # For now, we'll just append the data as metadata
        # In a full implementation, you would modify the PDF structure
        base, _ = os.path.splitext(pdf_path)
        output_path = f"{base}_embedded.pdf"
        
        # Copy the original file
        _ = shutil.copy2(pdf_path, output_path)
        
        # In a real implementation, you would embed the data in the PDF
        # For demonstration, we'll just save the data to a separate file
        data_file_path = f"{base}_embedded_data.txt"
        with open(data_file_path, 'w') as f:
            _ = f.write(data)
            
        return output_path
        
    def _embed_in_video(self, video_path: str, data: str) -> str:
        """
        Embed data in a video file (placeholder implementation)
        
        Args:
            video_path (str): Path to the video file
            data (str): Data to embed
            
        Returns:
            str: Path to the output video with embedded data
        """
        # For video files, steganography is more complex
        # For demonstration, we'll just copy the file and save data separately
        base, _ = os.path.splitext(video_path)
        output_path = f"{base}_embedded.mp4"
        
        # Copy the original file
        _ = shutil.copy2(video_path, output_path)
        
        # Save the data to a separate file
        data_file_path = f"{base}_embedded_data.txt"
        with open(data_file_path, 'w') as f:
            _ = f.write(data)
            
        return output_path
        
    def _extract_from_pdf(self, pdf_path: str) -> str:
        """
        Extract data from a PDF file (placeholder implementation)
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted data
        """
        # In a real implementation, you would extract the data from the PDF
        # For demonstration, we'll try to read from the separate data file
        base, _ = os.path.splitext(pdf_path)
        data_file_path = f"{base}_embedded_data.txt"
        
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r') as f:
                return f.read()
        else:
            raise ValueError("No embedded data found in PDF")
            
    def _extract_from_video(self, video_path: str) -> str:
        """
        Extract data from a video file (placeholder implementation)
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            str: Extracted data
        """
        # For demonstration, we'll try to read from the separate data file
        base, _ = os.path.splitext(video_path)
        data_file_path = f"{base}_embedded_data.txt"
        
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r') as f:
                return f.read()
        else:
            raise ValueError("No embedded data found in video")