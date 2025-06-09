# Client Test Project

This is a simple client test project written in Python.

## Setup

This project uses `uv` for dependency management and virtual environment creation.

1. **Install `uv`:**
   If you don't have `uv` installed, you can install it using pip:
   ```bash
   pip install uv
   ```
   Or follow the instructions on the official `uv` documentation for other installation methods.

2. **Create a virtual environment and install dependencies:**
   Navigate to the project directory in your terminal and run:
   ```bash
   uv sync
   ```
   This command will create a virtual environment in `.venv` and install the dependencies listed in `requirements.txt`.

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
   (On Windows, use `.venv\Scripts\activate`)

## Running the Project

Once the virtual environment is activated, you can run the main script (assuming it's named `main.py`):

```bash
uv run python main.py
```

## Dependencies

The project dependencies are listed in [pyproject.toml](./pyproject.toml).


