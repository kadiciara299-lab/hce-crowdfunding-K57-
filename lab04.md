# BÁO CÁO THẨM ĐỊNH RỦI RO HỢP ĐỒNG TOKEN — LAB 04

### Bảng kết luận thẩm định

| Hợp đồng | Kết luận | Tên hàm | Số dòng | Rủi ro cho người nắm giữ |
| :--- | :--- | :--- | :--- | :--- |
| **ClubTokenA** | **An toàn** (Không có quyền đặc biệt) | *Không tìm thấy* | *Không có* | **Không có rủi ro từ quyền admin**: Hợp đồng không kế thừa `Ownable`, không có hàm đúc thêm hay chặn giao dịch. Tổng cung cố định 1.000.000 CTA ngay từ constructor. |
| **ClubTokenB** | **Rủi ro cao** (Nguy cơ đúc vô hạn / Lạm phát) | [`mint(address to, uint256 amount)`](file:///Users/phuongnguyennguyen/Downloads/hce-web3-starter/contracts/lab04/ClubTokens.sol#L18-L20) | [Dòng 18–20](file:///Users/phuongnguyennguyen/Downloads/hce-web3-starter/contracts/lab04/ClubTokens.sol#L18-L20) | **Pha loãng tài sản / Nguy cơ sập giá (Rug Pull)**: Chủ sở hữu có thể tự ý đúc thêm token không giới hạn số lượng và bán xả ra thị trường làm giá token về 0. |
| **ClubTokenC** | **Rủi ro cao** (Nguy cơ đóng băng / Bẫy không thể bán) | [`setRestricted(address user, bool status)`](file:///Users/phuongnguyennguyen/Downloads/hce-web3-starter/contracts/lab04/ClubTokens.sol#L30-L32) | [Dòng 30–32](file:///Users/phuongnguyennguyen/Downloads/hce-web3-starter/contracts/lab04/ClubTokens.sol#L30-L32) | **Đóng băng tài sản (Blacklist / Honeypot)**: Chủ sở hữu có thể đưa bất kỳ địa chỉ nào vào danh sách hạn chế, chặn toàn bộ lệnh chuyển đi ở [`_update`](file:///Users/phuongnguyennguyen/Downloads/hce-web3-starter/contracts/lab04/ClubTokens.sol#L34-L37), khiến người nắm giữ không thể bán hay chuyển token. |

---

### Chi tiết thẩm định chuyên sâu từng hợp đồng

#### 1. Hợp đồng [ClubTokenA]
* **Quyền đặc biệt của chủ sở hữu:** **Không tìm thấy**.
* **Phân tích kỹ thuật:**
  * Hợp đồng chỉ kế thừa [`ERC20`], không kế thừa `Ownable`.
  * Toàn bộ 1.000.000 token (nhân hệ số thập phân) được đúc một lần duy nhất tại constructor [Dòng 8–10]
  * Không có hàm `external` hay `public` nào cho phép can thiệp vào số dư hoặc trạng thái chuyển nhượng.
* **Đánh giá rủi ro:** Người nắm giữ hoàn toàn được bảo vệ trước sự can thiệp có chủ đích của bên phát hành.

#### 2. Hợp đồng [ClubTokenB]
* **Quyền đặc biệt của chủ sở hữu:** Hàm [`mint`]n
* **Điều kiện thực thi:** Ràng buộc bởi bộ điều chỉnh quyền `onlyOwner` ([Dòng 18]
* **Rủi ro người nắm giữ:**
  * **Lạm phát không kiểm soát (Infinite Minting):** Không có trần tổng cung (`maxSupply`). Chủ sở hữu có thể đúc số lượng tùy ý về ví của mình.
  * **Xả hàng (Dump):** Nếu token có giá trị thanh khoản trên sàn phi tập trung (DEX), chủ sở hữu có thể đúc hàng triệu token và hoán đổi rút cạn thanh khoản, làm toàn bộ token của các nhà đầu tư khác mất giá trị.

#### 3. Hợp đồng [ClubTokenC]
* **Quyền đặc biệt của chủ sở hữu:** Hàm [`setRestricted`] tại [Dòng 30–32]:**
  * Chủ sở hữu bật/tắt cờ `restricted` qua mapping tại [Dòng 24] và [Dòng 31]
  * Trong hàm ghi đè [`_update`] ([Dòng 35]), kiểm tra điều kiện:
    ```solidity
    require(!restricted[from], "Dia chi bi han che");
    ```
* **Rủi ro người nắm giữ:**
  * **Đóng băng tài khoản / Honeypot:** Bất kỳ địa chỉ ví nào khi bị đặt `restricted = true` sẽ bị chặn gửi đi (`from`), tức là vẫn nhận được token nhưng **không thể chuyển nhượng hay bán ra**. Quyền sở hữu tài sản thực tế bị tước bỏ bởi chủ sở hữu hợp đồng.
