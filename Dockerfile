# استخدم إصدار Python المناسب (موجود في runtime.txt)
FROM python:3.10-slim

# تعيين دليل العمل
WORKDIR /app

# تثبيت حزم النظام الضرورية (ffmpeg و libmagic)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libmagic1 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات المتطلبات
COPY requirements.txt .
COPY packages.txt .

# تثبيت حزم Python (لاحظ أن whisperx يحتاج تثبيت خاص)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir whisperx@git+https://github.com/m-bain/whisperx.git

# نسخ باقي الكود
COPY . .

# متغير المنفذ
ENV PORT=8000
EXPOSE $PORT

# أمر التشغيل (يقرأ PORT من البيئة)
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
