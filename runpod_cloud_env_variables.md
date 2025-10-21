# RunPod Environment Variables - ChromaDB Cloud Setup

## 🔧 Required Environment Variables for ChromaDB Cloud

### **OpenAI Configuration**
```bash
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
```

### **ChromaDB Cloud Configuration (Your Actual Values)**
```bash
CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMA_DATABASE=newtest
```

## 📋 Complete Environment Variables List

### **Essential Variables (Required)**
| Variable | Description | Your Value | Required |
|----------|-------------|------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` | ✅ Yes |
| `CHROMA_API_KEY` | Your ChromaDB API key | `ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW` | ✅ Yes |
| `CHROMA_TENANT` | Your ChromaDB tenant | `28757e4a-f042-4b0c-ad7c-9257cd36b130` | ✅ Yes |
| `CHROMA_DATABASE` | Your ChromaDB database | `newtest` | ✅ Yes |

### **Optional Variables (With Defaults)**
| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `CHROMA_HOST` | ChromaDB host (not needed for cloud) | `localhost` | ❌ No |
| `CHROMA_PORT` | ChromaDB port (not needed for cloud) | `8000` | ❌ No |

## 🚀 Setting Environment Variables in RunPod

### **Method 1: RunPod Console**
1. Go to your endpoint in [RunPod Console](https://console.runpod.io/serverless)
2. Click **Edit Endpoint**
3. Go to **Environment Variables** section
4. Add these variables:

```
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW
CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130
CHROMA_DATABASE=newtest
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### **Method 2: GitHub Secrets (for GitHub Actions)**
Add these to your GitHub repository secrets:
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add each secret:

```
OPENAI_API_KEY
CHROMA_API_KEY
CHROMA_TENANT
CHROMA_DATABASE
CHROMA_HOST
CHROMA_PORT
```

## 🔑 Getting Your API Keys

### **OpenAI API Key**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in to your account
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-proj-`)

### **ChromaDB Cloud Details (Already Found)**
- **API Key**: `ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW`
- **Tenant**: `28757e4a-f042-4b0c-ad7c-9257cd36b130`
- **Database**: `newtest`

## 🧪 Testing Environment Variables

### **Local Testing**
```bash
# Set environment variables
export OPENAI_API_KEY="sk-proj-your-key-here"
export CHROMA_API_KEY="ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW"
export CHROMA_TENANT="28757e4a-f042-4b0c-ad7c-9257cd36b130"
export CHROMA_DATABASE="newtest"

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
   - Solution: Verify ChromaDB credentials

3. **ChromaDB Cloud Connection**
   - Error: Connection to ChromaDB failed
   - Solution: Check `CHROMA_TENANT` and `CHROMA_DATABASE`

### **Debug Steps**
1. Check environment variables in RunPod console
2. Verify API keys are valid
3. Test ChromaDB connection
4. Check RunPod logs for errors

## 📊 Environment Variables Validation

### **Required Variables Check**
```python
# Check if all required variables are set
required_vars = ['OPENAI_API_KEY', 'CHROMA_API_KEY', 'CHROMA_TENANT', 'CHROMA_DATABASE']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
else:
    print("✅ All required environment variables are set")
```

### **ChromaDB Cloud Variables Check**
```python
# Check ChromaDB Cloud variables
chroma_vars = {
    'CHROMA_API_KEY': 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW',
    'CHROMA_TENANT': '28757e4a-f042-4b0c-ad7c-9257cd36b130',
    'CHROMA_DATABASE': 'newtest'
}

for var, value in chroma_vars.items():
    env_value = os.getenv(var)
    if env_value == value:
        print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: Expected {value}, got {env_value}")
```

## 🔒 Security Best Practices

### **API Key Security**
- Never commit API keys to GitHub
- Use environment variables or secrets
- Rotate keys regularly
- Monitor usage and costs

### **ChromaDB Cloud Security**
- Use secure API keys
- Monitor access logs
- Implement proper authentication
- Use HTTPS for connections

## 📈 Monitoring Environment Variables

### **Health Checks**
```python
def check_environment():
    """Check if all environment variables are properly set"""
    checks = {
        'OpenAI API Key': bool(os.getenv('OPENAI_API_KEY')),
        'ChromaDB API Key': bool(os.getenv('CHROMA_API_KEY')),
        'ChromaDB Tenant': bool(os.getenv('CHROMA_TENANT')),
        'ChromaDB Database': bool(os.getenv('CHROMA_DATABASE')),
    }
    
    for check, status in checks.items():
        print(f"{'✅' if status else '❌'} {check}: {'Set' if status else 'Missing'}")
    
    return all(checks.values())
```

## 🎯 Quick Setup Checklist

- [ ] Get OpenAI API key from OpenAI Platform
- [ ] Use your existing ChromaDB Cloud credentials
- [ ] Set environment variables in RunPod console
- [ ] Test the deployment
- [ ] Monitor performance and logs

## 🔄 ChromaDB Cloud vs Self-Hosted

### **ChromaDB Cloud (Your Setup)**
- ✅ No host URL needed
- ✅ No port configuration needed
- ✅ Managed by ChromaDB
- ✅ Automatic scaling
- ✅ Built-in security

### **Self-Hosted ChromaDB**
- ❌ Requires host URL
- ❌ Requires port configuration
- ❌ Manual management
- ❌ Manual scaling
- ❌ Manual security setup

---

**Ready to deploy? Use your ChromaDB Cloud credentials - no host URL needed!**
