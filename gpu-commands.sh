#!/bin/bash
# Hashcats GPU Miner - Quick Setup Commands
# Run these commands ONE BY ONE on your GPU server

echo "=========================================="
echo "HASHCATS GPU MINER - SETUP SCRIPT"
echo "=========================================="
echo ""

# Step 1: Check GPU
echo "Step 1: Checking GPU..."
nvidia-smi
echo ""
read -p "Did you see GPU info? (y/n): " gpu_check
if [ "$gpu_check" != "y" ]; then
    echo "⚠️  GPU not detected. You can still mine with CPU."
fi
echo ""

# Step 2: Update system
echo "Step 2: Updating system..."
sudo apt update
echo ""

# Step 3: Install Python
echo "Step 3: Installing Python..."
sudo apt install python3 python3-pip -y
echo ""

# Step 4: Install required packages
echo "Step 4: Installing mining packages..."
pip3 install web3 eth-account pycryptodome requests numpy
echo ""

# Step 5: Try GPU acceleration
if [ "$gpu_check" = "y" ]; then
    echo "Step 5: Installing GPU acceleration..."
    pip3 install pycuda
    echo ""
fi

# Step 6: Download miner (you need to upload hashcats_miner.py first)
echo "=========================================="
echo "SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Upload hashcats_miner.py to this server"
echo "2. Run: python3 hashcats_miner.py"
echo "3. Enter your private key when prompted"
echo ""
echo "To run in background:"
echo "  nohup python3 hashcats_miner.py > miner.log 2>&1 &"
echo ""
echo "To check logs:"
echo "  tail -f miner.log"
echo ""
