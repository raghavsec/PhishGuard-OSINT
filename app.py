import whois
import requests
import socket
from urllib.parse import urlparse
import datetime
import pandas as pd
import time

# ----------------------------
# CORE OSINT FUNCTIONS (Domain, IP aur Location nikalne ke liye)
# ----------------------------

def extract_domain(url_input):
    # URL se faltu cheezein hatakar clean domain nikalna
    url_input = url_input.strip()
    if not url_input.startswith(('http://', 'https://')):
        url_text = 'http://' + url_input
    else:
        url_text = url_input
    try:
        parsed_url = urlparse(url_text)
        domain = parsed_url.netloc
        if ':' in domain: domain = domain.split(':')[0]
        if domain.startswith('www.'): domain = domain[4:]
        return domain
    except Exception:
        return url_input

def get_ip_and_geo(domain):
    # Domain ka IP address aur hosting ISP track karna
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,city,isp", timeout=4)
        if response.status_code == 200:
            return ip_address, response.json()
        return ip_address, {"status": "fail"}
    except socket.gaierror:
        return None, {"status": "fail", "message": "Not Active / No IP"}
    except Exception:
        return None, {"status": "fail"}

def safe_parse_date(date_field):
    # WHOIS date format ko sahi se parse karna bina error ke
    if isinstance(date_field, list): date_field = date_field[0]
    if isinstance(date_field, datetime.datetime):
        if date_field.tzinfo is not None:
            date_field = date_field.replace(tzinfo=None)
        return date_field
    return None

# ----------------------------
# HIGH-VOLUME TYPOSQUATTING ENGINE (70-100+ Fake Domains Banane Ke Liye)
# ----------------------------
def generate_typo_variations(base_domain):
    base_domain = base_domain.lower()
    parts = base_domain.split('.')
    if len(parts) < 2:
        return []
    
    name = parts[0]
    ext = ".".join(parts[1:])
    variations = set()

    # 1. Aksharon ko double karna
    for i in range(len(name)):
        variations.add(f"{name[:i]}{name[i]}{name[i]}{name[i+1:]}.{ext}")
    
    # 2. Aksharon ko chhod dena
    for i in range(len(name)):
        variations.add(f"{name[:i]}{name[i+1:]}.{ext}")

    # 3. Phishing keywords ki mega list mix karna
    phishing_keywords = [
        'login', 'verify', 'secure', 'helpdesk', 'support', 'account-update',
        'portal', 'signin', 'admin', 'kyc', 'banking', 'rewards', 'free', 
        'online', 'office', 'safety', 'security', 'service', 'web'
    ]
    for kw in phishing_keywords:
        variations.add(f"{name}-{kw}.{ext}")
        variations.add(f"{kw}-{name}.{ext}")
        variations.add(f"{name}{kw}.{ext}")

    # 4. Visual characters badalna (jaise o ko 0, i ko 1 banana)
    replacements = {'o': '0', 'i': '1', 'l': '1', 'e': '3', 'a': '4', 's': '5'}
    for char, repl in replacements.items():
        if char in name:
            alt_name = name.replace(char, repl)
            variations.add(f"{alt_name}.{ext}")
            variations.add(f"{alt_name}-login.{ext}")

    # 5. Fake aur saste domain extensions mix karna (TLD Swapping)
    fake_extensions = ['xyz', 'top', 'site', 'online', 'club', 'cc', 'net', 'co']
    for f_ext in fake_extensions:
        if f_ext != ext:
            variations.add(f"{name}.{f_ext}")
            variations.add(f"{name}-login.{f_ext}")
            variations.add(f"{name}-secure.{f_ext}")

    variations.discard(base_domain)
    return list(variations)

# SMART RISK ENGINE (Threat Score calculate karne ke liye)
def quick_analyze(domain, is_lookalike=False):
    score = 0
    reasons = []
    
    if is_lookalike:
        score += 30
        reasons.append("Brand Lookalike Pattern")
        
    keywords = ['login', 'verify', 'secure', 'update', 'kyc', 'banking', 'support', 'helpdesk', 'signin', 'account']
    if any(kw in domain.lower() for kw in keywords):
        score += 40
        reasons.append("Suspicious Keywords Detected")
    
    try:
        w = whois.whois(domain)
        if w.domain_name:
            c_date = safe_parse_date(w.get('creation_date'))
            if c_date:
                age = (datetime.datetime.now() - c_date).days
                if age < 90:
                    score += 40
                    reasons.append(f"Extremely New Domain ({age} days old)")
                else:
                    reasons.append(f"Established Trusted Domain ({age} days old)")
            else:
                score += 20
                reasons.append("Registration Date Hidden/Unclear")
        else:
            score += 20
            reasons.append("Missing Registry Data")
    except Exception:
        score += 20
        reasons.append("WHOIS Lookup Failed / Privacy Hidden")
        w = None

    if score == 0 and not reasons:
        reasons.append("Clean Domain Record")

    return min(score, 100), " | ".join(reasons), w

# ----------------------------
# INTERACTIVE CMD CLI MENU SYSTEM
# ----------------------------

def main_menu():
    while True:
        print("\n=======================================================")
        print("      AUTOMATED PHISHING DOMAIN TAKEDOWN ASSISTANT     ")
        print("              [ Cyber Cell CLI Dashboard ]             ")
        print("=======================================================")
        print("1. Single URL Investigation")
        print("2. Proactive Brand Typosquatting Scanner")
        print("3. Exit/Bahar Niklein")
        print("-------------------------------------------------------")
        
        choice = input("Apna option select karein (1, 2 ya 3): ").strip()
        
        if choice == '1':
            print("\n--- SINGLE URL INVESTIGATION ---")
            target_url = input("Suspicious URL entered karein: ").strip()
            if target_url:
                cleaned_domain = extract_domain(target_url)
                print(f"\n[SCANNING] `{cleaned_domain}` ki infrastructure check ho rahi hai...")
                
                ip, geo = get_ip_and_geo(cleaned_domain)
                score, reasons, whois_data = quick_analyze(cleaned_domain, is_lookalike=False)
                
                print("\n------------------------------")
                print("📊 SCAN RESULTS & THREAT INTEL")
                print("------------------------------")
                print(f"-> Threat Risk Score   : {score}/100")
                print(f"-> Resolved IP Address : {ip if ip else 'Not Active'}")
                print(f"-> Hosting Provider    : {geo.get('isp', 'N/A') if ip else 'N/A'}")
                print(f"-> Server Location     : {geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')}")
                print(f"-> Analysis Markers    : {reasons}")
                print("------------------------------")
                
                if score >= 50 and ip:
                    print("\n[ALERT] High Risk Phishing Evidence Found! Generating Takedown Request...")
                    takedown_email = f"""
Subject: URGENT: Phishing Website Takedown Request - {cleaned_domain}

Dear Abuse Team / Hosting Security Department,

This is an official automated security alert regarding a phishing/impersonation infrastructure hosted on your network. 

We request the immediate suspension/takedown of the following malicious domain:
- Malicious Domain: {cleaned_domain}
- Resolved Server IP: {ip}
- Hosting Provider (ISP): {geo.get('isp', 'Unknown')}
- Incident Type: Phishing & Cyber Fraud Impersonation

Regards,
Cyber Cell Incident Response Team
"""
                    print("\n=== GENERATED TAKEDOWN EMAIL (Niche diye text ko copy karein) ===")
                    print(takedown_email)
                    print("==================================================================")
                elif not ip:
                    print("\n[INFO] Yeh domain abhi internet par active nahi hai.")
                else:
                    print(f"\n[SAFE] `{cleaned_domain}` poori tarah se safe lag raha hai.")
                    
        elif choice == '2':
            print("\n--- PROACTIVE BRAND TYPOSQUATTING SCANNER ---")
            brand_domain = input("Official Target Domain dalein (e.g., instagram.com): ").strip()
            if brand_domain:
                cleaned_brand = extract_domain(brand_domain)
                print(f"\n[PROCESSING] Permutations generate ho rahe hain...")
                
                possible_phish_domains = generate_typo_variations(cleaned_brand)
                print(f"[INFO] Total {len(possible_phish_domains)} advanced variations check ho rahe hain. Kripya wait karein...\n")
                
                active_threats = []
                total_domains = len(possible_phish_domains)
                
                for index, test_domain in enumerate(possible_phish_domains):
                    # Progress status print karne ke liye
                    print(f"Scanning ({index + 1}/{total_domains}): {test_domain}", end="\r")
                    
                    ip, geo = get_ip_and_geo(test_domain)
                    if ip: 
                        score, reasons, w_data = quick_analyze(test_domain, is_lookalike=True)
                        if score >= 50: 
                            active_threats.append({
                                "Suspicious Domain": test_domain,
                                "Threat Score": f"{score}/100",
                                "Resolved IP": ip,
                                "ISP": geo.get('isp', 'Unknown')
                            })
                    time.sleep(0.01)
                
                # Nayi line par parinaam dikhane ke liye clearing row
                print(" " * 60, end="\r") 
                print("\n-------------------------------------------")
                print("🚨 LIVE PHISHING & IMPERSONATION THREATS FOUND")
                print("-------------------------------------------")
                
                if active_threats:
                    # Pandas dataframe ko cleanly plain text table me dikhane ka logic
                    df = pd.DataFrame(active_threats)
                    print(df.to_string(index=False))
                    print(f"\n[ALERT] Internet par {len(active_threats)} active lookalike threat infrastructure live mile hain!")
                else:
                    print(f"[CLEAN] Sarei variations clean hain! `{cleaned_brand}` ke liye koi active threat nahi mila.")
                    
        elif choice == '3':
            print("\nExiting... Cyber Cell Assistant Tool band ho raha hai. Jai Hind!")
            break
        else:
            print("\n[ERROR] Invalid option! Kripya sahi number chunna (1, 2, ya 3).")

if __name__ == "__main__":
    main_menu()