import re 

messages = [
    "❄️  DO4PZ2U9  ❄️\n 1000 | 0.1 DOGE\n💰 ~0.000033 / ~0.03284 (USDT)\n\n 📅 01-13-2025 08:03:41",
    "❄️  VUSA7CZ0  ❄️\n 1500 | 0.0002 BNB\n💰 ~0.000091 / ~0.136829 (USDT)\n\n 📅 01-13-2025 07:41:06",
    "FVUSA7CZ0F\n\n 📅 01-13-2025 07:41:13",
    "FW8LPTML"
]


def extract_code(text):
   
   
    pattern = r"[A-Z0-9]{8,}"
    matches = re.findall(pattern, text)
    return matches if matches else None

for msg in messages:
    codes = extract_code(msg)
    if codes:
        print(f"Extracted codes: {', '.join(codes)}")
    else:
        print("No code found in the message.")