from urllib.parse import urlparse
import re


FEATURE_COLUMNS = [
    "length_url",
    "length_hostname",
    "ip",
    "nb_dots",
    "nb_hyphens",
    "nb_at",
    "nb_qm",
    "nb_and",
    "nb_eq",
    "nb_slash",
    "nb_colon",
    "nb_www",
    "nb_com",
    "ratio_digits_url",
    "ratio_digits_host",
    "nb_subdomains",
    "prefix_suffix",
    "shortening_service",
    "phish_hints",
    "suspecious_tld",
]


def _digit_ratio(text: str) -> float:
    if not text:
        return 0.0
    digits = sum(ch.isdigit() for ch in text)
    return digits / len(text)


def _words(text: str) -> list[str]:
    return [w for w in re.split(r"\W+", text.lower()) if w]


def extract_url_features(url: str) -> dict:
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path = parsed.path.lower()
    full = url.lower()

    all_words = _words(full)
    host_words = _words(hostname)
    path_words = _words(path)

    suspicious_words = [
        "login", "secure", "verify", "account", "bank",
        "update", "password", "confirm", "signin", "wallet"
    ]

    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly", "is.gd"]
    suspicious_tlds = [".xyz", ".top", ".tk", ".ml", ".ga", ".cf"]

    features = {col: 0 for col in FEATURE_COLUMNS}

    features["length_url"] = len(url)
    features["length_hostname"] = len(hostname)
    features["ip"] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) else 0

    features["nb_dots"] = full.count(".")
    features["nb_hyphens"] = full.count("-")
    features["nb_at"] = full.count("@")
    features["nb_qm"] = full.count("?")
    features["nb_and"] = full.count("&")
    features["nb_or"] = full.count("|")
    features["nb_eq"] = full.count("=")
    features["nb_underscore"] = full.count("_")
    features["nb_tilde"] = full.count("~")
    features["nb_percent"] = full.count("%")
    features["nb_slash"] = full.count("/")
    features["nb_star"] = full.count("*")
    features["nb_colon"] = full.count(":")
    features["nb_comma"] = full.count(",")
    features["nb_semicolumn"] = full.count(";")
    features["nb_dollar"] = full.count("$")
    features["nb_space"] = full.count(" ")
    features["nb_www"] = full.count("www")
    features["nb_com"] = full.count(".com")
    features["nb_dslash"] = full.count("//")

    features["http_in_path"] = 1 if "http" in path else 0
    features["https_token"] = 1 if "https" in hostname else 0

    features["ratio_digits_url"] = _digit_ratio(full)
    features["ratio_digits_host"] = _digit_ratio(hostname)

    try:
        features["port"] = 1 if parsed.port else 0
    except ValueError:
        features["port"] = 0

    features["nb_subdomains"] = max(hostname.count(".") - 1, 0)
    features["prefix_suffix"] = 1 if "-" in hostname else 0
    features["shortening_service"] = 1 if any(s in hostname for s in shorteners) else 0

    features["length_words_raw"] = len(all_words)
    features["char_repeat"] = max([full.count(c) for c in set(full)] or [0])

    features["shortest_words_raw"] = min([len(w) for w in all_words] or [0])
    features["shortest_word_host"] = min([len(w) for w in host_words] or [0])
    features["shortest_word_path"] = min([len(w) for w in path_words] or [0])

    features["longest_words_raw"] = max([len(w) for w in all_words] or [0])
    features["longest_word_host"] = max([len(w) for w in host_words] or [0])
    features["longest_word_path"] = max([len(w) for w in path_words] or [0])

    features["avg_words_raw"] = sum(len(w) for w in all_words) / len(all_words) if all_words else 0
    features["avg_word_host"] = sum(len(w) for w in host_words) / len(host_words) if host_words else 0
    features["avg_word_path"] = sum(len(w) for w in path_words) / len(path_words) if path_words else 0

    features["phish_hints"] = sum(1 for w in suspicious_words if w in full)
    features["suspecious_tld"] = 1 if any(tld in hostname for tld in suspicious_tlds) else 0

    return features