# FTP Protocol Implementation

Welcome to the **FTP Protocol Implementation** project!  
This Python-based solution brings together both connection-oriented and connectionless file transfer protocols, all accessible through a modern web interface.

---

## 🚀 Features

### 🔗 Connection-Oriented FTP (TCP)

- **Reliable Transmission:** Utilizes TCP sockets for robust data transfer.
- **Chunked File Transfer:** Files are split into 100-byte chunks for efficient handling.
- **Acknowledgments:** Each chunk requires confirmation, ensuring data integrity.
- **Timeout & Retransmission:** Automatic recovery from lost packets.
- **Guaranteed Delivery:** Your files arrive safely, every time.

### ⚡ Connectionless FTP (UDP)

- **Fast Transmission:** Leverages UDP sockets for speed.
- **Line-by-Line Transfer:** Files sent one line at a time.
- **No Overhead:** No acknowledgments or retransmissions—just quick delivery.
- **Best-Effort:** Ideal for scenarios where speed matters more than reliability.

---

## 🛠️ Installation

1. **Clone the repository** or set up your project directory.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage (Local Development)

Start the application (defaults to port 5000):

```bash
python app.py
```

Or override ports (web + TCP + UDP) and enable debug:

```bash
WEB_PORT=5050 CO_PORT=2525 CL_PORT=2424 FLASK_DEBUG=1 python app.py
```

Open your browser and visit: `http://localhost:<WEB_PORT>` (e.g. http://localhost:5050)

Temporary files go in `temp/`; uploaded files land in `uploads_connection_oriented/` or `uploads_connectionless/`.

---

## 💡 Why Use This Project?

- Learn the differences between TCP and UDP file transfers.
- Experiment with real-world networking concepts.
- Extend and customize for your own use cases.

---

## 🐳 Deploy with Docker

Build the image:

```bash
docker build -t ftp-transfer .
```

Run (mapping host port 8080 to container 5000):

```bash
docker run --rm -e WEB_PORT=5000 -e CO_PORT=2121 -e CL_PORT=2021 -p 8080:5000 ftp-transfer
```

Visit: http://localhost:8080

Persist uploads with a volume:

```bash
docker run --rm \
   -e WEB_PORT=5000 -p 8080:5000 \
   -v $(pwd)/uploads_connection_oriented:/app/uploads_connection_oriented \
   -v $(pwd)/uploads_connectionless:/app/uploads_connectionless \
   ftp-transfer
```

### Reverse Proxy (Nginx snippet)

```nginx
location / {
      proxy_pass http://127.0.0.1:8080;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

Set `WEB_PORT` to the internal Flask port and let Nginx handle TLS.

### Production Notes

- Uses Gunicorn (3 workers, 4 threads). Tune for CPU cores.
- Ensure proper file size limits at proxy layer if changing defaults.
- Run health checks against `/`.
- Add monitoring around chunk retransmission stats for TCP.

## 🤝 Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for:

- Setup & environment
- Coding / UI style guidelines
- Commit message conventions
- Pull request checklist
- Future improvement ideas

## 📄 License

This project is released under the MIT License. By submitting contributions you agree they are provided under the same license.

---

Enjoy seamless file transfers and explore the world of network protocols!

---

Made with ❤️ • Visit: https://cftechlab.hcsarker.me

---