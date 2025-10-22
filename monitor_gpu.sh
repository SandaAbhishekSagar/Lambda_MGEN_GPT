#!/bin/bash

# GPU Monitoring Script for Lambda Labs
# Northeastern University Chatbot - Ultra-Fast GPU Deployment

echo "🔍 GPU MONITORING - Northeastern Chatbot"
echo "========================================"
echo "Target: Sub-8-second response times"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if nvidia-smi is available
check_nvidia_smi() {
    if command -v nvidia-smi &> /dev/null; then
        return 0
    else
        print_error "nvidia-smi not found - GPU monitoring not available"
        return 1
    fi
}

# Get GPU information
get_gpu_info() {
    echo "📊 GPU Information:"
    echo "------------------"
    
    if check_nvidia_smi; then
        nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw --format=csv,noheader,nounits | while IFS=',' read -r name memory_total memory_used memory_free utilization temperature power; do
            echo "GPU: $name"
            echo "Memory: ${memory_used}MB / ${memory_total}MB (${memory_free}MB free)"
            echo "Utilization: ${utilization}%"
            echo "Temperature: ${temperature}°C"
            echo "Power: ${power}W"
            echo ""
        done
    else
        print_error "Cannot get GPU information"
        return 1
    fi
}

# Monitor GPU usage in real-time
monitor_gpu_realtime() {
    echo "📈 Real-time GPU Monitoring (Ctrl+C to stop):"
    echo "---------------------------------------------"
    
    if check_nvidia_smi; then
        watch -n 1 nvidia-smi
    else
        print_error "Cannot start real-time monitoring"
        return 1
    fi
}

# Check application status
check_application_status() {
    echo "🔍 Application Status:"
    echo "---------------------"
    
    # Check if chatbot service is running
    if systemctl is-active --quiet northeastern-chatbot; then
        print_success "Chatbot service is running"
    else
        print_warning "Chatbot service is not running"
    fi
    
    # Check if API server is responding
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "API server is responding"
        
        # Get API health info
        echo "API Health Information:"
        curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Could not parse health response"
    else
        print_warning "API server is not responding"
    fi
    
    echo ""
}

# Check system resources
check_system_resources() {
    echo "💻 System Resources:"
    echo "-------------------"
    
    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU Usage: ${cpu_usage}%"
    
    # Memory usage
    memory_info=$(free -h | grep "Mem:")
    echo "Memory: $memory_info"
    
    # Disk usage
    disk_info=$(df -h / | tail -1 | awk '{print $3 " / " $2 " (" $5 " used)"}')
    echo "Disk: $disk_info"
    
    # Load average
    load_avg=$(uptime | awk -F'load average:' '{print $2}')
    echo "Load Average: $load_avg"
    
    echo ""
}

# Performance test
run_performance_test() {
    echo "⚡ Performance Test:"
    echo "--------------------"
    
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "Testing API response time..."
        
        # Test multiple requests
        for i in {1..3}; do
            echo "Test $i:"
            start_time=$(date +%s.%N)
            response=$(curl -s -X POST http://localhost:8000/chat \
                -H "Content-Type: application/json" \
                -d '{"question": "What programs does Northeastern offer?"}' \
                -w "%{http_code}")
            end_time=$(date +%s.%N)
            
            response_time=$(echo "$end_time - $start_time" | bc)
            http_code=$(echo "$response" | tail -c 4)
            
            if [ "$http_code" = "200" ]; then
                print_success "Response time: ${response_time}s"
                
                # Check if response time meets sub-8-second target
                if (( $(echo "$response_time < 8" | bc -l) )); then
                    print_success "✅ Meets sub-8-second target!"
                else
                    print_warning "⚠️ Response time exceeds 8 seconds"
                fi
            else
                print_error "HTTP $http_code - API error"
            fi
            echo ""
        done
    else
        print_warning "API server not available for performance test"
    fi
}

# Generate performance report
generate_report() {
    echo "📊 Performance Report:"
    echo "----------------------"
    
    # Get GPU info
    if check_nvidia_smi; then
        echo "GPU Status:"
        nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits | while IFS=',' read -r name memory_used memory_total utilization temperature; do
            echo "  $name: ${utilization}% utilization, ${temperature}°C, ${memory_used}MB/${memory_total}MB"
        done
    fi
    
    # Get system info
    echo "System Status:"
    echo "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
    echo "  Memory: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
    echo "  Load: $(uptime | awk -F'load average:' '{print $2}')"
    
    # Get application status
    if systemctl is-active --quiet northeastern-chatbot; then
        echo "  Chatbot Service: Running"
    else
        echo "  Chatbot Service: Not Running"
    fi
    
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "  API Server: Responding"
    else
        echo "  API Server: Not Responding"
    fi
    
    echo ""
}

# Main menu
show_menu() {
    echo "🔍 GPU Monitoring Menu:"
    echo "======================="
    echo "1. Show GPU Information"
    echo "2. Real-time GPU Monitoring"
    echo "3. Check Application Status"
    echo "4. Check System Resources"
    echo "5. Run Performance Test"
    echo "6. Generate Performance Report"
    echo "7. Exit"
    echo ""
    read -p "Select option (1-7): " choice
}

# Main function
main() {
    echo "🚀 Lambda Labs GPU Monitoring"
    echo "============================="
    echo ""
    
    # Check if running interactively
    if [ -t 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            case $choice in
                1)
                    get_gpu_info
                    ;;
                2)
                    monitor_gpu_realtime
                    ;;
                3)
                    check_application_status
                    ;;
                4)
                    check_system_resources
                    ;;
                5)
                    run_performance_test
                    ;;
                6)
                    generate_report
                    ;;
                7)
                    echo "Goodbye!"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option. Please select 1-7."
                    ;;
            esac
            echo ""
            read -p "Press Enter to continue..."
            echo ""
        done
    else
        # Non-interactive mode - show all information
        get_gpu_info
        check_application_status
        check_system_resources
        generate_report
    fi
}

# Handle command line arguments
case "${1:-}" in
    "info")
        get_gpu_info
        ;;
    "monitor")
        monitor_gpu_realtime
        ;;
    "status")
        check_application_status
        ;;
    "resources")
        check_system_resources
        ;;
    "test")
        run_performance_test
        ;;
    "report")
        generate_report
        ;;
    *)
        main
        ;;
esac
