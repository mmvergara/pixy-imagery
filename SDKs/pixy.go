package pixyimagery

import (
	"bytes"
	"encoding/json"
	"fmt"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
)

type PixyImagery struct {
	BaseURL string
	APIKey  *string
}

type ImageUploadResponse struct {
	Images []struct {
		ImageID string `json:"image_id"`
		URL     string `json:"url"`
	} `json:"images"`
}

type ImageURLOptions struct {
	Width              int  `json:"w,omitempty"`
	Height             int  `json:"h,omitempty"`
	MaintainAspectRatio bool `json:"maintain_aspect_ratio,omitempty"`
}

func NewPixyImagery(baseURL string, apiKey *string) *PixyImagery {
	if baseURL == "" {
		baseURL = "http://localhost:5100"
	}
	return &PixyImagery{
		BaseURL: baseURL,
		APIKey:  apiKey,
	}
}

func (p *PixyImagery) constructURL(endpoint string) string {
	url := fmt.Sprintf("%s%s", p.BaseURL, endpoint)
	if p.APIKey != nil {
		url += fmt.Sprintf("?api_key=%s", *p.APIKey)
	}
	return url
}

func (p *PixyImagery) UploadImages(images []string) (*ImageUploadResponse, error) {
	url := p.constructURL("/upload-image")

	var buf bytes.Buffer
	writer := multipart.NewWriter(&buf)

	for _, imagePath := range images {
		file, err := os.Open(imagePath)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		part, err := writer.CreateFormFile("images", filepath.Base(imagePath))
		if err != nil {
			return nil, err
		}

		_, err = io.Copy(part, file)
		if err != nil {
			return nil, err
		}
	}

	err := writer.Close()
	if err != nil {
		return nil, err
	}

	resp, err := http.Post(url, writer.FormDataContentType(), &buf)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		var errorData map[string]string
		json.NewDecoder(resp.Body).Decode(&errorData)
		return nil, fmt.Errorf("image upload failed: %s", errorData["error"])
	}

	var response ImageUploadResponse
	err = json.NewDecoder(resp.Body).Decode(&response)
	if err != nil {
		return nil, err
	}

	return &response, nil
}

func (p *PixyImagery) GetImageURL(imageID string, options *ImageURLOptions) string {
	url := p.constructURL(fmt.Sprintf("/%s", imageID))

	params := url.Values{}
	if options != nil {
		if options.Width > 0 {
			params.Set("w", fmt.Sprintf("%d", options.Width))
		}
		if options.Height > 0 {
			params.Set("h", fmt.Sprintf("%d", options.Height))
		}
		if options.MaintainAspectRatio {
			params.Set("maintain_aspect_ratio", "true")
		}
	}

	if len(params) > 0 {
		url += "&" + params.Encode()
	}

	return url
}

func (p *PixyImagery) GetRandomImageURL(options *ImageURLOptions) string {
	url := p.constructURL("/random")

	params := url.Values{}
	if options != nil {
		if options.Width > 0 {
			params.Set("w", fmt.Sprintf("%d", options.Width))
		}
		if options.Height > 0 {
			params.Set("h", fmt.Sprintf("%d", options.Height))
		}
		if options.MaintainAspectRatio {
			params.Set("maintain_aspect_ratio", "true")
		}
	}

	if len(params) > 0 {
		url += "&" + params.Encode()
	}

	return url
}
