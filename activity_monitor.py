import psutil

def get_process_info(ip: str) -> list:
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters']):
        try:
            for conn in psutil.net_connections():
                if conn.laddr.ip == ip:
                    if conn.pid == proc.pid:
                        process_info.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent'],
                            'read_bytes': conn.info.get('rbytes', 0),
                            'write_bytes': conn.info.get('wbytes', 0)
                        })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return process_info
