#!/usr/bin/env python3
"""
Học phần: Tiền điện tử & Hợp đồng thông minh (ECO2432)
Lab 6: Phân tích dòng tiền ví và số dư lũy kế trong 90 ngày
Tuân thủ đầy đủ quy ước AGENTS.md và đặc tả SPEC.md.
Sử dụng thư viện chuẩn urllib.request để chạy độc lập không phụ thuộc pip.
Hỗ trợ Etherscan API v2 đa chuỗi (Sepolia chainid=11155111).
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone


def get_api_key() -> str:
    """
    Quy tắc AGENTS.md: Không ghi khóa API trong mã nguồn; đọc từ biến môi trường.
    """
    api_key = os.getenv("ETHERSCAN_API_KEY")
    return (api_key or "").strip()


def fetch_transactions(address: str, api_key: str, chain_id: int = 11155111, days: int = 90) -> list:
    """
    Lấy danh sách giao dịch từ Etherscan API v2 hợp nhất (hỗ trợ Sepolia testnet và Mainnet).
    Quy tắc AGENTS.md: Kiểm tra trạng thái phản hồi trước khi xử lý dữ liệu.
    """
    clean_addr = address.strip().lower()
    now_ts = int(time.time())
    start_ts = now_ts - (days * 86400)

    # Sử dụng Etherscan v2 API hợp nhất đa chuỗi
    base_url = "https://api.etherscan.io/v2/api"
    all_txs = []
    page = 1
    offset = 100

    print(f"[*] Đang lấy dữ liệu từ Etherscan v2 API (ChainID: {chain_id}) cho ví: {address}")
    print(f"[*] Phạm vi: {days} ngày gần nhất (tính từ {datetime.fromtimestamp(start_ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')})...")

    while True:
        query_url = (
            f"{base_url}?chainid={chain_id}"
            f"&module=account&action=txlist"
            f"&address={clean_addr}"
            f"&startblock=0&endblock=99999999"
            f"&page={page}&offset={offset}&sort=asc"
            f"&apikey={api_key}"
        )

        req = urllib.request.Request(query_url, headers={"User-Agent": "ECO2432-WalletAnalyzer/1.0"})

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    print(f"[LỖI] HTTP status: {response.status}. Không thể kết nối Etherscan.")
                    sys.exit(1)
                body = response.read().decode("utf-8")
                data = json.loads(body)
        except urllib.error.URLError as e:
            print(f"[LỖI] Lỗi kết nối mạng: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[LỖI] Không thể phân tích dữ liệu phản hồi: {e}")
            sys.exit(1)

        status = str(data.get("status", "0"))
        message = data.get("message", "")
        result = data.get("result", [])

        # Kiểm tra trạng thái nghiệp vụ từ API
        if status != "1":
            if message == "No transactions found" or "No transactions" in str(result):
                break  # Không có giao dịch nào
            else:
                print(f"[LỖI API] Etherscan phản hồi lỗi: {message} ({result})")
                print(">> Kiểm tra lại khóa API hoặc kết nối mạng.")
                sys.exit(1)

        if not isinstance(result, list) or len(result) == 0:
            break

        all_txs.extend(result)

        # Đã hết các trang phân trang
        if len(result) < offset:
            break

        page += 1
        time.sleep(0.25)  # Tránh chạm rate limit

    # Lọc giao dịch trong `days` ngày gần nhất
    recent_txs = [tx for tx in all_txs if int(tx.get("timeStamp", 0)) >= start_ts]
    print(f"[✓] Tổng giao dịch tải về: {len(all_txs)} | Giao dịch trong 90 ngày: {len(recent_txs)}")
    return recent_txs


def parse_and_calculate_cash_flow(address: str, tx_list: list) -> dict:
    """
    Quy tắc nghiệp vụ R1 - R6 từ SPEC.md:
    R1: to == address và thành công -> Dòng tiền vào (+value)
    R2, R3: from == address -> Dòng tiền ra (-value - gas_fee)
    R4: from == address và thất bại -> Dòng tiền ra (-gas_fee, value = 0)
    R5: Quy đổi wei sang ETH (chia cho 10^18)
    R6: Sắp xếp theo thời gian tăng dần, tính số dư lũy kế
    """
    target = address.strip().lower()
    sorted_txs = sorted(tx_list, key=lambda x: int(x.get("timeStamp", 0)))

    total_inflow = 0.0
    total_outflow = 0.0
    cumulative_balance = 0.0
    processed_rows = []

    for tx in sorted_txs:
        tx_from = tx.get("from", "").lower()
        tx_to = tx.get("to", "").lower()
        is_error = str(tx.get("isError", "0"))  # "0" = thành công, "1" = thất bại

        # R5: Quy đổi wei sang ETH trước khi hiển thị (AGENTS.md)
        val_eth = int(tx.get("value", 0)) / (10 ** 18)
        gas_used = int(tx.get("gasUsed", 0))
        gas_price = int(tx.get("gasPrice", 0))
        gas_fee_eth = (gas_used * gas_price) / (10 ** 18)

        timestamp = int(tx.get("timeStamp", 0))
        tx_time_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        tx_hash = tx.get("hash", "")

        tx_type = ""
        net_impact = 0.0

        if tx_to == target:
            # R1: Dòng tiền vào
            if is_error == "0":
                tx_type = "IN"
                net_impact = val_eth
                total_inflow += val_eth
            else:
                # Tiền gửi đến bị lỗi: người nhận không nhận được gì và không mất phí
                tx_type = "IN (FAILED)"
                net_impact = 0.0
        elif tx_from == target:
            # R2, R3, R4: Dòng tiền ra
            if is_error == "0":
                tx_type = "OUT"
                net_impact = -(val_eth + gas_fee_eth)
                total_outflow += (val_eth + gas_fee_eth)
            else:
                # R4: Thất bại vẫn mất phí gas
                tx_type = "OUT (FAILED)"
                net_impact = -gas_fee_eth
                total_outflow += gas_fee_eth
        else:
            continue

        cumulative_balance += net_impact
        processed_rows.append({
            "time": tx_time_str,
            "timestamp": timestamp,
            "hash": tx_hash,
            "type": tx_type,
            "value_eth": val_eth,
            "gas_fee_eth": gas_fee_eth,
            "net_impact": net_impact,
            "balance": cumulative_balance
        })

    return {
        "rows": processed_rows,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "net_flow": cumulative_balance
    }


def display_report(address: str, results: dict):
    """Hiển thị bảng dữ liệu và 3 chỉ số tổng hợp theo mục 4 SPEC.md"""
    rows = results["rows"]
    if not rows:
        print("\n" + "=" * 70)
        print(">> THÔNG BÁO: Vi khong co giao dich trong ky (90 ngày gần nhất).")
        print("=" * 70)
        return

    print("\n" + "=" * 105)
    print(f"BÁO CÁO DÒNG TIỀN VÍ: {address}")
    print("=" * 105)
    print(f"{'Thời gian (UTC)':<22} | {'Loại':<10} | {'Giá trị (ETH)':<14} | {'Phí Gas (ETH)':<14} | {'Biến động ròng':<16} | {'Lũy kế (ETH)':<14}")
    print("-" * 105)

    for r in rows:
        print(f"{r['time']:<22} | {r['type']:<10} | {r['value_eth']:<14.6f} | {r['gas_fee_eth']:<14.6f} | {r['net_impact']:<+16.6f} | {r['balance']:<14.6f}")

    print("-" * 105)
    print(f"[1] Tổng dòng tiền vào (Total Inflow)  : +{results['total_inflow']:.6f} ETH")
    print(f"[2] Tổng dòng tiền ra (Total Outflow) : -{results['total_outflow']:.6f} ETH (bao gồm phí gas)")
    print(f"[3] Chênh lệch số dư ròng trong kỳ    : {results['net_flow']:+.6f} ETH")
    print("=" * 105)


def plot_balance_chart(address: str, results: dict, output_image: str = "balance_chart.png"):
    """Vẽ biểu đồ đường biến động số dư lũy kế theo thời gian."""
    rows = results["rows"]
    if not rows:
        return

    try:
        import matplotlib.pyplot as plt
        times = [datetime.fromtimestamp(r["timestamp"], tz=timezone.utc) for r in rows]
        balances = [r["balance"] for r in rows]

        plt.figure(figsize=(11, 5.5))
        plt.plot(times, balances, marker='o', markersize=6, linestyle='-', color='#1a73e8', linewidth=2, label="Số dư ròng lũy kế (ETH)")
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)

        plt.title(f"Biểu đồ biến động số dư ví on-chain (90 ngày gần nhất)\n{address}", fontsize=11, pad=12)
        plt.xlabel("Thời gian (UTC)", fontsize=10)
        plt.ylabel("Số dư ròng lũy kế (ETH)", fontsize=10)
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend(loc="upper left")
        plt.tight_layout()

        plt.savefig(output_image, dpi=150)
        print(f"\n[✓] Đã tạo và lưu ảnh biểu đồ thành công: {output_image}")
    except ImportError:
        print("\n[LƯU Ý] Môi trường chưa cài đặt thư viện 'matplotlib'.")
        print("Để vẽ biểu đồ dạng ảnh PNG, hãy cài đặt bằng lệnh: pip3 install matplotlib")


def main():
    print("=== ECO2432 - CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ON-CHAIN ===")

    api_key = get_api_key()
    if not api_key:
        if len(sys.argv) > 2:
            api_key = sys.argv[2]
        else:
            api_key = input("Nhập Etherscan API Key (hoặc cấu hình ETHERSCAN_API_KEY): ").strip()

    if len(sys.argv) > 1:
        address = sys.argv[1]
    else:
        address = input("Nhập địa chỉ ví Ethereum (0x...): ").strip()

    if not address.startswith("0x") or len(address) != 42:
        print("[LỖI] Địa chỉ ví không đúng định dạng chuẩn 42 ký tự (0x...)!")
        sys.exit(1)

    # Mặc định sử dụng Sepolia testnet (11155111) cho học phần ECO2432
    chain_id = 11155111
    txs = fetch_transactions(address, api_key, chain_id=chain_id, days=90)
    results = parse_and_calculate_cash_flow(address, txs)
    display_report(address, results)
    plot_balance_chart(address, results)


if __name__ == "__main__":
    main()
