# ReconGraph

ReconGraph is a powerful platform that maps your **digital footprint** across various platforms and services. It provides comprehensive insights into your online presence, scans for website vulnerabilities, and analyzes file capabilities using **CAPA**.

---

## 🚀 Features

- **Digital Footprint Mapping**: Identify and track your online presence across various apps and platforms.
- **Website Exposure Analysis**: Analyze websites for open ports, running services, and other exposed information.
- **File Analysis with CAPA**: Extract capabilities from executable files to detect potential malicious behavior.

---

## 🛠️ Installation

Ensure you have **Python 3.10+** installed on your system.

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/ReconGraph.git
cd ReconGraph
```

2. **Set up a virtual environment (optional but recommended)**:

```bash
python -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Flask server using the following command:

```bash
python src/main.py
```

### API Endpoints

1. **Map Digital Footprint**

   **POST** `/api/footprint`
   ```json
   {
     "username": "example_user"
   }
   ```

2. **Analyze Website Exposure**

   **POST** `/api/website`
   ```json
   {
     "url": "http://example.com"
   }
   ```

3. **Run File Analysis with CAPA**

   **POST** `/api/file`
   ```json
   {
     "file_path": "path/to/binary"
   }
   ```

Example Request with `curl`:

```bash
curl -X POST http://localhost:5000/api/footprint -H "Content-Type: application/json" -d '{"username": "example_user"}'
```

---


## 🤝 Contributing

We welcome contributions! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

Please ensure your code follows the existing style and includes tests where applicable.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

**ReconGraph** - Mapping the digital world, one footprint at a time. 🌐
