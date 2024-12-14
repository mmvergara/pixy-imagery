export class PixyImagery {
  /**
   * Create a new PixyImagery client
   * @param {Object} options - Configuration options
   * @param {string} [options.baseUrl='http://localhost:5100'] - Base URL of the Pixy Imagery service
   * @param {string} [options.apiKey=null] - API key for authentication
   */
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:5100';
    this.apiKey = options.apiKey || null;
  }

  /**
   * Construct URL with API key if required
   * @param {string} endpoint - Endpoint path
   * @returns {string} Full URL with optional API key
   */
  _constructUrl(endpoint) {
    const url = new URL(endpoint, this.baseUrl);
    if (this.apiKey) {
      url.searchParams.set('api_key', this.apiKey);
    }
    return url.toString();
  }

  /**
   * Upload one or more images
   * @param {File[]|FileList} images - Images to upload
   * @returns {Promise<{images: {image_id: string, url: string}[]}>} Upload result
   */
  async uploadImages(images) {
    const formData = new FormData();
    
    // Ensure we're working with an array
    const imageArray = Array.from(images);
    
    // Append each image to FormData
    imageArray.forEach(image => {
      formData.append('images', image);
    });

    const url = this._constructUrl('/upload-image');
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Image upload failed');
    }

    return response.json();
  }

  /**
   * Get an image by its ID
   * @param {string} imageId - ID of the image
   * @param {Object} [options={}] - Resize options
   * @param {number} [options.width] - Desired width
   * @param {number} [options.height] - Desired height
   * @param {boolean} [options.maintainAspectRatio=false] - Maintain aspect ratio
   * @returns {Promise<Blob>} Image blob
   */
  async getImage(imageId, options = {}) {
    const url = new URL(this._constructUrl(`/${imageId}`));
    
    if (options.width) url.searchParams.set('w', options.width);
    if (options.height) url.searchParams.set('h', options.height);
    if (options.maintainAspectRatio) url.searchParams.set('maintain_aspect_ratio', 'true');

    const response = await fetch(url.toString());

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to retrieve image');
    }

    return response.blob();
  }

  /**
   * Get a random image
   * @param {Object} [options={}] - Resize options
   * @param {number} [options.width] - Desired width
   * @param {number} [options.height] - Desired height
   * @param {boolean} [options.maintainAspectRatio=false] - Maintain aspect ratio
   * @returns {Promise<Blob>} Random image blob
   */
  async getRandomImage(options = {}) {
    const url = new URL(this._constructUrl('/random'));
    
    if (options.width) url.searchParams.set('w', options.width);
    if (options.height) url.searchParams.set('h', options.height);
    if (options.maintainAspectRatio) url.searchParams.set('maintain_aspect_ratio', 'true');

    const response = await fetch(url.toString());

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to retrieve random image');
    }

    return response.blob();
  }
}
