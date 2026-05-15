# 🚀 Quick Start Guide - ZERO Setup Required!

## **What is This?**
A ChatGPT-like app where you:
1. ✅ Upload a PDF
2. ✅ Ask questions
3. ✅ Get instant AI answers

**No installation. No setup. Just click and go!**

---

## **How to Use (3 Simple Steps)**

### **Step 1: Run the App**
```bash
streamlit run app.py
```
App opens in your browser (http://localhost:8501)

### **Step 2: Get a FREE API Key (Pick ONE)**

#### **Option A: Google Gemini (RECOMMENDED - Easiest)**
1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Get API Key"** → **"Create API key in new project"**
3. Copy the key
4. Paste in app under "Google API Key:"

**Why:** ✅ Completely FREE, ✅ No credit card, ✅ Instant access

---

#### **Option B: Groq (FREE & Super Fast)**
1. Go to: https://console.groq.com
2. Sign up (Google/GitHub/Email)
3. Go to **API Keys**
4. Click **"Create API Key"**
5. Copy the key
6. Select "⚡ Groq" in app, paste key

**Why:** ✅ FREE, ✅ Very fast, ✅ Good limits

**Models:** Automatically selects the latest available (Llama 3.3 → Llama 3.2 → Gemma → Mixtral)

**If you get a model error:** Check https://console.groq.com/docs/models for current available models

---

#### **Option C: OpenAI (If you have credits)**
1. Go to: https://platform.openai.com/api-keys
2. Create API key
3. Paste in app (costs ~$0.001 per question)

---

### **Step 3: Use the App**
1. **Select LLM provider** from dropdown (default: Google)
2. **Paste your API key** in the text field
3. **Click "🚀 Initialize System"**
4. **Upload a PDF** file
5. **Ask questions** in the chat
6. **Get instant answers!**

---

## **What's Free?**

| Provider | Cost | Limits | Speed |
|----------|------|--------|-------|
| **Google Gemini** | FREE | Generous | ⭐⭐⭐ Good |
| **Groq** | FREE | Very Generous | ⚡⚡⚡ Fast |
| **OpenAI** | $$ | No limit | ⭐⭐⭐ Good |

---

## **Example Usage**

```
1. Upload: company_report.pdf
2. Ask: "What are the key insights from Q4?"
3. Get: AI-generated answer in seconds
```

---

## **Troubleshooting**

### **"API Key Invalid"**
- Double-check you copied the full key
- No extra spaces at start/end
- Regenerate key from provider

### **"Could not connect"**
- Check internet connection
- Provider might be down (rare)
- Try another provider

### **Groq: "Model decommissioned" Error**
- Groq frequently updates their models
- Check available models: https://console.groq.com/docs/models
- The app auto-tries Llama 3.3 → Llama 3.2 → Gemma → Mixtral
- If all fail, pick a model from Groq console and let us know

### **"No documents found"**
- Make sure you uploaded a PDF first
- Click "Upload & Process" button

---

## **Keyboard Tips**
- **Ctrl+C**: Stop the app
- **Enter**: Submit question
- **Upload multiple PDFs**: Yes, supported!

---

## **Security**
🔒 Your API key is:
- ✅ Stored in your browser session only
- ✅ Never saved to disk
- ✅ Never shared with us
- ✅ Deleted when you close the app

---

## **Still Have Questions?**

Check the docs:
- [LLM_PROVIDERS.md](LLM_PROVIDERS.md) - Detailed provider info
- [INSTALLATION.md](INSTALLATION.md) - Setup help
- [README.md](README.md) - Full documentation

---

## **TL;DR (Too Long; Didn't Read)**

```bash
# 1. Run app
streamlit run app.py

# 2. Get FREE key from: https://aistudio.google.com/app/apikey

# 3. Paste key in app → Click Initialize → Upload PDF → Ask questions!
```

**That's it!** 🎉

---

**Enjoy! Questions? Check other docs or contact support.**
