import os
import sys
import base64
import zlib
import qrcode
from math import ceil

# ===== 配置 =====
CHUNK_SIZE = 2500   # 每张二维码最大 Base64 字符，保守容量
OUTPUT_DIR = "qr_output"
# =================

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def compress_and_b64(text):
    compressed = zlib.compress(text.encode("utf-8"))
    b64 = base64.b64encode(compressed).decode("ascii")
    return b64

def split_chunks(b64, size):
    return [b64[i:i+size] for i in range(0, len(b64), size)]

def make_qr(data, filename):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(filename)

def main():
    if len(sys.argv) < 2:
        print(f"用法: python {os.path.basename(sys.argv[0])} <输入文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    text = read_file(input_file)
    b64 = compress_and_b64(text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    chunks = split_chunks(b64, CHUNK_SIZE)
    total = len(chunks)
    width = len(str(total))

    index_lines = []

    for i, chunk in enumerate(chunks, start=1):
        header = f"{str(i).zfill(width)}/{str(total).zfill(width)}"
        payload = header + "\n" + chunk
        name = f"qr_{str(i).zfill(width)}.png"
        path = os.path.join(OUTPUT_DIR, name)

        make_qr(payload, path)
        index_lines.append(f"{header} -> {name}")
        print(f"生成 {path}")

    with open(os.path.join(OUTPUT_DIR, "index.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print(f"\n总共 {total} 张二维码，输出目录: {OUTPUT_DIR}")
    print("按编号顺序打开，每张扫码一次即可")

if __name__ == "__main__":
    main()
