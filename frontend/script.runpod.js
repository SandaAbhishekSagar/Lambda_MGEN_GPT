// RunPod-specific frontend modifications
// This file extends the main script.js to work with RunPod serverless endpoints

/**
 * Override the sendMessage method to work with RunPod's request format
 */
(function() {
    // Wait for chatbot to be initialized
    const initRunPodIntegration = () => {
        if (typeof chatbot === 'undefined') {
            setTimeout(initRunPodIntegration, 100);
            return;
        }
        
        console.log('🚀 Initializing RunPod integration');
        
        // Store original sendMessage method
        const originalSendMessage = chatbot.sendMessage.bind(chatbot);
        
        // Override sendMessage to use RunPod format
        chatbot.sendMessage = async function(message) {
            if (!message || !message.trim()) return;
            
            message = message.trim();
            
            // Add user message to UI
            this.addMessage(message, 'user');
            this.chatInput.value = '';
            this.messageCount++;
            
            // Show loading
            this.showLoading();
            
            const startTime = Date.now();
            
            try {
                console.log('📤 Sending to RunPod:', message);
                
                // RunPod serverless format
                const runpodPayload = {
                    input: {
                        question: message,
                        n_results: 10
                    }
                };
                
                // Prepare headers
                const headers = {
                    'Content-Type': 'application/json'
                };
                
                // Add API key if configured
                if (window.RUNPOD_API_KEY) {
                    headers['Authorization'] = `Bearer ${window.RUNPOD_API_KEY}`;
                }
                
                // Send request to RunPod
                const endpoint = window.API_ENDPOINTS?.chat || `${this.apiBaseUrl}/runsync`;
                console.log('📡 RunPod endpoint:', endpoint);
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(runpodPayload),
                    timeout: window.REQUEST_CONFIG?.timeout || 120000
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('📥 RunPod response:', data);
                
                // RunPod wraps the response in 'output' field
                const result = data.output || data;
                
                // Extract answer
                const answer = result.answer || "I couldn't generate an answer.";
                
                // Calculate response time
                const responseTime = Date.now() - startTime;
                this.responseTimes.push(responseTime);
                
                // Add bot message
                this.addMessage(answer, 'bot', {
                    sources: result.sources || [],
                    confidence: result.confidence || 'medium',
                    timing: result.timing || { total: responseTime / 1000 },
                    documentsSearched: result.documents_searched || 0
                });
                
                // Log performance
                console.log(`⏱️ Response time: ${responseTime}ms`);
                if (result.timing) {
                    console.log('⏱️ Backend timing:', result.timing);
                }
                
                // Check 8-second requirement
                const totalSeconds = responseTime / 1000;
                if (totalSeconds < 8) {
                    console.log(`✅ Meets requirement: ${totalSeconds.toFixed(2)}s < 8s`);
                } else {
                    console.warn(`⚠️ Exceeds requirement: ${totalSeconds.toFixed(2)}s > 8s`);
                }
                
                // Update stats
                this.updateStats();
                
            } catch (error) {
                console.error('❌ Error:', error);
                
                const responseTime = Date.now() - startTime;
                let errorMessage = 'Sorry, I encountered an error. ';
                
                if (error.name === 'AbortError' || responseTime > 120000) {
                    errorMessage += 'The request timed out. The server might be starting up (cold start). Please try again in a few seconds.';
                } else if (error.message.includes('Failed to fetch')) {
                    errorMessage += 'Could not connect to the server. Please check your internet connection and the endpoint URL.';
                } else {
                    errorMessage += error.message;
                }
                
                this.addMessage(errorMessage, 'bot', {
                    confidence: 'low',
                    error: true
                });
            } finally {
                this.hideLoading();
            }
        };
        
        console.log('✅ RunPod integration active');
        console.log('📡 API endpoint:', chatbot.apiBaseUrl);
    };
    
    // Start integration
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRunPodIntegration);
    } else {
        initRunPodIntegration();
    }
})();

console.log('🚀 RunPod script loaded');

