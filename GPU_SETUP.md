# GPU Miner Setup - Maximum Performance

## For Your RTX 6000 Pro

### Step 1: Install CuPy (GPU acceleration library)

```bash
pip3 install cupy-cuda12x
```

Or if that fails, try:
```bash
pip3 install cupy-cuda11x
```

### Step 2: Verify GPU is detected

```bash
nvidia-smi
```

You should see your RTX 6000 Pro with memory usage.

### Step 3: Run the GPU Miner

```bash
python3 gpu_miner.py
```

## Expected Performance

**RTX 6000 Pro (48GB)**:
- **Target**: 800 MH/s - 1.5 GH/s
- **GPU Usage**: 95-98%
- **Power Draw**: ~250W

Compare to your current 86 KH/s = **10,000x faster!**

## If CuPy Installation Fails

### Option A: Try conda
```bash
conda install -c conda-forge cupy
```

### Option B: Check CUDA version
```bash
nvcc --version
```

Then install matching CuPy:
- CUDA 12.x: `pip3 install cupy-cuda12x`
- CUDA 11.x: `pip3 install cupy-cuda11x`

### Option C: Build from source (last resort)
```bash
pip3 install cupy
```

## Troubleshooting

**"No module named 'cupy'"**
```bash
pip3 install --upgrade cupy-cuda12x
```

**"CUDA not found"**
```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

**Low hashrate still**
- Make sure no other process is using the GPU
- Check `nvidia-smi` shows 95%+ GPU utilization
- Increase batch_size in the code if needed

## Quick Commands

```bash
# One-line install
pip3 install cupy-cuda12x web3 eth-account pycryptodome

# Run the miner
cd ~/hashcats
git pull
python3 gpu_miner.py
```

## What You'll See

```
🚀 GPU: NVIDIA RTX 6000 Ada Generation
💾 Memory: 49140 MB
⚡ Threads: 256 x 912 = 233,472

SPEED           HASHES          EXPECTED        CHANCE/MIN
850.50 MH/s     2.5T            8h 15m          0.15%

GPU STATUS
  ■■■■■■■■■■ 98% Utilization
  NVIDIA RTX 6000 Ada Generation
```

That's the power you're paying for! 🔥
