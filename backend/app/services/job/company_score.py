"""
Trusted companies receive a ranking bonus.

These values can grow over time as Upvanta learns
which employers consistently offer good jobs.
"""

TOP_COMPANIES = {

    # Big Tech
    "google": 25,
    "microsoft": 25,
    "apple": 24,
    "amazon": 24,
    "meta": 24,
    "netflix": 23,
    "openai": 25,
    "nvidia": 25,
    "tesla": 22,
    "intel": 20,
    "oracle": 20,
    "ibm": 20,
    "adobe": 22,
    "salesforce": 22,

    # AI
    "anthropic": 25,
    "hugging face": 24,
    "cohere": 23,
    "stability ai": 23,
    "databricks": 22,

    # Enterprise / SaaS
    "shopify": 23,
    "atlassian": 22,
    "github": 22,
    "stripe": 22,
    "spotify": 20,
    "uber": 20,
    "airbnb": 20,
    "dropbox": 18,

    # Finance
    "jpmorgan": 18,
    "goldman sachs": 18,
    "visa": 18,
    "mastercard": 18,
    "paypal": 18,

    # Consulting
    "accenture": 18,
    "deloitte": 18,
    "ey": 18,
    "kpmg": 18,
    "pwc": 18,

    # Remote-first
    "gitlab": 25,
    "automattic": 24,
    "zapier": 23,
    "doist": 23,
    "buffer": 22,

    # Job Platforms
    "linkedin": 15,
    "indeed": 10,

    # Energy
    "shell": 14,
    "chevron": 14,
    "exxonmobil": 14,

    # Consumer
    "unilever": 14,
    "nestle": 14,
    "pepsico": 14,
    "coca-cola": 14,

    # Manufacturing
    "siemens": 15,
    "bosch": 15,

    # African Tech
    "flutterwave": 18,
    "paystack": 18,
    "andela": 18,
    "interswitch": 17,
    "moniepoint": 17,
}