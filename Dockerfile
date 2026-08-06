FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libmagic1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ننسخ كل ملفات المشروع أولاً (بما فيها setup.py و pyproject.toml)
COPY . /app

# الآن نثبّت الاعتماديات (بما فيها المشروع المحلي المحدد بـ -e .)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
