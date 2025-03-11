# 🌱 ফসল রোগ সনাক্তকরণ (Crop Disease Detection) 🚜  

This project detects crop diseases using **YOLO (Object Detection)** and **ViT (Vision Transformer for Classification)**.  
It also provides **treatment recommendations** using **FAISS vector database** and **LangChain RAG** with **Bengali translations**.  

---

## 🚀 Features
✅ Detects crop diseases from leaf images 📷  
✅ Provides **Bengali** treatment plans using **FAISS + LangChain**  
✅ **Flask Backend** for model inference 🖥️  
✅ **Gradio Frontend** for easy image upload 🌐  
✅ **Docker support** for easy deployment 🐳  

---

## 🔧 Installation & Setup (Run Without Docker)

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/sayedul45/crop_disease_detection.git
cd crop_disease_detection
```
---

## Set Up Backend
```sh
cd backend
pip install -r requirements.txt
python app.py
```
---

## Set Up Frontend
```sh
cd frontend
pip install -r requirements.txt
python app.py
```


## 🐳 Installation & Setup (Using Docker)
### 1️⃣ Build and Start the Containers
```sh
docker-compose up --build
```
✔ This will:

Start backend at http://localhost:5000
Start frontend at http://localhost:7860

### 2️⃣ Access the App
🌍 Backend API: http://localhost:5000/predict
🌍 Frontend UI: http://localhost:7860

### 3️⃣ Stop the Containers
```sh
docker-compose down
```
