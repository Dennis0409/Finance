# 1️⃣ 使用 Python 3.10 基礎鏡像
FROM python:3.10

# 2️⃣ 設定工作目錄
WORKDIR /app

# 3️⃣ 複製專案內的所有文件到 Docker 容器
COPY . /app

# 4️⃣ 安裝 Flask 及相關依賴
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Expose Flask 的預設埠
EXPOSE 5001

# 6️⃣ 啟動 Flask 應用
CMD ["python", "app.py"]