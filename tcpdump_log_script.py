import subprocess
from datetime import datetime

# Tcpdump komutunu tanımla (Sürekli çalışması için -l seçeneği eklenir)
command = ["sudo", "tcpdump", "-i", "ens160", "-A", "-l", "port", "8083"]

# Çıktının yazılacağı dosyanın adı (Log amaçlı kullanım için)
log_file = "tcpdump_port_8083_log.txt"

# tcpdump komutunu çalıştır ve çıktıyı yakala
with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, text=True) as proc, open(log_file, "a") as file:
    print(f"tcpdump başlatıldı, port 8083 üzerinden gelen veriler {log_file} dosyasına ekleniyor...")
    
    try:
        # Çıktıyı satır satır oku
        for line in proc.stdout:
            # Her satır için zaman damgası ekle
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Zaman damgası ile birlikte dosyaya yaz (append modu ile)
            file.write(f"{timestamp} {line}")
            file.flush()
    except KeyboardInterrupt:
        # Kullanıcı tarafından kesintiye uğratıldığında tcpdump'u durdur
        print("tcpdump durduruluyor...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("tcpdump başarıyla durduruldu.")

# Not: Bu kodu çalıştırmak için Python 3'ün yüklü olması ve script'in sudo yetkisiyle çalıştırılması gerekir.