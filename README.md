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

## ▶️ Usage

Start the application:

```bash
python app.py
```

Open your browser and visit: [http://localhost:5000](http://localhost:5000)

---

## 💡 Why Use This Project?

- Learn the differences between TCP and UDP file transfers.
- Experiment with real-world networking concepts.
- Extend and customize for your own use cases.

---

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
