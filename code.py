import qrcode
import base64
import zlib
import sys
import os

# 默认参数
DEFAULT_OUTPUT = "output_qr.png"
CHUNK_SIZE = 2850  # Version40-L 大约最大容量（可调）

def main():
    if len(sys.argv) < 2:
        print(f"用法: python {os.path.basename(sys.argv[0])} <输入文件> [输出二维码文件]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_OUTPUT

    # 读取代码
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    # 压缩 + Base64
    compressed = zlib.compress(data.encode("utf-8"))
    b64 = base64.b64encode(compressed).decode("ascii")

    if len(b64) > CHUNK_SIZE:
        print(f"警告: 内容长度 {len(b64)} 超过单二维码容量限制 {CHUNK_SIZE}")
        print("建议调大二维码尺寸或拆分为多二维码")
        sys.exit(2)

    # 生成二维码
    qr = qrcode.QRCode(
        version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(b64)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

    print(f"二维码生成成功: {output_file}")
    print(f"压缩后长度: {len(b64)} 字符")

if __name__ == "__main__":
    main()



import base64, zlib

with open("scanned.txt", "r", encoding="utf-8") as f:
    b64 = f.read().strip()

data = zlib.decompress(base64.b64decode(b64)).decode("utf-8")

with open("restored_code.py", "w", encoding="utf-8") as f:
    f.write(data)

print("恢复成功: restored_code.py")
