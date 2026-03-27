"""KAP.org.tr'den fiili dolasim oranlarini cek"""
import requests
import re

def fetch_kap_fdo():
    """KAP'tan fiili dolasim oranlarini cek, dict dondur {ticker: fdo%}"""
    url = "https://kap.org.tr/tr/tumKalemler/kpy41_acc5_fiili_dolasimdaki_pay"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', resp.text, re.DOTALL)
    big = [s for s in scripts if len(s) > 100000][0]

    # Escape format: ldren\\":\\"THYAO\\"
    # Unescape edip parse edelim
    unescaped = big.replace('\\"', '"')

    # Simdi normal JSON-like pattern
    all_ch = re.findall(r'"children":"([^"]+)"', unescaped)

    results = {}
    i = 0
    while i < len(all_ch) - 2:
        val = all_ch[i]
        # 3-6 buyuk harf = ticker
        if re.match(r'^[A-Z]{3,6}$', val) and val not in ('HTML', 'HEAD', 'BODY'):
            fdo_str = all_ch[i + 2]  # 3. kolon = FDO%
            try:
                fdo = float(fdo_str.replace('.', '').replace(',', '.'))
                if 0 < fdo <= 100:
                    results[val] = round(fdo, 2)
            except ValueError:
                pass
            i += 3
        else:
            i += 1

    return results


if __name__ == "__main__":
    data = fetch_kap_fdo()
    print(f"{len(data)} hisse FDO verisi")
    for t in ["THYAO", "GARAN", "AKBNK", "EREGL", "PEKGY", "BJKAS"]:
        print(f"  {t}: %{data.get(t, 'YOK')}")
