<p align="center">
<h1 align="center">Pixy Imagery</h1>
</p>

<p align="center">
<img src="logo.png" width="200" height="200" />
</p>

<p align="center">
Very simple HTTP Based on-premise image solution for development workflows.
</p>

---

## Installation

### Docker (Recommended)

```bash
docker build . -t pixy-imagery
docker run -p 5100:5100 pixy-imagery

# Visit http://localhost:5100
```

### Local

```bash
pip install -r requirements.txt
python app.py

# Visit http://localhost:5100
```

## API Reference

**IMPORTANT** <br/>
If API_KEY is set in `.env`, all endpoints require `?api_key=<api_key>` in the query string.

### `POST /upload-image`

- **Description**: Upload one or more images.

- **Form Data (required)**:

  - `images` (file field in form data)

- **Response**:
  - `{"image_id","url"}[]`

---

### `GET /<image_id>`

**Description**: Retrieve an image by its ID.

- **Query Params (optional)**:

  - `w` (width)
  - `h` (height)
  - `maintain_aspect_ratio` (boolean, default: `false`)

---

### `GET /random`

**Description**: Retrieve a random image.

**Optional Query Parameters**:

- `w` (width)
- `h` (height)
- `maintain_aspect_ratio` (boolean, default: `false`)
