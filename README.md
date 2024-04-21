# Welcome to the Kohya Stable Diffusion FastAPI Project

This project combines Kohya's stable diffusion scripts with FastAPI to create a straightforward API designed for image captioning and model training tasks. Its primary purpose is to enable the invocation of Python scripts through unified HTTP requests. Below you will find the essential information to start using this project.

## Getting Started

### Prerequisites

- Python 3.10

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/gengen1988/kohya-restful.git
   cd kohya-restful
   ```

2. Setup venv and install dependencies:
   ```
   setup.bat
   ```

### Running the Server

```
start.bat
```

This will start the FastAPI server running on `http://127.0.0.1:8000`. The API endpoints are defined in the `main.py` file and can be accessed via the specified URL.

## Usage

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/sd-scripts/finetune/tag_images_by_wd14_tagger' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '["--help"]'
```

api docs: http://127.0.0.1:8000/docs

paths and args can be found in sd-scripts.

## Contributing

Contributions are welcome! Please read the CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Kohya-ss for the stable diffusion scripts
- FastAPI team for the great framework
