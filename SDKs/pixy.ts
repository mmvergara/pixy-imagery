interface PixyImageryOptions {
  baseUrl?: string;
  apiKey?: string | null;
}

interface ImageUploadResult {
  images: Array<{
    image_id: string;
    url: string;
  }>;
}

interface ResizeOptions {
  width?: number;
  height?: number;
  maintainAspectRatio?: boolean;
}

export class PixyImagery {
  private baseUrl: string;
  private apiKey: string | null;

  /**
   * Create a new PixyImagery client
   * @param options - Configuration options
   */
  constructor(options: PixyImageryOptions = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:5100';
    this.apiKey = options.apiKey || null;
  }

  /**
   * Construct URL with API key if required
   * @param endpoint - Endpoint path
   * @returns Full URL with optional API key
   */
  private _constructUrl(endpoint: string): string {
    const url = new URL(endpoint, this.baseUrl);
    if (this.apiKey) {
      url.searchParams.set('api_key', this.apiKey);
    }
    return url.toString();
  }

  /**
   * Upload one or more images
   * @param images - Images to upload
   * @returns Upload result
   */
  async uploadImages(images: File[] | FileList): Promise<ImageUploadResult> {
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
   * @param imageId - ID of the image
   * @param options - Resize options
   * @returns Image blob
   */
  async getImage(imageId: string, options: ResizeOptions = {}): Promise<Blob> {
    const url = new URL(this._constructUrl(`/${imageId}`));
    
    if (options.width) url.searchParams.set('w', options.width.toString());
    if (options.height) url.searchParams.set('h', options.height.toString());
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
   * @param options - Resize options
   * @returns Random image blob
   */
  async getRandomImage(options: ResizeOptions = {}): Promise<Blob> {
    const url = new URL(this._constructUrl('/random'));
    
    if (options.width) url.searchParams.set('w', options.width.toString());
    if (options.height) url.searchParams.set('h', options.height.toString());
    if (options.maintainAspectRatio) url.searchParams.set('maintain_aspect_ratio', 'true');

    const response = await fetch(url.toString());

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to retrieve random image');
    }

    return response.blob();
  }
}