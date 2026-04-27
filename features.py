"""
features.py - Modul ekstraksi fitur URL untuk CyberShield ID

Mengekstrak fitur-fitur dari URL yang bisa dihitung secara real-time
tanpa perlu mengunduh konten halaman web.
"""

import re
import ipaddress
from urllib.parse import urlparse, unquote

# Daftar fitur yang digunakan model (harus konsisten antara training & prediksi)
FEATURE_COLUMNS = [
    'URLLength',
    'DomainLength',
    'IsDomainIP',
    'TLDLength',
    'NoOfSubDomain',
    'HasObfuscation',
    'NoOfObfuscatedChar',
    'ObfuscationRatio',
    'NoOfLettersInURL',
    'LetterRatioInURL',
    'NoOfDegitsInURL',
    'DegitRatioInURL',
    'NoOfEqualsInURL',
    'NoOfQMarkInURL',
    'NoOfAmpersandInURL',
    'NoOfOtherSpecialCharsInURL',
    'SpacialCharRatioInURL',
    'IsHTTPS',
]


def extract_features(url):
    """
    Ekstrak fitur-fitur dari sebuah URL string.

    Args:
        url (str): URL lengkap (mis. https://example.com/path?q=1)

    Returns:
        dict: Dictionary berisi fitur-fitur numerik dari URL.
    """
    # Pastikan URL punya scheme
    if '://' not in url:
        url = 'http://' + url

    parsed = urlparse(url)
    domain = parsed.netloc or ''

    # Hapus port jika ada (mis. example.com:8080)
    if ':' in domain:
        domain = domain.split(':')[0]

    # Ekstrak TLD
    domain_parts = domain.split('.')
    tld = domain_parts[-1] if len(domain_parts) > 1 else ''

    # ---- Hitung fitur-fitur ---- #

    # URLLength: panjang URL (dataset menghitung tanpa trailing slash, -1 dari len)
    url_clean = url.rstrip('/')
    url_length = len(url_clean) - 1  # sesuai pola dataset

    # DomainLength
    domain_length = len(domain)

    # IsDomainIP: 1 jika domain adalah alamat IP
    is_domain_ip = 0
    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        pass

    # TLDLength
    tld_length = len(tld)

    # NoOfSubDomain: jumlah subdomain (parts - 2 untuk domain.tld)
    no_of_subdomain = max(0, len(domain_parts) - 2)

    # Obfuscation: karakter yang di-encode (%XX)
    obfuscated_chars = re.findall(r'%[0-9a-fA-F]{2}', url)
    no_of_obfuscated_char = len(obfuscated_chars)
    has_obfuscation = 1 if no_of_obfuscated_char > 0 else 0
    obfuscation_ratio = no_of_obfuscated_char / url_length if url_length > 0 else 0

    # Hitung karakter di URL
    no_of_letters = sum(1 for c in url_clean if c.isalpha())
    letter_ratio = no_of_letters / url_length if url_length > 0 else 0

    no_of_digits = sum(1 for c in url_clean if c.isdigit())
    digit_ratio = no_of_digits / url_length if url_length > 0 else 0

    # Karakter spesial
    no_of_equals = url_clean.count('=')
    no_of_qmark = url_clean.count('?')
    no_of_ampersand = url_clean.count('&')

    # Karakter spesial lainnya (selain =, ?, &)
    standard_special = set('=?&')
    all_special = set('~`!@#$%^&*()_+-=[]{}|;:\'",.<>?/')
    other_special_chars = sum(
        1 for c in url_clean
        if c in all_special and c not in standard_special
    )

    total_special = no_of_equals + no_of_qmark + no_of_ampersand + other_special_chars
    special_char_ratio = total_special / url_length if url_length > 0 else 0

    # IsHTTPS
    is_https = 1 if parsed.scheme.lower() == 'https' else 0

    # Bangun dictionary fitur
    features = {
        'URLLength': url_length,
        'DomainLength': domain_length,
        'IsDomainIP': is_domain_ip,
        'TLDLength': tld_length,
        'NoOfSubDomain': no_of_subdomain,
        'HasObfuscation': has_obfuscation,
        'NoOfObfuscatedChar': no_of_obfuscated_char,
        'ObfuscationRatio': obfuscation_ratio,
        'NoOfLettersInURL': no_of_letters,
        'LetterRatioInURL': round(letter_ratio, 3),
        'NoOfDegitsInURL': no_of_digits,
        'DegitRatioInURL': round(digit_ratio, 3),
        'NoOfEqualsInURL': no_of_equals,
        'NoOfQMarkInURL': no_of_qmark,
        'NoOfAmpersandInURL': no_of_ampersand,
        'NoOfOtherSpecialCharsInURL': other_special_chars,
        'SpacialCharRatioInURL': round(special_char_ratio, 3),
        'IsHTTPS': is_https,
    }

    return features
