interface PixyImageryOptions {
  baseUrl?: string;
  apiKey?: string | null;
}

interface ImageUploadResponse {
  images: { image_id: string; url: string }[];
}

interface ImageUrlOptions {
  width?: number;
  height?: number;
  maintainAspectRatio?: boolean;
}

export class PixyImagery {
  private baseUrl: string;
  private apiKey: string | null;

  /**
   * Create a new PixyImagery client
   * @param {PixyImageryOptions} options - Configuration options
   * @param {string} [options.baseUrl='http://localhost:5100'] - Base URL of the Pixy Imagery service
   * @param {string} [options.apiKey=null] - API key for authentication
   */
  constructor(options: PixyImageryOptions = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:5100';
    this.apiKey = options.apiKey || null;
  }

  /**
   * Construct URL with API key if required
   * @param {string} endpoint - Endpoint path
   * @returns {URL} Full URL with optional API key
   */
  private _constructUrl(endpoint: string): URL {
    const url = new URL(endpoint, this.baseUrl);
    if (this.apiKey) {
      url.searchParams.set('api_key', this.apiKey);
    }
    return url;
  }

  /**
   * Upload one or more images
   * @param {File[] | FileList} images - Images to upload
   * @returns {Promise<ImageUploadResponse>} Upload result
   */
  async uploadImages(images: File[] | FileList): Promise<ImageUploadResponse> {
    const formData = new FormData();
    
    // Ensure we're working with an array
    const imageArray = Array.from(images);
    
    // Append each image to FormData
    imageArray.forEach(image => {
      formData.append('images', image);
    });

    const url = this._constructUrl('/upload-image');
    
    const response = await fetch(url.toString(), {
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
   * Get image URL by its ID
   * @param {string} imageId - ID of the image
   * @param {ImageUrlOptions} [options={}] - URL options
   * @param {number} [options.width] - Desired width
   * @param {number} [options.height] - Desired height
   * @param {boolean} [options.maintainAspectRatio=false] - Maintain aspect ratio
   * @returns {string} Image URL
   */
  getImageUrl(imageId: string, options: ImageUrlOptions = {}): string {
    const url = this._constructUrl(`/${imageId}`);
    
    if (options.width) url.searchParams.set('w', options.width.toString());
    if (options.height) url.searchParams.set('h', options.height.toString());
    if (options.maintainAspectRatio) url.searchParams.set('maintain_aspect_ratio', 'true');

    return url.toString();
  }

  /**
   * Get a random image URL
   * @param {ImageUrlOptions} [options={}] - URL options
   * @param {number} [options.width] - Desired width
   * @param {number} [options.height] - Desired height
   * @param {boolean} [options.maintainAspectRatio=false] - Maintain aspect ratio
   * @returns {string} Random image URL
   */
  getRandomImageUrl(options: ImageUrlOptions = {}): string {
    const url = this._constructUrl('/random');
    
    if (options.width) url.searchParams.set('w', options.width.toString());
    if (options.height) url.searchParams.set('h', options.height.toString());
    if (options.maintainAspectRatio) url.searchParams.set('maintain_aspect_ratio', 'true');

    return url.toString();
  }
}
