import requests
from typing import List, Union, Optional, Dict
from pathlib import Path
import io

class PixyImagery:
    """
    Python client for Pixy Imagery service.
    
    Provides methods for uploading, retrieving, and managing images.
    """
    
    def __init__(self, 
                 base_url: str = 'http://localhost:5100', 
                 api_key: Optional[str] = None):
        """
        Initialize Pixy Imagery client.
        
        :param base_url: Base URL of the Pixy Imagery service
        :param api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
    
    def _construct_url(self, endpoint: str) -> str:
        """
        Construct full URL with optional API key.
        
        :param endpoint: API endpoint path
        :return: Full URL with optional API key
        """
        url = f"{self.base_url}{endpoint}"
        
        # Add API key if required
        if self.api_key is not None:
            url += f"?api_key={self.api_key}"
        
        return url
    
    def upload_images(self, 
                      images: Union[str, Path, List[Union[str, Path]], List[io.IOBase]]) -> Dict:
        """
        Upload one or more images to the Pixy Imagery service.
        
        :param images: Single image or list of images (file paths or file-like objects)
        :return: Dictionary containing uploaded image details
        """
        # Normalize input to list
        if not isinstance(images, list):
            images = [images]
        
        # Prepare multipart form data
        files = []
        for image in images:
            # Handle file paths
            if isinstance(image, (str, Path)):
                files.append(('images', open(image, 'rb')))
            # Handle file-like objects
            elif hasattr(image, 'read'):
                files.append(('images', image))
            else:
                raise ValueError(f"Unsupported image type: {type(image)}")
        
        # Construct URL
        url = self._construct_url('/upload-image')
        
        # Send request
        response = requests.post(url, files=files)
        
        # Close file handles
        for _, file in files:
            if hasattr(file, 'close'):
                file.close()
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.json()
    
    def get_image(self, 
                  image_id: str, 
                  width: Optional[int] = None, 
                  height: Optional[int] = None, 
                  maintain_aspect_ratio: bool = False) -> bytes:
        """
        Retrieve an image by its ID with optional resizing.
        
        :param image_id: Unique identifier of the image
        :param width: Optional desired width
        :param height: Optional desired height
        :param maintain_aspect_ratio: Maintain image aspect ratio
        :return: Image as bytes
        """
        # Construct URL with optional parameters
        url = self._construct_url(f"/{image_id}")
        
        # Add query parameters
        params = {}
        if width is not None:
            params['w'] = width
        if height is not None:
            params['h'] = height
        if maintain_aspect_ratio:
            params['maintain_aspect_ratio'] = True
        
        # Send request
        response = requests.get(url, params=params)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.content
    
    def get_random_image(self, 
                          width: Optional[int] = None, 
                          height: Optional[int] = None, 
                          maintain_aspect_ratio: bool = False) -> bytes:
        """
        Retrieve a random image with optional resizing.
        
        :param width: Optional desired width
        :param height: Optional desired height
        :param maintain_aspect_ratio: Maintain image aspect ratio
        :return: Image as bytes
        """
        # Construct URL with optional parameters
        url = self._construct_url("/random")
        
        # Add query parameters
        params = {}
        if width is not None:
            params['w'] = width
        if height is not None:
            params['h'] = height
        if maintain_aspect_ratio:
            params['maintain_aspect_ratio'] = True
        
        # Send request
        response = requests.get(url, params=params)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        return response.content

# Optional: allow direct import of class
__all__ = ['PixyImagery']