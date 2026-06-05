import browser_cookie3

def get_auto_cookies():
    try:
        
        cks = browser_cookie3.chrome(domain_name='funpay.com') or browser_cookie3.firefox(domain_name='funpay.com') or browser_cookie3.edge(domain_name='funpay.com') or browser_cookie3.yandex(domain_name='funpay.com')
        
        return "; ".join(f"{c.name}={c.value}" for c in cks)
    except Exception:
        return None