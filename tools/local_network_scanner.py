"""
HelpUS Native Local Environment & Network Scanner.
Discovers local network interfaces, probes hosts on the local subnet (ARP / TCP ping),
identifies open service ports (HTTP, DBs, SSH, RDP), classifies asset roles,
and inspects active local application services.
"""
from __future__ import annotations

import concurrent.futures
import ipaddress
import json
import socket
import sys
import time
from typing import Any, Dict, List, Optional

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    80: "HTTP Web",
    443: "HTTPS Web",
    1433: "MSSQL Database",
    3000: "Next.js / Node App",
    3306: "MySQL Database",
    5432: "PostgreSQL Database",
    6379: "Redis Cache",
    8000: "FastAPI / Python Service",
    8080: "HTTP Alternate",
}


def get_local_ip() -> str:
    """Detects the primary active local network IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not send real packets, just determines routing interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def scan_port(host: str, port: int, timeout: float = 0.3) -> bool:
    """Fast non-blocking socket connect test."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        res = s.connect_ex((host, port))
        return res == 0
    except Exception:
        return False
    finally:
        s.close()


def scan_host(host_ip: str, ports_to_check: Optional[List[int]] = None) -> Optional[Dict[str, Any]]:
    """Scans specific ports on a target host to detect active services."""
    ports_to_check = ports_to_check or list(COMMON_PORTS.keys())
    open_ports = []
    
    for port in ports_to_check:
        if scan_port(host_ip, port):
            open_ports.append({
                "port": port,
                "service": COMMON_PORTS.get(port, "Unknown Service")
            })

    if not open_ports and host_ip != "127.0.0.1":
        return None

    # Determine asset classification based on discovered ports
    port_nums = {p["port"] for p in open_ports}
    asset_role = "Estação de Trabalho / Host Genérico"
    pci_scope = False
    internet_exposed = False
    crit = "medium"

    if 5432 in port_nums or 3306 in port_nums or 1433 in port_nums:
        asset_role = "Servidor de Banco de Dados"
        pci_scope = True
        crit = "high"
    elif 80 in port_nums or 443 in port_nums or 3000 in port_nums or 8080 in port_nums:
        asset_role = "Servidor Web / Aplicação HelpUS"
        crit = "high"

    try:
        hostname = socket.gethostbyaddr(host_ip)[0]
    except Exception:
        hostname = "Desconhecido"

    return {
        "ip": host_ip,
        "hostname": hostname,
        "role": asset_role,
        "open_ports": open_ports,
        "evidence": {
            "network_segmented": host_ip.startswith("192.168.") or host_ip.startswith("10."),
            "internet_exposed": internet_exposed,
            "pci_in_scope": pci_scope,
            "business_criticality": crit,
            "high_availability": len(open_ports) > 2,
        }
    }


def scan_local_subnet(max_hosts: int = 15) -> Dict[str, Any]:
    """
    Scans the immediate neighborhood of the local IPv4 subnet.
    Runs fast multithreaded discovery.
    """
    local_ip = get_local_ip()
    network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)

    discovered_assets = []

    # Always scan localhost first
    localhost_asset = scan_host("127.0.0.1", [80, 443, 3000, 5432, 8000, 8080])
    if localhost_asset:
        localhost_asset["role"] = "Máquina Local do Operador (WagnerPredator)"
        discovered_assets.append(localhost_asset)

    # Scan a sample slice around the local IP
    ip_int = int(ipaddress.IPv4Address(local_ip))
    candidates = []
    
    # Check gateway (.1) and nearby neighbors (+/- 5 IPs)
    gw = str(network.network_address + 1)
    if gw != local_ip:
        candidates.append(gw)
        
    for offset in range(-5, 6):
        try:
            cand = str(ipaddress.IPv4Address(ip_int + offset))
            if cand not in candidates and cand != "127.0.0.1":
                candidates.append(cand)
        except Exception:
            pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda ip: scan_host(ip, [80, 443, 3000, 8080, 5432]), candidates)
        for res in results:
            if res:
                discovered_assets.append(res)

    return {
        "scan_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "local_ip": local_ip,
        "subnet": str(network),
        "total_discovered": len(discovered_assets),
        "assets": discovered_assets,
    }


if __name__ == "__main__":
    print(f"[*] Iniciando varredura nativa da rede local...")
    data = scan_local_subnet()
    print(json.dumps(data, indent=2, ensure_ascii=False))
