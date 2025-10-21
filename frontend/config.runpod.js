/**
 * RunPod Configuration for Northeastern University Chatbot
 * 
 * SETUP INSTRUCTIONS:
 * 1. Deploy your chatbot to RunPod Serverless
 * 2. Get your endpoint URL from RunPod console
 * 3. Replace YOUR_ENDPOINT_ID below with your actual endpoint ID
 * 4. Rename this file to config.js (or copy the content)
 * 5. Deploy to Vercel
 * 
 * Your RunPod endpoint URL will look like:
 * https://api.runpod.ai/v2/abcd1234xyz/runsync
 *                              ^^^^^^^^^ this is your endpoint ID
 */

// RunPod endpoint configuration
window.API_BASE_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID";

// RunPod API key (if using authenticated endpoints)
// Leave empty if using public endpoint
window.RUNPOD_API_KEY = "";

// API endpoints
window.API_ENDPOINTS = {
    chat: window.API_BASE_URL + "/runsync",
    health: window.API_BASE_URL + "/health",
    status: window.API_BASE_URL + "/status"
};

// Request configuration
window.REQUEST_CONFIG = {
    timeout: 120000,  // 2 minutes (RunPod includes cold start time)
    maxRetries: 2,
    headers: {
        'Content-Type': 'application/json'
    }
};

// Add API key to headers if provided
if (window.RUNPOD_API_KEY) {
    window.REQUEST_CONFIG.headers['Authorization'] = `Bearer ${window.RUNPOD_API_KEY}`;
}

console.log('🚀 RunPod Configuration Loaded');
console.log('📡 API Base URL:', window.API_BASE_URL);
console.log('✅ RunPod endpoint ready');

