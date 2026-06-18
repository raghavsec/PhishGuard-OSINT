# PhishGuard-OSINT
OSINT-powered phishing domain scanner with WHOIS analysis, threat scoring, and typosquatting detection.

A Python-based OSINT and phishing domain investigation framework designed to assist security researchers, SOC analysts, blue teams, and cybercrime investigators in identifying suspicious domains, phishing infrastructure, and typosquatting attacks.

The tool performs domain intelligence gathering, WHOIS analysis, IP resolution, geolocation lookup, threat scoring, and proactive brand impersonation detection.

---

## Features

### Single URL Investigation

* Domain extraction and normalization
* WHOIS information retrieval
* Domain age analysis
* DNS resolution
* IP address lookup
* Hosting provider identification
* Geolocation tracking
* Automated threat scoring
* Takedown email generation for suspicious domains

### Brand Typosquatting Scanner

* Generates 70+ domain permutations
* Character omission attacks
* Character duplication attacks
* Homograph-style substitutions
* Phishing keyword combinations
* TLD swapping detection
* Active infrastructure identification
* Automated threat ranking

### Threat Intelligence Engine

Risk scoring based on:

* Lookalike domain patterns
* Suspicious phishing keywords
* Newly registered domains
* Hidden WHOIS information
* Missing registration data
* Domain reputation indicators

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/phishing-domain-intelligence-tool.git
cd phishing-domain-intelligence-tool
```

### Install Dependencies

```bash
pip install python-whois requests pandas
```

---

## Usage

Run the tool:

```bash
python phishing_intel.py
```

Main Menu:

```text
1. Single URL Investigation
2. Proactive Brand Typosquatting Scanner
3. Exit
```

---

## Example Investigation

Input:

```text
instagram-login-security.com
```

Output:

```text
Threat Score: 90/100
IP Address: xxx.xxx.xxx.xxx
Hosting Provider: Example ISP
Location: Country, City

Analysis:
- Brand Lookalike Pattern
- Suspicious Keywords Detected
- Extremely New Domain
```

---

## Generated Threat Intelligence

The tool collects:

* Domain Name
* Registration Details
* Creation Date
* Domain Age
* IP Address
* Hosting ISP
* Country
* City
* Threat Score
* Risk Indicators

---

## Project Structure

```text
project/
│
├── phishing_intel.py
├── requirements.txt
└── README.md
```

---

## Use Cases

* Phishing Investigation
* Brand Protection
* Typosquatting Detection
* Threat Hunting
* SOC Monitoring
* Cybercrime Analysis
* Security Research
* Incident Response

---

## Disclaimer

This project is intended solely for:

* Educational Purposes
* Security Research
* Threat Intelligence
* Defensive Security Operations

Users are responsible for complying with all applicable laws and regulations. The author is not responsible for misuse of this software.

---

## Author

Raghav Upadhyay

B.Tech Student | Cybersecurity Enthusiast

LinkedIn:
https://linkedin.com/in/raghav-upadhyay-b78424414

---

## License

MIT License
