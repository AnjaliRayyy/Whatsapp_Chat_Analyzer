# 📊 WhatsApp Chat Analyzer

A **Streamlit-based web application** that analyzes WhatsApp chat exports and provides meaningful insights through data visualization and statistics.

---

## 🚀 Features

* 📈 Total messages, words, media, and links analysis
* 👥 User-wise activity comparison
* 📅 Monthly and daily timeline of chats
* 🔥 Most active days and months
* ☁️ Word cloud generation
* 😂 Emoji usage analysis
* 🔗 URL detection and counting

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – Web interface
* **Pandas** – Data processing
* **Matplotlib** – Visualizations
* **WordCloud** – Word cloud generation
* **urlextract** – URL detection
* **emoji** – Emoji analysis

---

## 📂 Project Structure

```
whatsapp_chat_analyzer/
│
├── app.py
├── helper.py
├── preprocessor.py
├── stop_hinglish.txt
├── requirements.txt
└── README.md
```

---

## 📥 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📄 How to Use

1. Export your WhatsApp chat (**without media**)
2. Upload the `.txt` file in the app
3. Select a user or view overall chat statistics
4. Explore insights using interactive charts

---

## 📌 Sample Use Cases

* Analyze group chat activity
* Compare user participation
* Study emoji and word usage trends
* Visualize messaging patterns over time

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---
