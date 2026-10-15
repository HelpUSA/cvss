#!/usr/bin/env python3
"""Inspect live production deployment at https://cvss.helpusbr.com."""
import urllib.request
import ssl
import re
import json

def inspect_production():
    url = "https://cvss.helpusbr.com"
    print(f"Inspecting production at {url}...")
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            headers = dict(resp.getheaders())
            html = resp.read().decode("utf-8", errors="ignore")
            
            print(f"HTTP Status: {resp.status}")
            print("Relevant Headers:")
            for k, v in headers.items():
                if any(x in k.lower() for x in ["vercel", "server", "etag", "cache", "deploy", "git"]):
                    print(f"  {k}: {v}")
            
            legacy_terms = [
                "AI Watcher",
                "Gate de Homologação Humana",
                "Aprovação HITL",
                "Especialista obrigatório",
                "SuperAdmin Master como gate de score",
                "AI calcula CVSS",
                "expert review",
                "expert validation",
                "especialista"
            ]
            
            print("\nLegacy Terms Scan:")
            found_any = False
            for term in legacy_terms:
                count = len(re.findall(re.escape(term), html, re.IGNORECASE))
                print(f"  {term}: {count}")
                if count > 0:
                    found_any = True
            
            title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            print(f"\nTitle: {title.group(1) if title else 'None'}")
            
            # Check meta or script tags for build/commit info
            build_ids = re.findall(r'"buildId":"([^"]+)"', html)
            if build_ids:
                print(f"Next.js buildId: {build_ids[0]}")
            
            # Check additional routes
            for path in ["/demo", "/login", "/app"]:
                suburl = f"{url}{path}"
                try:
                    subreq = urllib.request.Request(suburl, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(subreq, context=ctx, timeout=10) as subresp:
                        subhtml = subresp.read().decode("utf-8", errors="ignore")
                        subtitle = re.search(r"<title>(.*?)</title>", subhtml, re.IGNORECASE)
                        print(f"\nRoute {path}: Status {subresp.status}, Title: {subtitle.group(1) if subtitle else 'None'}")
                except Exception as sub_err:
                    print(f"\nRoute {path}: Error {sub_err}")
                    
    except Exception as e:
        print(f"Error inspecting {url}: {e}")

if __name__ == "__main__":
    inspect_production()
