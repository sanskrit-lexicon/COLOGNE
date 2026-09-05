_Created: 30-03-2025 · Last updated: 05-09-2026_

# Issue 445: Enhancements and API Development

This directory addresses Issue 445, focusing on specific enhancements and API development for the Sanskrit Lexicon project.

## Contents

- `abs.xml`: An XML file containing abstracted data or configurations.
- `frontend.html`: The frontend interface, incorporating JavaScript and jQuery for dynamic functionalities.
- `serve_api.py`: A Python script designed to serve the API, facilitating backend operations.
- `transform.xsl`: An XSLT stylesheet for transforming XML data, likely used in conjunction with `abs.xml`.

## Dependencies

- **Python 3.x**: Required to run `serve_api.py`.
- **Flask**: A Python web framework utilized in `serve_api.py`. Install it using:

  ```bash
  pip install flask
  ```

- **Flask-RESTx**: An extension for Flask that simplifies the creation of RESTful APIs. Install it using:

  ```bash
  pip install flask-restx
  ```

- **Flask-CORS**: A Flask extension for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible. Install it using:

  ```bash
  pip install flask-cors
  ```

- **lxml**: A Python library for processing XML and HTML, potentially required for XML transformations. Install it using:

  ```bash
  pip install lxml
  ```

- **sqlite3**: A lightweight disk-based database that doesn't require a separate server process. It comes pre-installed with Python.

- **JavaScript and jQuery**: Utilized in `frontend.html` for dynamic content and API interactions. Ensure a modern web browser is used to support these technologies.

## Usage

1. **Backend Setup**:

   - Navigate to the directory containing `serve_api.py`.

   - Ensure that the SQLite database file (`temp_pwg_10.sqlite`) and the XSLT file (`transform.xsl`) are present in the same directory.

   - Run the API server:

     ```bash
     python serve_api.py
     ```

   - By default, the server runs on `http://127.0.0.1:5000/`.

2. **Frontend Interaction**:

   - Open `frontend.html` in a web browser.

   - The frontend provides input fields for searching the dictionary by headwords and definitions.

   - Transliteration selection is purely handled on the frontend. The backend does not process transliterations.

## API Overview (Flask-based)

The API is built using the **Flask** web framework, with extensions **Flask-RESTx** for creating RESTful APIs and **Flask-CORS** for handling Cross-Origin Resource Sharing.

### **API Endpoint: `/search`**
- **Method:** `GET`
- **Description:** Searches the dictionary based on the provided parameters and returns matching entries.
- **Parameters:**

  | Parameter      | Type   | Description |
  |---------------|--------|-------------|
  | `key_query`   | string | The term to search in headwords. |
  | `data_query`  | string | The term to search in definitions. |

- **Example Request:**

  ```bash
  curl "http://127.0.0.1:5000/search?key_query=ramaRa&data_query=a"
  ```

- **Example Response (JSON format):**

  ```json
  {
    "results": [
      {
        "key": "कर्म",
        "lnum": "12345",
        "data": "action, work, deed"
      }
    ]
  }
  ```

## Parameters Passed from Frontend to Backend

The `frontend.html` file sends the following parameters to the backend API via HTTP requests:

1. **`key_query`**: The term entered in the headword input box.
2. **`data_query`**: The term entered in the definition input box.

## Dropdown Options in `frontend.html`

- **Input and Output Transliteration Schemes** are handled on the frontend and do not affect API requests.
- The frontend supports all scripts available in the [`@indic-transliteration/sanscript`](https://www.npmjs.com/package/@indic-transliteration/sanscript) package. These include:

  - **IAST**
  - **Harvard-Kyoto**
  - **SLP1**
  - **Velthuis**
  - **WX**
  - **Devanagari**
  - **Bengali**
  - **Gujarati**
  - **Gurmukhi**
  - **Kannada**
  - **Malayalam**
  - **Oriya**
  - **Tamil**
  - **Telugu**
  - **Grantha**

## Notes

- Ensure all dependencies are installed before running the scripts.
- Flask should be run in **debug mode** (`debug=True`) for development but should be disabled in production.
- The transliteration conversion is purely frontend-based and does not impact backend processing.
- For any issues or contributions, refer to the main repository's guidelines.

_Dr. Mārcis Gasūns_
