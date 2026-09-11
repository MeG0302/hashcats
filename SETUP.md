# Hashcats GPU Miner Setup Guide

## Step-by-Step Installation for GPU Server

### Step 1: Check Your GPU
```bash
nvidia-smi
```
This should show your GPU model and driver version.

### Step 2: Install Python Dependencies
```bash
# Install Python packages
pip install web3 eth-account pycryptodome requests numpy

# For GPU acceleration (if you have CUDA)
pip install pycuda
```

### Step 3: Get Your Private Key
You need your wallet's private key. **NEVER SHARE THIS!**

To export from MetaMask:
1. Click the 3 dots next to your account
2. Account details → Show private key
3. Enter password and copy the key

### Step 4: Run the Miner

#### Basic CPU Version (Simple, Works Everywhere)
```bash
python hashcats_miner.py
```

#### GPU Version (Faster, Requires CUDA)
```bash
python hashcats_gpu_miner.py
```

### Step 5: Enter Your Private Key
When prompted, paste your private key and press Enter.

The miner will start and show:
- ✅ Current hashrate (MH/s or GH/s)
- ✅ Expected time to find a cat
- ✅ Chance per minute
- ✅ Best hash found so far
- ✅ Network difficulty
- ✅ Cost for next cat

## Quick Commands for GPU Server

### 1. First Time Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install dependencies
pip3 install web3 eth-account pycryptodome requests numpy
```

### 2. Check if CUDA is available
```bash
nvidia-smi
nvcc --version
```

### 3. Install CUDA support (if available)
```bash
pip3 install pycuda
```

### 4. Download the miner
```bash
# Copy hashcats_miner.py to your server
# You can use: scp, wget, or paste directly
```

### 5. Run it
```bash
python3 hashcats_miner.py
```

### 6. Run in background (keeps running after you disconnect)
```bash
nohup python3 hashcats_miner.py > miner.log 2>&1 &
```

### 7. Check if it's running
```bash
tail -f miner.log
```

### 8. Stop the miner
```bash
# Find the process
ps aux | grep hashcats

# Kill it (replace XXXX with the process ID)
kill XXXX
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'web3'"
```bash
pip3 install web3
```

### "GPU not detected"
The miner will work with CPU. For GPU:
```bash
# Check CUDA
nvidia-smi

# Install CUDA toolkit if missing
sudo apt install nvidia-cuda-toolkit -y

# Install pycuda
pip3 install pycuda
```

### "Connection failed"
Check your internet connection and RPC URL.

### "Insufficient funds"
You need ETH on Robinhood Chain to pay for minting:
- Check balance on Robinhood Chain
- Bridge ETH to Robinhood Chain if needed

## One-Line Installation (Copy-Paste Ready)

```bash
sudo apt update && sudo apt install python3 python3-pip -y && pip3 install web3 eth-account pycryptodome requests numpy && echo "Setup complete! Now run: python3 hashcats_miner.py"
```

## Performance Tips

1. **GPU is ~40-100x faster** than CPU
2. **Close other programs** to maximize hashrate
3. **Check temperature**: `nvidia-smi` - keep under 80°C
4. **Multiple GPUs**: Modify script to use multiple devices
5. **Network stability**: Use reliable RPC endpoint

## Security Notes

⚠️ **IMPORTANT**:
- Never share your private key
- Never run unknown code with your private key
- Review the code before running
- Use a separate wallet for mining if possible
- Keep your private key secure

## Expected Hashrates

- **Modern GPU (RTX 3090)**: 500-1000 MH/s
- **Mid GPU (GTX 1050 Ti)**: 200-300 MH/s  
- **CPU (8 cores)**: 5-10 MH/s per core

## Current Difficulty Reference

At 48 bits:
- Total hashes needed: ~281 trillion
- With 500 MH/s: ~6-7 days average
- With 1 GH/s: ~3-4 days average

Check the miner display for real-time calculations!
