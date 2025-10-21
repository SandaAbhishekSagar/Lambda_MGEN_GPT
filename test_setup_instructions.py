"""
Setup Instructions and Environment Test
Provides clear instructions for setting up the RunPod deployment
"""

import os
import sys

def check_environment_variables():
    """Check if environment variables are set"""
    print("Checking Environment Variables...")
    print("=" * 50)
    
    # Your ChromaDB Cloud credentials
    chromadb_vars = {
        'CHROMA_API_KEY': 'ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW',
        'CHROMA_TENANT': '28757e4a-f042-4b0c-ad7c-9257cd36b130',
        'CHROMA_DATABASE': 'newtest'
    }
    
    print("Your ChromaDB Cloud credentials:")
    for var, value in chromadb_vars.items():
        print(f"  {var} = {value}")
    
    # Check if OpenAI API key is set
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print(f"\nOK OpenAI API Key: {openai_key[:8]}...")
    else:
        print("\nWARNING: OPENAI_API_KEY not set")
        print("You need to set this before testing")
    
    return True

def show_runpod_environment_variables():
    """Show the exact environment variables for RunPod"""
    print("\nRunPod Environment Variables:")
    print("=" * 50)
    print("Copy these to your RunPod endpoint configuration:")
    print()
    print("OPENAI_API_KEY=sk-proj-your-openai-key-here")
    print("CHROMA_API_KEY=ck-4RLZskGk7sxLbFNvMZCQY4xASn4WPReJ1W4CSf9tvhUW")
    print("CHROMA_TENANT=28757e4a-f042-4b0c-ad7c-9257cd36b130")
    print("CHROMA_DATABASE=newtest")
    print("CHROMA_HOST=localhost")
    print("CHROMA_PORT=8000")
    print()

def show_deployment_steps():
    """Show deployment steps"""
    print("RunPod Deployment Steps:")
    print("=" * 50)
    print("1. Push your code to GitHub:")
    print("   git add .")
    print("   git commit -m 'Add RunPod deployment'")
    print("   git push origin main")
    print()
    print("2. Go to RunPod Console:")
    print("   https://console.runpod.io/serverless")
    print()
    print("3. Create New Endpoint:")
    print("   - Click 'New Endpoint'")
    print("   - Select 'Import Git Repository'")
    print("   - Choose your repository")
    print("   - Select branch: main")
    print()
    print("4. Configure Endpoint:")
    print("   - Name: northeastern-university-chatbot")
    print("   - GPU: RTX 4090 or A100 (16GB+)")
    print("   - Workers: 1")
    print("   - Timeout: 300 seconds")
    print()
    print("5. Set Environment Variables:")
    print("   - Use the variables shown above")
    print()
    print("6. Deploy and Test:")
    print("   - Click 'Deploy Endpoint'")
    print("   - Wait for build to complete")
    print("   - Test with sample input")

def show_testing_instructions():
    """Show testing instructions"""
    print("Testing Instructions:")
    print("=" * 50)
    print("1. Local Testing (Optional):")
    print("   - Install dependencies: pip install -r requirements_runpod.txt")
    print("   - Set environment variables")
    print("   - Run: python runpod_quick_test.py")
    print()
    print("2. RunPod Testing:")
    print("   - Go to your endpoint in RunPod console")
    print("   - Click 'Requests' tab")
    print("   - Use test input:")
    print('   {"input": {"question": "What undergraduate programs does Northeastern offer?"}}')
    print()
    print("3. Expected Response:")
    print("   - Answer: Detailed response about programs")
    print("   - Sources: List of relevant sources")
    print("   - Confidence: high/medium/low")
    print("   - Timing: Response time in seconds")

def main():
    """Show setup instructions"""
    print("RunPod Deployment Setup Instructions")
    print("=" * 60)
    
    # Check environment
    check_environment_variables()
    
    # Show RunPod environment variables
    show_runpod_environment_variables()
    
    # Show deployment steps
    show_deployment_steps()
    
    # Show testing instructions
    show_testing_instructions()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Your ChromaDB Cloud credentials are ready!")
    print("You just need to:")
    print("1. Set your OpenAI API key")
    print("2. Push code to GitHub")
    print("3. Deploy via RunPod console")
    print("4. Set environment variables")
    print("5. Test the deployment")
    print("\nReady to deploy!")

if __name__ == "__main__":
    main()
