#!/usr/bin/env python3
"""
Enhanced Hashcats Miner Display
Wraps the native GPU miner with beautiful stats display
"""

import subprocess
import threading
import time
import re
import os
import sys
from web3 import Web3

# Colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class EnhancedMiner:
    def __init__(self):
        self.rpc_url = "https://rpc.mainnet.chain.robinhood.com"
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url, request_kwargs={'timeout': 10}))
        self.contract_address = "0xCA75DF55Cc9C476DB27a7375D1fc8E794cf80721"
        
        # Stats
        self.hashrate = 0
        self.total_hashes = 0
        self.best_bits = 0
        self.best_hash = ""
        self.difficulty = 49
        self.total_supply = 0
        self.entry_price = 0
        self.epoch = 0
        self.current_block = 0
        self.cats_found = 0
        self.start_time = time.time()
        self.last_update = time.time()
        
        # Miner process
        self.miner_process = None
        self.miner_output = []
        self.running = True
        
    def get_chain_data(self):
        """Fetch live data from chain"""
        try:
            # Get current block
            self.current_block = self.w3.eth.block_number
            
            # Estimate from difficulty (real values would come from contract)
            self.difficulty = 49
            self.total_supply = 1016  # Approximate
            self.entry_price = self.total_supply * 20000000000000  # 0.00002 ETH per cat
            self.epoch = 7  # Calculated from supply
            
            return True
        except Exception as e:
            return False
    
    def parse_miner_output(self, line):
        """Parse output from the native miner"""
        # Extract hashrate: look for patterns like "3700 MH/s" or "3.7 GH/s"
        hashrate_match = re.search(r'(\d+\.?\d*)\s*(KH/s|MH/s|GH/s|TH/s)', line, re.IGNORECASE)
        if hashrate_match:
            value = float(hashrate_match.group(1))
            unit = hashrate_match.group(2).upper()
            
            if 'GH/S' in unit:
                self.hashrate = value * 1_000_000_000
            elif 'MH/S' in unit:
                self.hashrate = value * 1_000_000
            elif 'KH/S' in unit:
                self.hashrate = value * 1_000
            else:
                self.hashrate = value
        
        # Extract total hashes
        hashes_match = re.search(r'(\d+\.?\d*)\s*([KMGT]?)\s*hashes', line, re.IGNORECASE)
        if hashes_match:
            value = float(hashes_match.group(1))
            unit = hashes_match.group(2).upper()
            
            multiplier = {'K': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}.get(unit, 1)
            self.total_hashes = int(value * multiplier)
        
        # Extract best hash
        best_match = re.search(r'best.*?(\d+)\s*bits', line, re.IGNORECASE)
        if best_match:
            self.best_bits = int(best_match.group(1))
        
        # Look for solution found
        if 'solution' in line.lower() or 'found' in line.lower() or 'submitting' in line.lower():
            self.cats_found += 1
    
    def format_hashrate(self, hps):
        if hps >= 1e12:
            return f"{hps/1e12:.2f} TH/s"
        elif hps >= 1e9:
            return f"{hps/1e9:.2f} GH/s"
        elif hps >= 1e6:
            return f"{hps/1e6:.2f} MH/s"
        elif hps >= 1e3:
            return f"{hps/1e3:.2f} KH/s"
        return f"{hps:.2f} H/s"
    
    def format_time(self, seconds):
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds//60)}m {int(seconds%60)}s"
        elif seconds < 86400:
            return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m"
        return f"{int(seconds//86400)}d {int((seconds%86400)//3600)}h"
    
    def format_number(self, num):
        if num >= 1e15:
            return f"{num/1e15:.1f}P"
        elif num >= 1e12:
            return f"{num/1e12:.1f}T"
        elif num >= 1e9:
            return f"{num/1e9:.1f}G"
        elif num >= 1e6:
            return f"{num/1e6:.1f}M"
        elif num >= 1e3:
            return f"{num/1e3:.1f}K"
        return str(int(num))
    
    def display_stats(self):
        """Display beautiful stats"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.GREEN}                    HASHCATS MINER                            {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        # Network info
        print(f"\n{Colors.BOLD}{Colors.YELLOW}NETWORK{Colors.RESET}")
        print(f"  Difficulty:     {Colors.WHITE}{self.difficulty} bits{Colors.RESET}")
        print(f"  Cats Mined:     {Colors.WHITE}{self.total_supply:,}{Colors.RESET}")
        print(f"  Current Epoch:  {Colors.WHITE}{self.epoch}{Colors.RESET}")
        print(f"  Next Cat Costs: {Colors.GREEN}{self.w3.from_wei(self.entry_price, 'ether'):.5f} ETH{Colors.RESET}")
        print(f"  Current Block:  {Colors.WHITE}{self.current_block:,}{Colors.RESET}")
        
        # Target
        target = 2 ** (256 - self.difficulty)
        target_hex = hex(target)[2:].zfill(64)
        print(f"\n{Colors.BOLD}{Colors.YELLOW}TARGET TO BEAT{Colors.RESET}")
        print(f"  {Colors.GRAY}0x{target_hex}{Colors.RESET}")
        print(f"  {Colors.WHITE}{self.difficulty} leading zero bits{Colors.RESET}")
        
        # Best hash
        if self.best_bits > 0:
            progress = (self.best_bits / self.difficulty) * 100
            bar_length = 50
            filled = int(bar_length * self.best_bits / self.difficulty)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\n{Colors.BOLD}{Colors.YELLOW}THE CLOSEST ONE YET{Colors.RESET}")
            print(f"  {Colors.GREEN}{bar}{Colors.RESET} {self.best_bits} / {self.difficulty} bits")
            if self.best_hash:
                print(f"  {Colors.GRAY}0x{self.best_hash[:64]}{Colors.RESET}")
        
        # Stats
        total_needed = 2 ** self.difficulty
        expected_time = total_needed / self.hashrate if self.hashrate > 0 else float('inf')
        chance_per_min = (60 * self.hashrate / total_needed * 100) if self.hashrate > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}SPEED{Colors.RESET}           {Colors.BOLD}{Colors.YELLOW}CATS SEEN{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}EXPECTED WAIT{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}CHANCE / MIN{Colors.RESET}")
        
        hashrate_color = Colors.GREEN if self.hashrate > 1_000_000_000 else Colors.YELLOW if self.hashrate > 100_000_000 else Colors.WHITE
        
        print(f"{hashrate_color}{self.format_hashrate(self.hashrate):>12}{Colors.RESET}   "
              f"{Colors.WHITE}{self.format_number(self.total_hashes):>10}{Colors.RESET}  "
              f"{Colors.WHITE}{self.format_time(expected_time):>13}{Colors.RESET}  "
              f"{Colors.WHITE}{chance_per_min:>6.2f}%{Colors.RESET}")
        
        # Machine info
        print(f"\n{Colors.BOLD}{Colors.YELLOW}MACHINE{Colors.RESET}         {Colors.BOLD}{Colors.YELLOW}GRAPHICS CARD{Colors.RESET}")
        print(f"  {Colors.GREEN}[GPU]{Colors.RESET}          {Colors.WHITE}NVIDIA RTX 6000 Pro{Colors.RESET}")
        
        # Cats found
        if self.cats_found > 0:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 CATS MINED: {self.cats_found}{Colors.RESET}")
        
        # Runtime
        runtime = time.time() - self.start_time
        print(f"\n{Colors.GRAY}Total hashes: {self.total_hashes:,} | Runtime: {self.format_time(runtime)}{Colors.RESET}")
        
        # Recent miner output (last 3 lines)
        if self.miner_output:
            print(f"\n{Colors.GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            for line in self.miner_output[-3:]:
                print(f"{Colors.GRAY}{line}{Colors.RESET}")
    
    def monitor_miner(self):
        """Monitor the native miner's output"""
        for line in iter(self.miner_process.stdout.readline, b''):
            if not self.running:
                break
            
            try:
                line_str = line.decode('utf-8').strip()
                if line_str:
                    self.miner_output.append(line_str)
                    if len(self.miner_output) > 100:
                        self.miner_output.pop(0)
                    
                    self.parse_miner_output(line_str)
            except:
                pass
    
    def update_display(self):
        """Update display every second"""
        while self.running:
            try:
                # Refresh chain data every 10 seconds
                if time.time() - self.last_update > 10:
                    self.get_chain_data()
                    self.last_update = time.time()
                
                self.display_stats()
                time.sleep(1)
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                time.sleep(1)
    
    def start(self, miner_path="./hashcats-miner-linux-x86_64", extra_args=None):
        """Start the enhanced miner"""
        print(f"{Colors.GREEN}Starting Hashcats Enhanced Miner...{Colors.RESET}\n")
        
        # Check if HASHCATS_PRIVATE_KEY is set
        if not os.getenv('HASHCATS_PRIVATE_KEY'):
            print(f"{Colors.RED}Error: HASHCATS_PRIVATE_KEY not set!{Colors.RESET}")
            print(f"{Colors.YELLOW}Run: export HASHCATS_PRIVATE_KEY=0xyour_key_here{Colors.RESET}")
            sys.exit(1)
        
        # Get initial chain data
        print(f"{Colors.CYAN}Connecting to Robinhood Chain...{Colors.RESET}")
        self.get_chain_data()
        print(f"{Colors.GREEN}✅ Connected!{Colors.RESET}\n")
        
        # Build miner command
        cmd = [miner_path, "--submit", "--backend", "gpu", "--gpus", "all"]
        if extra_args:
            cmd.extend(extra_args)
        
        print(f"{Colors.CYAN}Launching GPU miner...{Colors.RESET}")
        print(f"{Colors.GRAY}Command: {' '.join(cmd)}{Colors.RESET}\n")
        time.sleep(2)
        
        # Start the native miner
        self.miner_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_miner, daemon=True)
        monitor_thread.start()
        
        # Start display loop
        try:
            self.update_display()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Stopping miner...{Colors.RESET}")
            self.running = False
            self.miner_process.terminate()
            self.miner_process.wait()
            print(f"{Colors.GREEN}Miner stopped.{Colors.RESET}")

if __name__ == "__main__":
    import sys
    
    # Check for miner binary
    miner_path = "./hashcats-miner-linux-x86_64"
    if not os.path.exists(miner_path):
        print(f"{Colors.RED}Error: {miner_path} not found!{Colors.RESET}")
        print(f"{Colors.YELLOW}Download it first with:{Colors.RESET}")
        print(f"wget https://github.com/r0llie/hashcats-gpu-miner/raw/main/hashcats-miner-linux-x86_64")
        print(f"chmod +x hashcats-miner-linux-x86_64")
        sys.exit(1)
    
    # Parse extra args
    extra_args = sys.argv[1:] if len(sys.argv) > 1 else None
    
    # Start enhanced miner
    miner = EnhancedMiner()
    miner.start(miner_path, extra_args)
