# LLM Provider Guide

Your app now supports **4 different LLM providers**. Choose based on your needs!

---

## 🔵 **Google Gemini** (RECOMMENDED - FREE)

**Best for:** Getting started quickly, completely free tier

**Note:** The app automatically tries the best available model (1.5-flash → 1.0-pro → gemini-pro)

### Setup:
1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Get API Key"** → **"Create API key in new project"**
3. Copy the key
4. In app → Select "🔵 Google Gemini Pro (FREE)"
5. Paste key in the API Key field
6. Click "🚀 Initialize System"

### Pricing:
- **100% FREE** for reasonable usage
- No billing card required
- Perfect for testing/development

### Strengths:
✅ Free tier  
✅ No credit card needed  
✅ Good quality responses  
✅ Easy to set up

---

## ⚡ **Groq Mixtral** (FREE & SUPER FAST)

**Best for:** Speed, large documents, free tier with good limits

**Note:** The app automatically tries the latest available models (Llama 3.3 → Llama 3.2 → Gemma → Mixtral)

⚠️ **Important:** Groq frequently updates and deprecates models. If you get a model decommissioned error:
1. Check: https://console.groq.com/docs/models
2. See which models are currently available
3. The app will automatically try the next available model

### Setup:
1. Go to: https://console.groq.com
2. Click **"Sign up"** (via Google/GitHub/Email)
3. In console, click **"API Keys"**
4. Click **"Create API Key"**
5. Copy the key
6. In app → Select "⚡ Groq Mixtral (FREE & FAST)"
7. Paste key and click "🚀 Initialize System"

### Pricing:
- **FREE** tier: Generous limits
- No credit card required for free tier
- Paid plans available for higher usage

### Current Models (Latest First):
✅ Llama 3.3 70B Versatile  
✅ Llama 3.2 90B Text  
✅ Llama 3.2 70B Text  
✅ Gemma 2 9B IT  
✅ Mixtral 8x7B 32768  

*(List updates as Groq adds/removes models)*

### Strengths:
✅ VERY FAST responses (~1 sec vs 10 sec with others)  
✅ Good free tier limits  
✅ Great for production use  
✅ Auto-selects latest available model

---

## 🔴 **OpenAI GPT-3.5** (PAID)

**Best for:** Maximum quality, most reliable

### Setup:
1. Go to: https://platform.openai.com/api-keys
2. Sign up for OpenAI account
3. Add **billing information** (credit card required)
4. Create API key
5. Copy the key
6. In app → Select "🔴 OpenAI GPT-3.5 (PAID)"
7. Paste key and click "🚀 Initialize System"

### Pricing:
- ~$0.0005 per 1K input tokens
- ~$0.001 per 1K output tokens
- Typical query: $0.001-0.005
- Set usage limits in OpenAI account

### Strengths:
✅ Best answer quality  
✅ Most reliable  
✅ Production-grade  
✅ Large context window

---

## Comparison Table

| Provider | Cost | Speed | Quality | Setup | Free Tier |
|----------|------|-------|---------|-------|-----------|
| **Google Gemini** | $0 | Fast | Good | ⭐⭐ Easy | Yes |
| **Groq** | $0 | ⚡ Fastest | Good | ⭐⭐ Easy | Yes |
| **OpenAI** | $$ | Fast | ⭐⭐⭐ Best | ⭐⭐⭐ Medium | No |

---

## Quick Start Recommendation

1. **Just testing?** → Use **Google Gemini** (free, easiest)
2. **Want speed?** → Use **Groq** (free, super fast)
3. **Need best quality?** → Use **OpenAI** (paid but best)

---

## Environment Variables (Optional)

You can set API keys as environment variables to avoid entering them each time:

**Windows CMD:**
```cmd
set OPENAI_API_KEY=sk-your-key
set GOOGLE_API_KEY=your-google-key
set GROQ_API_KEY=your-groq-key
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-your-key"
$env:GOOGLE_API_KEY="your-google-key"
$env:GROQ_API_KEY="your-groq-key"
```

**Then run:**
```bash
streamlit run app.py
```

---

## Troubleshooting

### "Could not connect to provider"
- Check your API key is correct
- Provider might be down - try another
- Check your internet connection

### "Quota exceeded"
- You've used up your free tier limits
- Switch to another provider
- Upgrade your billing plan

### "Ollama not running"
- Make sure Ollama is installed
- Open terminal and run: `ollama serve`
- Try: `ollama pull llama2` first

### Slow responses
- Groq is fastest (~1 sec)
- Ollama depends on your computer
- OpenAI is fast but uses internet

---

## Support Links

- **Google Gemini**: https://ai.google.dev/
- **Groq**: https://console.groq.com
- **OpenAI**: https://platform.openai.com
- **Ollama**: https://ollama.ai

---

**Recommended for first use: Google Gemini (FREE & EASY!)**
