import requests
from typing import List, Optional, Dict


class PixyImagery:
    def __init__(
        self, base_url: str = "http://localhost:5100", api_key: Optional[str] = None
    ):
        """
        Create a new PixyImagery client

        :param base_url: Base URL of the Pixy Imagery service
        :param api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key

    def _construct_url(self, endpoint: str) -> str:
        """
        Construct URL with API key if required

        :param endpoint: Endpoint path
        :return: Full URL with optional API key
        """
        url = f"{self.base_url}{endpoint}"
        if self.api_key:
            url += f"?api_key={self.api_key}"
        return url

    def upload_images(self, images: List) -> Dict[str, List[Dict[str, str]]]:
        """
        Upload one or more images

        :param images: List of images to upload
        :return: Upload result containing image ids and URLs
        """
        url = self._construct_url("/upload-image")
        files = [("images", image) for image in images]

        response = requests.post(url, files=files)

        if response.status_code != 200:
            error_data = response.json()
            raise Exception(error_data.get("error", "Image upload failed"))

        return response.json()

    def get_image_url(
        self,
        image_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect_ratio: bool = False,
    ) -> str:
        """
        Get image URL by its ID

        :param image_id: ID of the image
        :param width: Desired width
        :param height: Desired height
        :param maintain_aspect_ratio: Whether to maintain aspect ratio
        :return: Image URL
        """
        url = self._construct_url(f"/{image_id}")

        params = {}
        if width:
            params["w"] = width
        if height:
            params["h"] = height
        if maintain_aspect_ratio:
            params["maintain_aspect_ratio"] = "true"

        if params:
            url += "&" + "&".join([f"{key}={value}" for key, value in params.items()])

        return url

    def get_random_image_url(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect_ratio: bool = False,
    ) -> str:
        """
        Get a random image URL

        :param width: Desired width
        :param height: Desired height
        :param maintain_aspect_ratio: Whether to maintain aspect ratio
        :return: Random image URL
        """
        url = self._construct_url("/random")

        params = {}
        if width:
            params["w"] = width
        if height:
            params["h"] = height
        if maintain_aspect_ratio:
            params["maintain_aspect_ratio"] = "true"

        if params:
            url += "&" + "&".join([f"{key}={value}" for key, value in params.items()])

        return url
