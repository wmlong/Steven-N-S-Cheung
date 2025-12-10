import os
import math
import qrcode

# ===== 配置区域 =====
INPUT_FILE = "mycode.py"     # 要导出的代码文件名
OUTPUT_DIR = "qr_output"     # 二维码图片输出目录
MAX_PAYLOAD = 700            # 每个二维码里放多少字符（含换行）
# ====================


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_text(text, max_payload):
    chunks = []
    length = len(text)
    for i in range(0, length, max_payload):
        chunks.append(text[i:i + max_payload])
    return chunks


def main():
    # 读取源码
    text = read_text(INPUT_FILE)

    # 切片
    chunks = split_text(text, MAX_PAYLOAD)
    total = len(chunks)
    width = len(str(total))  # 序号宽度，比如 10 片就是 2 位

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_lines = []

    for i, chunk in enumerate(chunks, start=1):
        # 序号头，例如 "001/010"
        header = f"{str(i).zfill(width)}/{str(total).zfill(width)}"
        payload = header + "\n" + chunk

        # 生成二维码
        qr = qrcode.QRCode(
            version=None,          # 自动选择合适版本
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image()

        filename = f"qr_{str(i).zfill(width)}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        img.save(filepath)

        index_lines.append(f"{header} -> {filename}")

        print(f"生成: {filepath}")

    # 写一个索引文件，方便核对
    index_file = os.path.join(OUTPUT_DIR, "index.txt")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print(f"\n共生成 {total} 个二维码，索引见: {index_file}")
    print("按 qr_001, qr_002 ... 的顺序依次在屏幕上打开给手机扫码即可。")


if __name__ == "__main__":
    main()
