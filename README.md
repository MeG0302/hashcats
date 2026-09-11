# 🎮 Hashcats GPU Miner

A Python-based GPU/CPU miner for Hashcats NFTs on Robinhood Chain.

![Mining Interface](https://via.placeholder.com/800x400/1a1a1a/00ff00?text=HASHCATS+MINER)

## 📁 Files Included

| File | Purpose |
|------|---------|
| `hashcats_miner.py` | Main CPU miner (works everywhere) |
| `hashcats_gpu_miner.py` | GPU-accelerated version (requires CUDA) |
| `COPY_PASTE_COMMANDS.txt` | **START HERE** - Terminal commands |
| `START_MINING.md` | Quick start guide with examples |
| `TERMINAL_COMMANDS.txt` | Step-by-step terminal instructions |
| `MINER_SETUP.md` | Detailed setup guide |
| `requirements-miner.txt` | Python dependencies |

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install web3 eth-account pycryptodome requests numpy
```

### Step 2: Run the Miner
```bash
python3 hashcats_miner.py
```

### Step 3: Enter Your Private Key
When prompted, paste your wallet's private key (starts with `0x`)

## 📊 What You'll See

```
╔════════════════════════════════════════════════════════════════╗
║                    HASHCATS MINER                              ║
╚════════════════════════════════════════════════════════════════╝

NETWORK
  Difficulty:     48 bits
  Cats Mined:     867
  Next Cat Costs: 0.01736 ETH

TARGET TO BEAT                     48 leading zero bits
  0x0000000000001ce74f965da1fb4c88aab654e838f31a21...

THE CLOSEST ONE YET                39 / 48 bits
  0x00000000001ce74f965da1fb4c88aab654e838f31a21...

SPEED           CATS SEEN   EXPECTED WAIT   CHANCE / MIN
737.80 MH/s         4.4T            4d 9h             0.1%

MACHINE         GRAPHICS CARD
  [GPU]          NVIDIA GeForce RTX 3090
```

## ⚡ Performance

| Hardware | Hashrate | Expected Time (48 bits) |
|----------|----------|-------------------------|
| RTX 4090 | ~1.2 GH/s | 2-3 days |
| RTX 3090 | ~800 MH/s | 4-5 days |
| RTX 3080 | ~600 MH/s | 5-6 days |
| RTX 3070 | ~400 MH/s | 7-9 days |
| GTX 1050 Ti | ~250 MH/s | 12-15 days |
| CPU (8 cores) | ~40 MH/s | 230+ days |

*Note: Mining is probabilistic - actual time varies!*

## 🎯 Features

- ✅ **Real-time stats**: Hashrate, difficulty, expected time, chance per minute
- ✅ **GPU acceleration**: Automatic GPU detection and usage
- ✅ **Auto-refresh**: Updates chain data every 20 seconds
- ✅ **Best hash tracking**: Shows your closest attempt
- ✅ **Auto-submission**: Sends solutions to blockchain automatically
- ✅ **Colorful interface**: Easy-to-read terminal display
- ✅ **Background mode**: Run with `nohup` for persistent mining

## 🔧 Advanced Usage

### Run in Background
```bash
nohup python3 hashcats_miner.py > mining.log 2>&1 &
```

### Check Logs
```bash
tail -f mining.log
```

### Stop Mining
```bash
pkill -f hashcats_miner.py
```

### Check if Running
```bash
ps aux | grep hashcats_miner
```

## 📦 Dependencies

```
web3>=6.0.0
eth-account>=0.8.0
pycryptodome>=3.18.0
requests>=2.31.0
numpy>=1.24.0
pycuda>=2022.1 (optional, for GPU)
```

Install all at once:
```bash
pip3 install web3 eth-account pycryptodome requests numpy
```

## 🔐 Security

- ⚠️ **Never share your private key**
- ⚠️ **Review code before running**
- ⚠️ **Use a dedicated mining wallet**
- ⚠️ **Keep backups offline**
- ⚠️ **Ensure you have ETH on Robinhood Chain**

## 🎮 How Hashcats Mining Works

1. **Proof of Work**: Find a keccak256 hash below the target
2. **Hash Inputs**: `keccak256(address + nonce + previousWork + anchor)`
3. **Address Locked**: Your wallet address is in the hash (non-transferable)
4. **Time Limited**: Solutions expire in ~25 seconds
5. **Difficulty Scales**: Doubles every epoch (8 cats)
6. **Entry Price**: 0.00002 ETH × total cats minted

## 📈 Economics

- **Entry Price**: Increases with each cat (0.00002 ETH per existing cat)
- **Revenue Split**: 70% to holders, 30% to buyback
- **Burn Mechanism**: Burn cat → get $HASH tokens
- **Rent**: Earlier cats earn from later mints

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'web3'"
```bash
pip3 install web3
```

### "GPU not detected"
CPU mining works automatically. For GPU:
```bash
nvidia-smi  # Check if GPU is visible
pip3 install pycuda  # Install GPU support
```

### "Connection failed"
- Check internet connection
- Verify RPC endpoint is accessible
- Try again in a few seconds

### "Insufficient funds"
- Need ETH on Robinhood Chain for gas
- Check balance: Bridge ETH if needed

## 📚 Additional Resources

- **Hashcats Website**: https://hashcats.art
- **Contract**: 0xCA75DF55Cc9C476DB27a7375D1fc8E794cf80721
- **Chain**: Robinhood Chain
- **RPC**: https://rpc.robinhood.com

## 🎯 Mining Tips

1. **Use GPU**: 40-100x faster than CPU
2. **Background Mode**: Use `nohup` to keep mining after disconnect
3. **Monitor Temperature**: Keep GPU under 80°C
4. **Check Balance**: Ensure enough ETH for minting
5. **Be Patient**: Mining is probabilistic!

## 📝 License

MIT License - Use at your own risk

## ⚠️ Disclaimer

This software is for educational purposes. Mining cryptocurrencies and NFTs involves risk. Always:
- Do your own research
- Never invest more than you can afford to lose
- Verify all code before running
- Use secure, dedicated wallets

---

**Ready to mine? Open `COPY_PASTE_COMMANDS.txt` and get started! 🚀**
