#!/bin/bash

clear
echo "===== PMF Detector - Interface Selection ====="
echo

interfaces=$(iwconfig 2>/dev/null | grep 'IEEE 802.11' | cut -d ' ' -f1 | sort | uniq)

if [[ -z "$interfaces" ]]; then
    echo "Tidak ada interface wireless yang terdeteksi."
    exit 1
fi

echo "Daftar interface wireless:"
select iface in $interfaces; do
    if [[ -n "$iface" ]]; then
        echo "Interface dipilih: $iface"
        echo "$iface" > interface.txt
        break
    else
        echo "Pilihan tidak valid."
    fi
done

echo
echo "[+] Menjalankan FastAPI..."
uvicorn app.main:app --reload
