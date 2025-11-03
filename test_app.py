"""
Test script for SecureConnect application"""

import os
import tempfile
from core.file_handler import FileHandler


def test_file_handler():
    """Test the file handler functionality"""
    print("Testing FileHandler...")
    
    # Create a temporary text file for testing
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        _ = tmp.write(b"This is a test image file")
        test_file_path = tmp.name
    
    output_path = None
    
    try:
        # Create file handler
        handler = FileHandler()
        
        # Test data to embed
        test_data = "This is a secret connection request!"
        
        # Test embedding data
        print("Embedding data...")
        output_path = handler.embed_data(test_file_path, test_data)
        print(f"Data embedded in: {output_path}")
        
        # Test extracting data
        print("Extracting data...")
        extracted_data = handler.extract_data(output_path)
        print(f"Extracted data: {extracted_data}")
        
        # Verify the data matches
        if extracted_data == test_data:
            print("SUCCESS: Data matches!")
        else:
            print("ERROR: Data does not match!")
            
    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:
        # Clean up temporary files
        try:
            _ = os.unlink(test_file_path)
            if output_path and os.path.exists(output_path):
                _ = os.unlink(output_path)
                # Also clean up the embedded data file that was created
                base, _ = os.path.splitext(output_path)
                data_file = f"{base}_embedded_data.txt"
                if os.path.exists(data_file):
                    _ = os.unlink(data_file)
        except Exception as e:
            print(f"Cleanup error: {e}")


if __name__ == "__main__":
    test_file_handler()