import streamlit as st
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import which
from textblob import TextBlob
from reportlab.pdfgen import canvas
import tempfile
import os

AudioSegment.converter = which("ffmpeg")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 40px !important;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] {
    background-color: #0f172a;
}

[data-testid="stSidebar"] * {
    color: white !important;
}
            
.stDownloadButton button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 10px !important;
    height: 50px !important;
    font-size: 18px !important;
    font-weight: bold !important;
}
label {
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

[data-testid="stFileUploader"] label {
    color: white !important;
}
            /* File uploader button */
[data-testid="stFileUploader"] button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    border: none !important;
}

/* Upload area text */
[data-testid="stFileUploader"] {
    color: white !important;
}

/* File uploader label */
label {
    color: white !important;
    font-weight: bold !important;
}

/* Metric cards */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 40px !important;
    font-weight: bold !important;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Interview Coach")

with st.sidebar:
    st.title("🎤 AI Interview Coach")
    st.markdown("---")
    st.write("🤖 AI-Powered Interview Analysis")
    st.write("👩‍💻 Developed by Vahedunnisa")
    st.write("📊 Version 1.0")

st.title("🎤 AI Interview Coach")

st.markdown("""
### Analyze Your Interview Performance Using AI

✅ Speech-to-Text Analysis  
✅ Confidence Scoring  
✅ Technical Skill Detection  
✅ AI Feedback Generation  
✅ Performance Dashboard
""")
st.markdown("### 🎵 Upload Your Interview Recording")

uploaded_file = st.file_uploader(
    "",
    type=["wav", "mp3", "mp4", "m4a"]
)

if uploaded_file is not None:

    st.success("File uploaded successfully!")
    st.write("File Name:", uploaded_file.name)

    try:
        # Get original extension
        extension = os.path.splitext(uploaded_file.name)[1]

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as tmp:
            tmp.write(uploaded_file.read())
            temp_file = tmp.name

        # Convert audio/video to WAV
        audio = AudioSegment.from_file(temp_file)

        wav_file = temp_file + ".wav"
        audio.export(wav_file, format="wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        # -------------------------
        # TRANSCRIPT
        # -------------------------

        st.subheader("📝 Transcript")
        st.write(text)

        # -------------------------
        # FILLER WORD DETECTION
        # -------------------------

        filler_words = [
            "um",
            "uh",
            "like",
            "actually",
            "basically",
            "so"
        ]

        transcript = text.lower()

        count = 0
        found_words = []

        for word in filler_words:

            occurrences = transcript.count(word)

            if occurrences > 0:
                found_words.append(f"{word}: {occurrences}")
                count += occurrences

        st.subheader("🎯 Filler Word Analysis")

        if count == 0:
            st.success("No filler words detected!")
        else:
            for item in found_words:
                st.write(item)

            st.write("Total Filler Words:", count)

        # -------------------------
        # SPEAKING SPEED ANALYSIS
        # -------------------------

        duration_seconds = len(audio) / 1000

        word_count = len(text.split())

        wpm = (word_count / duration_seconds) * 60

        st.subheader("🎤 Speaking Speed Analysis")

        st.write("Total Words:", word_count)

        st.write(
            "Duration (seconds):",
            round(duration_seconds, 2)
        )

        st.write(
            "Words Per Minute (WPM):",
            round(wpm, 2)
        )

        if wpm < 100:
            st.warning("Speaking Pace: Too Slow")

        elif wpm <= 160:
            st.success("Speaking Pace: Good")

        else:
            st.warning("Speaking Pace: Too Fast")
        # -------------------------
        # SENTIMENT ANALYSIS
        # -------------------------

        blob = TextBlob(text)

        polarity = blob.sentiment.polarity

        st.subheader("😊 Sentiment Analysis")

        st.write("Sentiment Score:", round(polarity, 2))

        if polarity > 0.1:
            st.success("Positive Communication")

        elif polarity < -0.1:
            st.error("Negative Communication")

        else:
            st.info("Neutral Communication")

        # -------------------------
        # OVERALL INTERVIEW SCORE
        # -------------------------

        speed_score = 0
        filler_score = 0
        sentiment_score = 0

        # Speaking Speed Score
        if 100 <= wpm <= 160:
            speed_score = 40
        elif 80 <= wpm < 100 or 160 < wpm <= 180:
            speed_score = 30
        else:
            speed_score = 20

        # Filler Word Score
        if count == 0:
            filler_score = 30
        elif count <= 3:
            filler_score = 20
        else:
            filler_score = 10

        # Sentiment Score
        if polarity > 0.1:
            sentiment_score = 30
        elif polarity < -0.1:
            sentiment_score = 10
        else:
            sentiment_score = 20

        overall_score = speed_score + filler_score + sentiment_score

        st.subheader("🏆 Overall Interview Score")

        st.metric(
            label="Interview Score",
            value=f"{overall_score}/100"
        )

        if overall_score >= 80:
            st.success("Excellent Interview Performance!")

        elif overall_score >= 60:
            st.info("Good Interview Performance!")

        else:
            st.warning("Needs Improvement")
        # -------------------------
        # AI FEEDBACK GENERATOR
        # -------------------------

        st.subheader("🤖 AI Feedback")

        strengths = []
        improvements = []

        # Speed Feedback
        if 100 <= wpm <= 160:
            strengths.append("Good speaking pace")
        else:
            improvements.append("Maintain a speaking pace between 100 and 160 WPM")

        # Filler Word Feedback
        if count == 0:
            strengths.append("No filler words detected")
        else:
            improvements.append("Reduce filler words such as um, uh, like, actually")

        # Sentiment Feedback
        if polarity > 0.1:
            strengths.append("Positive communication style")
        elif polarity < -0.1:
            improvements.append("Try to sound more positive and confident")
        else:
            strengths.append("Neutral and professional tone")

        # Transcript Length Feedback
        if word_count >= 50:
            strengths.append("Provided detailed answers")
        else:
            improvements.append("Provide slightly more detailed responses")

        st.markdown("### ✅ Strengths")

        for item in strengths:
            st.write("✔", item)

        st.markdown("### 📈 Areas for Improvement")

        if len(improvements) == 0:
            st.write("✔ No major improvements needed")
        else:
            for item in improvements:
                st.write("✔", item)

        st.markdown("### 🎯 Final Recommendation")

        if overall_score >= 80:
            st.success(
            "You are interview-ready. Continue practicing and maintain your confidence."
            )

        elif overall_score >= 60:
            st.info(
                "You have a good foundation. Focus on the suggested improvements."
            )

        else:
            st.warning(
                "Practice more mock interviews to improve communication and confidence."
            )
        # -------------------------
        # TECHNICAL KEYWORD DETECTION
        # -------------------------

        technical_keywords = [
            "python",
            "java",
            "c",
            "sql",
            "html",
            "css",
            "javascript",
            "machine learning",
            "ml",
            "artificial intelligence",
            "ai",
            "data structures",
            "algorithms",
            "database",
            "web development",
            "cloud",
            "git",
            "github"
        ]

        found_keywords = []

        transcript_lower = text.lower()

        for keyword in technical_keywords:

            if keyword in transcript_lower:
                found_keywords.append(keyword)

        st.subheader("🧠 Technical Keyword Analysis")

        if len(found_keywords) == 0:
            st.warning("No technical keywords detected.")
        else:
            st.success(
                f"Detected {len(found_keywords)} technical keywords."
            )   

            for keyword in found_keywords:
                st.write("✔", keyword)
            st.write(
                    f"Technical Skill Score: {len(found_keywords)}/{len(technical_keywords)}"
                )

        # -------------------------
        # CONFIDENCE SCORE
        # -------------------------

        confidence_score = 100

        # Deduct for filler words
        confidence_score -= count * 5

        # Deduct for poor speaking pace
        if wpm < 100 or wpm > 160:
            confidence_score -= 10

        # Deduct for negative sentiment
        if polarity < -0.1:
            confidence_score -= 15

        # Prevent negative score
        confidence_score = max(0, confidence_score)

        st.subheader("🎙 Confidence Score")

        st.metric(
            label="Confidence",
            value=f"{confidence_score}/100"
        )

        if confidence_score >= 80:
            st.success("High Confidence")
        elif confidence_score >= 60:
            st.info("Moderate Confidence")
        else:
            st.warning("Low Confidence")

        # -------------------------
        # KPI CARDS
        # -------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Confidence",
                f"{confidence_score}/100"
            )

        with col2:
            st.metric(
            "Interview Score",
            f"{overall_score}/100"
        )
        
        # -------------------------
        # INTERVIEW DASHBOARD
        # -------------------------

        st.subheader("📊 Interview Dashboard")

        technical_score = min(len(found_keywords) * 10, 100)

        communication_score = 100

        communication_score -= count * 5

        if wpm < 100 or wpm > 160:
            communication_score -= 10

        communication_score = max(0, communication_score)

        chart_data = pd.DataFrame(
        {
            "Score": [
                confidence_score,
                overall_score,
                technical_score,
                communication_score
            ]
        },
        index=[
            "Confidence",
            "Interview Score",
            "Technical Skills",
            "Communication"
        ]
    )
        st.bar_chart(chart_data)
                # -------------------------
        # PDF REPORT GENERATION
        # -------------------------

        pdf_file = "Interview_Report.pdf"

        c = canvas.Canvas(pdf_file)

        c.setFont("Helvetica", 12)

        c.drawString(50, 800, "AI Interview Coach Report")

        c.drawString(50, 770, "Transcript Summary")
        c.drawString(50, 750, text[:100])

        c.drawString(50, 720, f"Filler Words: {count}")

        c.drawString(50, 690, f"Words Per Minute: {round(wpm, 2)}")

        c.drawString(50, 660, f"Sentiment Score: {round(polarity, 2)}")

        c.drawString(50, 630, f"Interview Score: {overall_score}/100")

        c.drawString(50, 600, f"Confidence Score: {confidence_score}/100")

        c.save()

        # Read PDF file
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()

        # Download button
        st.download_button(
            label="📄 Download Interview Report",
            data=pdf_data,
            file_name="Interview_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error("Could not convert speech to text")
        st.write(str(e))

    finally:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)

            if 'wav_file' in locals() and os.path.exists(wav_file):
                os.remove(wav_file)

        except:
            pass