# Auto Clicker - Nhiều vị trí

Ứng dụng Auto Clicker đa vị trí cho phép người dùng tự động click chuột vào các vị trí khác nhau trên màn hình với thời gian delay tùy chỉnh. Ứng dụng có giao diện đồ họa thân thiện và dễ sử dụng.

## Tính năng chính

- 🖱️ Click tự động nhiều vị trí trên màn hình
- ⏱️ Tùy chỉnh thời gian delay giữa các lần click
- 📍 Lấy tọa độ chuột hiện tại
- ⌨️ Phím tắt F1 để dừng quá trình tự động
- 🎨 Giao diện hiện đại và dễ sử dụng

## Cách sử dụng

1. **Thêm vị trí**: Nhấn nút "+ Thêm vị trí" để thêm một vị trí mới vào danh sách
2. **Lấy tọa độ**: Chọn một dòng (bằng cách click vào ô nhập), sau đó nhấn "📍 Lấy tọa độ". Ứng dụng sẽ đếm ngược 3 giây và sau đó lấy vị trí con trỏ chuột
3. **Nhập delay**: Nhập thời gian delay (bằng giây) cho mỗi vị trí
4. **Bắt đầu/Dừng**: Nhấn "▶️ Bắt đầu" để khởi động quá trình tự động click, và "⏹️ Dừng" hoặc phím F1 để dừng lại

## Yêu cầu hệ thống

- Python 3.6 trở lên
- Các thư viện: tkinter, pyautogui, keyboard

## Cài đặt

```bash
pip install pyautogui keyboard
```

## Chạy ứng dụng

```bash
python autoclick.py
```

## Lưu ý

- Ứng dụng sử dụng phím F1 làm phím tắt để dừng quá trình tự động click
- Phải có ít nhất một vị trí trong danh sách
- Khi đang chạy, không nên di chuyển chuột hoặc sử dụng bàn phím để tránh gián đoạn quá trình tự động

## Giấy phép

Phát triển và phân phối tự do cho mục đích cá nhân và phi thương mại.
