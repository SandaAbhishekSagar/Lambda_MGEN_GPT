# RunPod Environment Variables - Northeastern University Chatbot

## 🔧 Required Environment Variables

### **OpenAI Configuration**
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### **ChromaDB Configuration**
```bash
CHROMA_API_KEY=your-chroma-api-key-here
CHROMA_HOST=your-chroma-host-url
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
```

## 📋 Complete Environment Variables List

### **Essential Variables (Required)**
| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` | ✅ Yes |
| `CHROMA_API_KEY` | Your ChromaDB API key | `your-chroma-key` | ✅ Yes |
| `CHROMA_HOST` | ChromaDB host URL | `https://your-chroma-host.com` | ✅ Yes |

### **Optional Variables (With Defaults)**
| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `CHROMA_PORT` | ChromaDB port | `8000` | ❌ No |
| `CHROMA_TENANT` | ChromaDB tenant | `default_tenant` | ❌ No |
| `CHROMA_DATABASE` | ChromaDB database | `default_database` | ❌ No |

## 🚀 Setting Environment Variables in RunPod

### **Method 1: RunPod Console**
1. Go to your endpoint in [RunPod Console](https://console.runpod.io/serverless)
2. Click **Edit Endpoint**
3. Go to **Environment Variables** section
4. Add each variable:

```
OPENAI_API_KEY=sk-proj-your-openai-key-here
CHROMA_API_KEY=your-chroma-api-key-here
CHROMA_HOST=https://your-chroma-host.com
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
```

### **Method 2: GitHub Secrets (for GitHub Actions)**
Add these to your GitHub repository secrets:
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add each secret:

```
OPENAI_API_KEY
CHROMA_API_KEY
CHROMA_HOST
CHROMA_PORT
CHROMA_TENANT
CHROMA_DATABASE
```

## 🔑 Getting Your API Keys

### **OpenAI API Key**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in to your account
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-proj-`)

### **ChromaDB API Key**
1. Go to your ChromaDB cloud instance
2. Navigate to **Settings** or **API Keys**
3. Generate a new API key
4. Copy the key

### **ChromaDB Host**
- If using ChromaDB Cloud: `https://your-instance.chromadb.com`
- If using self-hosted: `https://your-domain.com`
- If using local: `localhost` (not recommended for production)

## 🧪 Testing Environment Variables

### **Local Testing**
```bash
# Set environment variables
export OPENAI_API_KEY="sk-proj-your-key-here"
export CHROMA_API_KEY="your-chroma-key-here"
export CHROMA_HOST="https://your-chroma-host.com"
export CHROMA_PORT="8000"

# Test the handler
python runpod_quick_test.py
```

### **RunPod Testing**
1. Go to your endpoint in RunPod console
2. Click **Requests** tab
3. Use test input:
```json
{
    "input": {
        "question": "What undergraduate programs does Northeastern offer?"
    }
}
```

## 🚨 Troubleshooting Environment Variables

### **Common Issues**

1. **Missing API Keys**
   - Error: `OPENAI_API_KEY not set!`
   - Solution: Add the environment variable in RunPod console

2. **Invalid ChromaDB Connection**
   - Error: `CHROMA_API_KEY not set!`
   - Solution: Verify ChromaDB credentials and host URL

3. **Connection Timeout**
   - Error: Connection to ChromaDB failed
   - Solution: Check `CHROMA_HOST` and `CHROMA_PORT`

### **Debug Steps**
1. Check environment variables in RunPod console
2. Verify API keys are valid
3. Test ChromaDB connection
4. Check RunPod logs for errors

## 📊 Environment Variables Validation

### **Required Variables Check**
```python
# Check if all required variables are set
required_vars = ['OPENAI_API_KEY', 'CHROMA_API_KEY', 'CHROMA_HOST']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
else:
    print("✅ All required environment variables are set")
```

### **Optional Variables Check**
```python
# Check optional variables with defaults
optional_vars = {
    'CHROMA_PORT': '8000',
    'CHROMA_TENANT': 'default_tenant',
    'CHROMA_DATABASE': 'default_database'
}

for var, default in optional_vars.items():
    value = os.getenv(var, default)
    print(f"✅ {var}: {value}")
```

## 🔒 Security Best Practices

### **API Key Security**
- Never commit API keys to GitHub
- Use environment variables or secrets
- Rotate keys regularly
- Monitor usage and costs

### **ChromaDB Security**
- Use HTTPS for ChromaDB connections
- Implement proper authentication
- Monitor access logs
- Use secure API keys

## 📈 Monitoring Environment Variables

### **Health Checks**
```python
def check_environment():
    """Check if all environment variables are properly set"""
    checks = {
        'OpenAI API Key': bool(os.getenv('OPENAI_API_KEY')),
        'ChromaDB API Key': bool(os.getenv('CHROMA_API_KEY')),
        'ChromaDB Host': bool(os.getenv('CHROMA_HOST')),
        'ChromaDB Port': bool(os.getenv('CHROMA_PORT', '8000')),
    }
    
    for check, status in checks.items():
        print(f"{'✅' if status else '❌'} {check}: {'Set' if status else 'Missing'}")
    
    return all(checks.values())
```

## 🎯 Quick Setup Checklist

- [ ] Get OpenAI API key from OpenAI Platform
- [ ] Get ChromaDB API key from your ChromaDB instance
- [ ] Note your ChromaDB host URL
- [ ] Set environment variables in RunPod console
- [ ] Test the deployment
- [ ] Monitor performance and logs

---

**Ready to deploy? Set these environment variables in your RunPod endpoint and you're good to go!**
