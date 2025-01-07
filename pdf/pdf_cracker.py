import itertools
import pikepdf
from tqdm import tqdm
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield "".join(password) 
        
def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as file:
        for line in file:
            yield line.strip() 

def try_passwords(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password) as pdf:
            print(f"[+] Password found: {password}")
            return password
    except pikepdf._core.PasswordError:
        return None

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    with tqdm(total=total_passwords, unit='passwords') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_passwords = {executor.submit(try_passwords, pdf_file, password): password for password in passwords}
            for future in as_completed(future_to_passwords):
                password = future_to_passwords[future] 
                if future.result():  
                    pbar.close()  
                    return future.result()
                pbar.update(1)  
    print('Unable to decrypt PDF')
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt PDF using password cracking')
    parser.add_argument('pdf_file', help='Path to the PDF file')
    parser.add_argument('-w' '--wordlist', help='Path to the wordlist file', default=None)
    parser.add_argument('-g', '--generate' , action='store_true', help='Generate passwords')
    parser.add_argument('-min', '--min-length', type=int, default=1, help='Minimum length of the password')
    parser.add_argument('-max', '--max-length', type=int, default=3, help='Maximum length of the password')
    parser.add_argument('-c', '--charset',type=str, default=string.digits + string.ascii_letters + string.punctuation, help='Characters to use for password generation')
    parser.add_argument('--max_workers', type=int, default=4, help='Number of workers for password cracking (default: 4)')

    args = parser.parse_args()

    if args.generate:
        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = sum(1 for _ in generate_passwords(args.charset, args.min_length, args.max_length))
    elif args.wordlist:
        passwords = load_wordlist(args.wordlist)
        total_passwords = sum(1 for _ in load_wordlist(args.wordlist))
    else:
        print('Either -g or -w flag must be provided')
        exit(1)
    
    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)
    if decrypted_password:
        print(f'[+] Password found: {decrypted_password} 😊')
        exit(0)
    else:
        print('[-] Password not found😢')
        exit(1)