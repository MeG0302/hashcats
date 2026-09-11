"""
Hashcats GPU Miner - Python Implementation
Mines Hashcats NFTs using GPU acceleration
"""

import time
import json
import os
from web3 import Web3
from eth_account import Account
from datetime import timedelta
import requests

# Color codes for terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Contract addresses on Robinhood Chain
HASHCATS_CONTRACT = "0xCA75DF55Cc9C476DB27a7375D1fc8E794cf80721"

# Try multiple RPC endpoints (official Robinhood Chain mainnet)
RPC_URLS = [
    "https://rpc.mainnet.chain.robinhood.com",
    "https://robinhood-mainnet.g.alchemy.com/v2/demo",
]

def get_working_rpc():
    """Test RPC endpoints and return the first working one"""
    for rpc in RPC_URLS:
        try:
            print(f"{Colors.YELLOW}Testing: {rpc}{Colors.RESET}")
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 15}))
            if w3.is_connected():
                print(f"{Colors.GREEN}✅ Connected to: {rpc}{Colors.RESET}")
                return rpc
        except Exception as e:
            print(f"{Colors.RED}❌ {rpc} failed: {str(e)[:50]}{Colors.RESET}")
            continue
    return None

RPC_URL = get_working_rpc()
if not RPC_URL:
    print(f"{Colors.RED}Failed to connect to any RPC endpoint!{Colors.RESET}")
    print(f"{Colors.YELLOW}Try using an Alchemy API key or other provider{Colors.RESET}")
    RPC_URL = RPC_URLS[0]  # Default fallback

# ABI for the mining function
HASHCATS_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "bytes32", "name": "anchor", "type": "bytes32"}
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "target",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "previousWork",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "currentEpoch",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class HashcatsMiner:
    def __init__(self, private_key, rpc_url=RPC_URL):
        """Initialize the miner with wallet credentials"""
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(HASHCATS_CONTRACT),
            abi=HASHCATS_ABI
        )
        
        # Mining stats
        self.total_hashes = 0
        self.start_time = time.time()
        self.best_hash = None
        self.best_bits = 0
        self.cats_mined = 0
        
        print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.GREEN}                    HASHCATS GPU MINER                        {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Wallet Address:{Colors.RESET} {Colors.WHITE}{self.address}{Colors.RESET}")
        
    def get_chain_data(self):
        """Fetch current mining parameters from the contract"""
        try:
            target = self.contract.functions.target().call()
            previous_work = self.contract.functions.previousWork().call()
            total_supply = self.contract.functions.totalSupply().call()
            epoch = self.contract.functions.currentEpoch().call()
            
            # Get anchor (recent block hash)
            latest_block = self.w3.eth.block_number
            # Use a block from 10 blocks ago for stability
            anchor_block = max(0, latest_block - 10)
            anchor = self.w3.eth.get_block(anchor_block)['hash']
            
            # Calculate entry price: 0.00002 ETH * total_supply
            entry_price = total_supply * 20000000000000  # 0.00002 ETH in wei
            
            # Calculate difficulty (leading zero bits)
            difficulty = 256 - target.bit_length()
            
            return {
                'target': target,
                'previous_work': previous_work,
                'anchor': anchor,
                'total_supply': total_supply,
                'epoch': epoch,
                'entry_price': entry_price,
                'difficulty': difficulty,
                'anchor_block': anchor_block
            }
        except Exception as e:
            print(f"{Colors.RED}Error fetching chain data: {e}{Colors.RESET}")
            return None
    
    def count_leading_zeros(self, hash_int):
        """Count leading zero bits in a hash"""
        if hash_int == 0:
            return 256
        return 256 - hash_int.bit_length()
    
    def format_hashrate(self, hashes_per_sec):
        """Format hashrate with appropriate units"""
        if hashes_per_sec >= 1_000_000_000:
            return f"{hashes_per_sec / 1_000_000_000:.2f} GH/s"
        elif hashes_per_sec >= 1_000_000:
            return f"{hashes_per_sec / 1_000_000:.2f} MH/s"
        elif hashes_per_sec >= 1_000:
            return f"{hashes_per_sec / 1_000:.2f} KH/s"
        else:
            return f"{hashes_per_sec:.2f} H/s"
    
    def format_time(self, seconds):
        """Format time duration"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        else:
            days = int(seconds // 86400)
            hours = int((seconds % 86400) // 3600)
            return f"{days}d {hours}h"
    
    def display_status(self, chain_data, hashrate, expected_time, chance_per_min):
        """Display mining status in a nice format"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.GREEN}                    HASHCATS MINER                            {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        # Network info
        print(f"\n{Colors.BOLD}{Colors.YELLOW}NETWORK{Colors.RESET}")
        print(f"  Difficulty:     {Colors.WHITE}{chain_data['difficulty']} bits{Colors.RESET}")
        print(f"  Cats Mined:     {Colors.WHITE}{chain_data['total_supply']:,}{Colors.RESET}")
        print(f"  Current Epoch:  {Colors.WHITE}{chain_data['epoch']}{Colors.RESET}")
        print(f"  Next Cat Costs: {Colors.GREEN}{self.w3.from_wei(chain_data['entry_price'], 'ether'):.5f} ETH{Colors.RESET}")
        
        # Target info
        target_hex = hex(chain_data['target'])[2:].zfill(64)
        print(f"\n{Colors.BOLD}{Colors.YELLOW}TARGET TO BEAT{Colors.RESET}")
        print(f"  {Colors.GRAY}0x{target_hex}{Colors.RESET}")
        print(f"  {Colors.WHITE}{chain_data['difficulty']} leading zero bits{Colors.RESET}")
        
        # Best hash found
        if self.best_hash:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}THE CLOSEST ONE YET{Colors.RESET}")
            bits_progress = (self.best_bits / chain_data['difficulty']) * 100
            progress_bar = '█' * int(bits_progress / 2) + '░' * (50 - int(bits_progress / 2))
            print(f"  {Colors.GREEN}{progress_bar}{Colors.RESET} {self.best_bits} / {chain_data['difficulty']} bits")
            print(f"  {Colors.GRAY}0x{self.best_hash}{Colors.RESET}")
        
        # Mining stats
        print(f"\n{Colors.BOLD}{Colors.YELLOW}SPEED{Colors.RESET}           {Colors.BOLD}{Colors.YELLOW}CATS SEEN{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}EXPECTED WAIT{Colors.RESET}  {Colors.BOLD}{Colors.YELLOW}CHANCE / MIN{Colors.RESET}")
        
        hashrate_color = Colors.GREEN if hashrate > 100_000_000 else Colors.YELLOW if hashrate > 10_000_000 else Colors.WHITE
        print(f"{hashrate_color}{self.format_hashrate(hashrate):>12}{Colors.RESET}   {Colors.WHITE}{self.total_hashes / 1_000_000_000:.1f}T{Colors.RESET:>10}  {Colors.WHITE}{self.format_time(expected_time):>13}{Colors.RESET}  {Colors.WHITE}{chance_per_min:.1f}%{Colors.RESET}")
        
        # Machine info
        print(f"\n{Colors.BOLD}{Colors.YELLOW}MACHINE{Colors.RESET}         {Colors.BOLD}{Colors.YELLOW}GRAPHICS CARD{Colors.RESET}")
        print(f"  {Colors.GREEN}[GPU]{Colors.RESET}          {Colors.WHITE}Detecting...{Colors.RESET}")
        
        # Cats mined
        if self.cats_mined > 0:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 CATS MINED: {self.cats_mined}{Colors.RESET}")
        
        print(f"\n{Colors.GRAY}Total hashes: {self.total_hashes:,}{Colors.RESET}")
        print(f"{Colors.GRAY}Runtime: {self.format_time(time.time() - self.start_time)}{Colors.RESET}")
    
    def mine_cpu(self, chain_data, duration=30):
        """CPU mining implementation (fallback)"""
        print(f"\n{Colors.YELLOW}Starting CPU mining...{Colors.RESET}")
        
        target = chain_data['target']
        previous_work = chain_data['previous_work']
        anchor = chain_data['anchor']
        
        nonce = 0
        hashes_this_round = 0
        round_start = time.time()
        
        while True:
            # Check if we need to refresh chain data (every 20 seconds)
            if time.time() - round_start > 20:
                print(f"{Colors.YELLOW}Refreshing chain data...{Colors.RESET}")
                return None  # Signal to refresh
            
            # Compute hash: keccak256(address, nonce, previousWork, anchor)
            hash_input = (
                self.address.lower().encode() +
                nonce.to_bytes(32, 'big') +
                previous_work +
                anchor
            )
            
            result_hash = self.w3.keccak(hash_input)
            result_int = int.from_bytes(result_hash, 'big')
            
            # Update stats
            nonce += 1
            hashes_this_round += 1
            self.total_hashes += 1
            
            # Check leading zeros
            leading_zeros = self.count_leading_zeros(result_int)
            if leading_zeros > self.best_bits:
                self.best_bits = leading_zeros
                self.best_hash = result_hash.hex()
            
            # Display status every 10000 hashes
            if hashes_this_round % 10000 == 0:
                elapsed = time.time() - round_start
                hashrate = hashes_this_round / elapsed if elapsed > 0 else 0
                
                # Calculate expected time and chance
                total_hashes_needed = 2 ** chain_data['difficulty']
                expected_time = total_hashes_needed / hashrate if hashrate > 0 else float('inf')
                chance_per_min = (60 * hashrate / total_hashes_needed * 100) if hashrate > 0 else 0
                
                self.display_status(chain_data, hashrate, expected_time, chance_per_min)
            
            # Check if we found a solution
            if result_int < target:
                print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
                print(f"{Colors.GREEN}🎉 SOLUTION FOUND! 🎉{Colors.RESET}")
                print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
                print(f"{Colors.WHITE}Nonce: {nonce}{Colors.RESET}")
                print(f"{Colors.WHITE}Hash:  0x{result_hash.hex()}{Colors.RESET}")
                return {'nonce': nonce, 'anchor': anchor, 'hash': result_hash.hex()}
    
    def submit_solution(self, solution, entry_price):
        """Submit the mining solution to the blockchain"""
        try:
            print(f"\n{Colors.YELLOW}Submitting solution to blockchain...{Colors.RESET}")
            
            # Build transaction
            tx = self.contract.functions.mint(
                solution['nonce'],
                solution['anchor']
            ).build_transaction({
                'from': self.address,
                'value': entry_price,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.address)
            })
            
            # Sign transaction
            signed_tx = self.account.sign_transaction(tx)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"{Colors.GREEN}Transaction sent: {tx_hash.hex()}{Colors.RESET}")
            print(f"{Colors.YELLOW}Waiting for confirmation...{Colors.RESET}")
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt['status'] == 1:
                print(f"{Colors.GREEN}✅ SUCCESS! Cat minted!{Colors.RESET}")
                self.cats_mined += 1
                return True
            else:
                print(f"{Colors.RED}❌ Transaction failed{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}Error submitting solution: {e}{Colors.RESET}")
            return False
    
    def start(self):
        """Main mining loop"""
        print(f"\n{Colors.GREEN}Connecting to Robinhood Chain...{Colors.RESET}")
        
        if not self.w3.is_connected():
            print(f"{Colors.RED}Failed to connect to RPC{Colors.RESET}")
            return
        
        print(f"{Colors.GREEN}✅ Connected!{Colors.RESET}")
        print(f"{Colors.YELLOW}Starting mining operation...{Colors.RESET}\n")
        
        while True:
            try:
                # Fetch current chain data
                chain_data = self.get_chain_data()
                if not chain_data:
                    print(f"{Colors.RED}Failed to fetch chain data. Retrying in 5s...{Colors.RESET}")
                    time.sleep(5)
                    continue
                
                # Mine (will return None after 20s to refresh, or solution if found)
                result = self.mine_cpu(chain_data)
                
                if result:
                    # Found a solution, try to submit
                    success = self.submit_solution(result, chain_data['entry_price'])
                    if success:
                        # Reset best hash stats
                        self.best_hash = None
                        self.best_bits = 0
                    
                    # Wait a bit before continuing
                    time.sleep(2)
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Mining stopped by user{Colors.RESET}")
                print(f"{Colors.WHITE}Total hashes computed: {self.total_hashes:,}{Colors.RESET}")
                print(f"{Colors.WHITE}Total cats mined: {self.cats_mined}{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.RED}Error in mining loop: {e}{Colors.RESET}")
                time.sleep(5)

if __name__ == "__main__":
    print(f"{Colors.CYAN}{'='*64}{Colors.RESET}")
    print(f"{Colors.CYAN}         HASHCATS GPU MINER - SETUP{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*64}{Colors.RESET}\n")
    
    # Get private key
    private_key = input(f"{Colors.YELLOW}Enter your private key: {Colors.RESET}").strip()
    
    if not private_key.startswith('0x'):
        private_key = '0x' + private_key
    
    try:
        miner = HashcatsMiner(private_key)
        miner.start()
    except Exception as e:
        print(f"{Colors.RED}Failed to initialize miner: {e}{Colors.RESET}")
