<p align="center">
<h1 align="center">Pixy Imagery</h1>
</p>

<p align="center">
<svg width="300" height="300" viewBox="0 0 483 483" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M468.903 205.698C383.08 157.639 288.381 174.921 216.278 250.496C301.769 297.437 397.253 281.015 468.903 205.698ZM54.6244 37.2061C148.613 63.7409 202.981 142.379 200.551 246.073C107.573 218.995 52.0584 140.402 54.6244 37.2061ZM210.105 268.216C290.479 300.034 316.637 364.876 281.061 440.662C201.819 408.573 174.544 343.609 210.105 268.216ZM195.117 262.948C116.992 230.889 52.6169 258.631 23.0181 335.806C100.57 366.914 165.775 339.836 195.117 262.948Z" fill="#3BE8CC"/>
</svg>
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
