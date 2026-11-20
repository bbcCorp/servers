# Variable Naming Update - LLM Configuration

**Date:** 2026-11-20  
**Status:** ✅ COMPLETE

---

## Changes Made

### Variable Renaming
Changed from provider-specific naming to generic LLM provider variables:

#### Before (Ollama-specific)
```env
OLLAMA_API="https://ollama.com/api"
OLLAMA_API_KEY="your-api-key"
```

#### After (Provider-agnostic)
```env
LLM_API="https://ollama.com/api"
LLM_API_KEY="your-api-key"
```

### Docker Compose Updates

#### Before
```yaml
HINDSIGHT_API_LLM_API_KEY: "${OLLAMA_API_KEY}"
HINDSIGHT_API_LLM_BASE_URL: "https://ollama.com/api"
HINDSIGHT_API_EMBEDDINGS_BASE_URL: "https://ollama.com/api"
```

#### After
```yaml
HINDSIGHT_API_LLM_API_KEY: "${LLM_API_KEY}"
HINDSIGHT_API_LLM_BASE_URL: "${LLM_API}"
HINDSIGHT_API_EMBEDDINGS_BASE_URL: "${LLM_API}"
```

---

## Benefits

✅ **Provider-agnostic naming** - Variables are not tied to a specific provider  
✅ **Easy switching** - Can swap LLM providers by just changing LLM_API and LLM_API_KEY  
✅ **Cleaner configuration** - Less clutter in environment variables  
✅ **Future-proof** - Ready for different LLM providers (OpenAI, Anthropic, etc.)

---

## Current Configuration

### Environment Variables
```env
LLM_API="https://ollama.com/api"
LLM_API_KEY="{your-ollama-cloud-api-key}"
```

### Hindsight Configuration
```
LLM Provider:        Ollama (via ${LLM_API})
LLM Model:          ollama
Embeddings Provider: Ollama (via ${LLM_API})
API Key:            ${LLM_API_KEY}
```

---

## Usage

### To switch LLM providers, simply update `.env`:

**Example 1: Ollama Cloud**
```env
LLM_API="https://ollama.com/api"
LLM_API_KEY="your-ollama-key"
```

**Example 2: OpenAI** (if Hindsight supports it)
```env
LLM_API="https://api.openai.com/v1"
LLM_API_KEY="sk-your-openai-key"
```

**Example 3: Local Ollama**
```env
LLM_API="http://localhost:11434"
LLM_API_KEY="ollama"
```

---

## Files Updated

✅ `.env` - Variable naming standardized  
✅ `docker-compose.yml` - Hindsight service uses new variable names  

---

## Verification

Environment variables are correctly substituted:
```bash
docker-compose config | grep -A 20 "hindsight:" | grep -E "LLM|EMBEDDINGS"
```

Output shows:
```
HINDSIGHT_API_LLM_API_KEY: ${LLM_API_KEY} → actual-key-value
HINDSIGHT_API_LLM_BASE_URL: ${LLM_API} → https://ollama.com/api
HINDSIGHT_API_EMBEDDINGS_BASE_URL: ${LLM_API} → https://ollama.com/api
```

---

## Next Steps

1. Add your Ollama Cloud API key to `.env`:
   ```env
   LLM_API_KEY="your-actual-api-key"
   ```

2. Restart Hindsight:
   ```bash
   docker-compose restart hindsight
   ```

3. Verify it's running:
   ```bash
   docker-compose logs hindsight
   docker-compose ps | grep hindsight
   ```

4. Access at: http://localhost:8080

---

## Summary

✅ Variables renamed from provider-specific to generic naming  
✅ Configuration remains functionally identical  
✅ More flexible for future provider changes  
✅ Cleaner environment configuration
