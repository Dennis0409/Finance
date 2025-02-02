# 財務管理系統 

這是一個使用 **Flask + SQLite** 開發的個人財務管理系統，支援 **JWT 身份驗證**，可 **記錄收入/支出、篩選記錄、統計數據**，並支援 **Docker 一鍵部署**。

## 主要功能
✅ 記錄收入與支出  
✅ 篩選特定範圍的紀錄  
✅ 總收入 & 支出計算  
✅ Docker 容器化部署  

## 如何運行（使用 Docker）
```bash
git clone https://github.com/Dennis0409/Finance.git
cd back
docker-compose up --build -d
```
之後訪問：```http://127.0.0.1:5001```

## Demo

### Register
![截圖 2025-02-02 下午4.24.36](https://hackmd.io/_uploads/rkuCojn_1l.png)

### Login
![截圖 2025-02-02 下午4.25.31](https://hackmd.io/_uploads/rJTWho3O1e.png)

### 財務紀錄
![截圖 2025-01-31 下午5.29.10](https://hackmd.io/_uploads/S1ND2i2dyx.png)

