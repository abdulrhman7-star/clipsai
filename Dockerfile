FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libmagic1 git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# تثبيت PyTorch للـ CPU فقط (حجم أقل من 200 ميجا بدلاً من 2 جيجا)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# الآن تثبيت باقي الاعتماديات (سيرى أن torch مثبت بالفعل ولن يحاول تثبيت نسخة CUDA)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
