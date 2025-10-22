# Service Restart Guide - Lambda Labs GPU Deployment

## 🚨 **CRITICAL: Avoiding Jupyter Interference**

When you see the service restart prompts during deployment, here's what to do:

### **For the "Pending kernel upgrade" dialog:**
- **Click "OK"** - This just acknowledges the kernel update
- **DO NOT restart the system** - This would break Jupyter
- The kernel update will be applied on the next system reboot (which you can do later)

### **For the "Daemons using outdated libraries" dialog:**
- **UNCHECK these services** (they can interfere with Jupyter):
  - `[] dbus.service` (unchecked)
  - `[] getty@tty1.service` (unchecked) 
  - `[] networkd-dispatcher.service` (unchecked)
  - `[] systemd-logind.service` (unchecked)
  - `[] unattended-upgrades.service` (unchecked)

- **KEEP CHECKED these services** (they're safe):
  - `[*] chrony.service` (checked)
  - `[*] cloudflared.service` (checked)
  - `[*] cron.service` (checked)
  - `[*] glances.service` (checked)
  - `[*] irqbalance.service` (checked)
  - `[*] lambda-jupyter.service` (checked) - **IMPORTANT: Keep this checked**
  - `[*] multipathd.service` (checked)
  - `[*] packagekit.service` (checked)
  - `[*] polkit.service` (checked)
  - `[*] rdma-ndd.service` (checked)
  - `[*] rpcbind.service` (checked)
  - `[*] serial-getty@ttyS0.service` (checked)
  - `[*] ssh.service` (checked)
  - `[*] systemd-journald.service` (checked)
  - `[*] systemd-manager` (checked)
  - `[*] systemd-networkd.service` (checked)
  - `[*] systemd-resolved.service` (checked)
  - `[*] systemd-udevd.service` (checked)

- **Click "OK"** to proceed

## 🛡️ **REVAMPED DEPLOYMENT SCRIPT**

Use the new `lambda_deploy_revamped.sh` script instead of the original:

```bash
# Use the revamped script that avoids system restarts
./lambda_deploy_revamped.sh
```

### **Key Differences in the Revamped Script:**

1. **No system upgrade** - Only installs essential packages
2. **No systemd service creation** - Uses simple startup script instead
3. **Minimal NVIDIA driver installation** - No restart required
4. **Preserves Jupyter functionality** - No interference with existing services

## 🚀 **Quick Deployment Steps:**

### **Step 1: Use the Revamped Script**
```bash
# Make executable (on Lambda Labs instance)
chmod +x lambda_deploy_revamped.sh

# Run the revamped deployment
./lambda_deploy_revamped.sh
```

### **Step 2: Handle Service Restart Prompts**
When you see the service restart dialogs:

1. **Kernel upgrade dialog**: Click "OK" (don't restart)
2. **Service restart dialog**: 
   - Uncheck services that might interfere with Jupyter
   - Keep `lambda-jupyter.service` checked
   - Click "OK"

### **Step 3: Continue with Deployment**
The script will continue and complete without requiring a system restart.

## 🔧 **Alternative: Manual Service Selection**

If you want to be extra careful, you can manually select which services to restart:

**SAFE TO RESTART:**
- `chrony.service` - Time synchronization
- `cloudflared.service` - Cloudflare tunnel
- `cron.service` - Scheduled tasks
- `glances.service` - System monitoring
- `irqbalance.service` - IRQ balancing
- `lambda-jupyter.service` - **Keep this for Jupyter**
- `multipathd.service` - Storage multipathing
- `packagekit.service` - Package management
- `polkit.service` - Policy kit
- `rdma-ndd.service` - RDMA networking
- `rpcbind.service` - RPC binding
- `serial-getty@ttyS0.service` - Serial console
- `ssh.service` - SSH access
- `systemd-journald.service` - System logging
- `systemd-manager` - System manager
- `systemd-networkd.service` - Network management
- `systemd-resolved.service` - DNS resolution
- `systemd-udevd.service` - Device management

**AVOID RESTARTING:**
- `dbus.service` - System message bus (can break GUI)
- `getty@tty1.service` - Console login (can break terminal)
- `networkd-dispatcher.service` - Network dispatcher (can break network)
- `systemd-logind.service` - Login manager (can break user sessions)
- `unattended-upgrades.service` - Automatic updates (can cause conflicts)

## ✅ **Verification Steps:**

After deployment, verify everything is working:

```bash
# Test the chatbot
python3 lambda_quick_start.py

# Start the chatbot
./start_chatbot.sh

# Check Jupyter is still working
# (Your Jupyter notebook should still be accessible)
```

## 🎯 **Summary:**

1. **Use `lambda_deploy_revamped.sh`** instead of the original script
2. **Handle service restart prompts carefully** - uncheck services that might interfere with Jupyter
3. **Keep `lambda-jupyter.service` checked** to maintain Jupyter functionality
4. **No system restart required** - everything will work immediately

This approach ensures your Jupyter environment remains functional while successfully deploying the GPU-optimized chatbot! 🚀
