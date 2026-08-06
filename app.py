import streamlit as st
import os
import tempfile
# نستورد المكتبة المحلية الموجودة في المستودع
from clipsai import Transcriber, ClipFinder, resize

st.set_page_config(page_title="ClipsAI - قص الفيديو", layout="wide")
st.title("🎬 ClipsAI - حول الفيديو الطويل إلى مقاطع")

uploaded_file = st.file_uploader("📤 اختر ملف فيديو", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # حفظ الفيديو في ملف مؤقت
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    st.video(video_path)
    st.success("✅ تم رفع الفيديو")

    # خيارات إضافية
    hf_token = st.text_input("رمز Hugging Face (اختياري – لتغيير الأبعاد)", type="password")
    do_resize = st.checkbox("تغيير الأبعاد إلى 9:16 (عمودي)")

    if st.button("🚀 ابدأ استخراج المقاطع"):
        status = st.status("جارٍ العمل...", expanded=True)
        try:
            # 1- تحويل الكلام إلى نص
            status.update(label="🎙️ جاري نسخ الكلام...")
            transcriber = Transcriber()
            transcription = transcriber.transcribe(audio_file_path=video_path)

            # 2- البحث عن المقاطع المناسبة
            status.update(label="✂️ جاري تحديد المقاطع...")
            clipfinder = ClipFinder()
            clips = clipfinder.find_clips(transcription=transcription)

            status.update(label=f"✅ تم العثور على {len(clips)} مقطع", state="running")
            st.subheader("📋 المقاطع المكتشفة")
            for i, clip in enumerate(clips):
                start = clip.start_time
                end = clip.end_time
                st.write(f"**مقطع {i+1}:** ⏱️ يبدأ {start:.1f}s - ينتهي {end:.1f}s - المدة {end-start:.1f}s")

            # 3- تغيير الأبعاد (إذا طلب المستخدم)
            if do_resize and hf_token:
                status.update(label="📐 جاري تغيير الأبعاد...")
                crops = resize(
                    video_file_path=video_path,
                    pyannote_auth_token=hf_token,
                    aspect_ratio=(9, 16)
                )
                out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                # حفظ الفيديو المُعاد تحجيمه (تختلف الطريقة حسب إصدار clipsai)
                if hasattr(crops, 'save_video'):
                    crops.save_video(out_path)
                elif hasattr(crops, 'write_video'):
                    crops.write_video(out_path)
                else:
                    # محاولة بديلة
                    crops[0].write_videofile(out_path, codec="libx264")
                with open(out_path, "rb") as f:
                    st.download_button("📥 تحميل الفيديو المُعاد تحجيمه", f, file_name="resized_video.mp4")
                status.update(label="✅ تم تغيير الأبعاد", state="complete")

            status.update(label="🎉 تم بنجاح!", state="complete")

        except Exception as e:
            status.update(label="❌ فشلت العملية", state="error")
            st.error(f"حدث خطأ: {e}")
        finally:
            # حذف الملف المؤقت
            if os.path.exists(video_path):
                os.unlink(video_path)
else:
    st.info("ℹ️ انتظر رفع فيديو للبدء")
