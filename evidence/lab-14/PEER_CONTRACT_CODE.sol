// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title EventTicketCore — Hop dong ve su kien cua Nhom 6 (Doi tuong duoc Nhom 5 audit cheo)
/// @notice Phat hanh ve su kien gioi han ban lai, co chuc nang hoan ve va check-in
contract EventTicketCore is ERC721, Ownable {
    uint256 public nextTokenId = 1;
    uint256 public maxSupply;
    uint256 public ticketPrice;
    uint256 public resellFeePercent; // Tinh bang phan tram (%) thay vi basis points

    mapping(uint256 => bool) public isCheckedIn;
    mapping(address => bool) public hasPurchased;

    event TicketBought(address indexed buyer, uint256 indexed tokenId);
    event TicketCheckedIn(uint256 indexed tokenId, address attendee);
    event TicketRefunded(address indexed buyer, uint256 indexed tokenId, uint256 amount);

    error SoldOut();
    error WrongEtherSent();
    error AlreadyHasTicket();
    error NotTicketOwner();
    error AlreadyCheckedIn();
    error TransferFailed();

    constructor(
        string memory _name,
        string memory _symbol,
        uint256 _maxSupply,
        uint256 _price,
        uint256 _feePercent
    ) ERC721(_name, _symbol) Ownable(msg.sender) {
        maxSupply = _maxSupply;
        ticketPrice = _price;
        resellFeePercent = _feePercent;
    }

    /// @notice Nguoi tham du mua ve
    function buyTicket() external payable {
        if (nextTokenId > maxSupply) revert SoldOut();
        if (msg.value != ticketPrice) revert WrongEtherSent();
        if (hasPurchased[msg.sender]) revert AlreadyHasTicket();

        uint256 tokenId = nextTokenId;
        nextTokenId++;
        hasPurchased[msg.sender] = true;

        _safeMint(msg.sender, tokenId);
        emit TicketBought(msg.sender, tokenId);
    }

    /// @notice Ban to chuc cap ve moi cho khach VIP
    /// @dev LO HONG 2: Quen kiem tra dia chi rong address(0)
    function issueVipTicket(address to) external onlyOwner {
        if (nextTokenId > maxSupply) revert SoldOut();
        uint256 tokenId = nextTokenId;
        nextTokenId++;
        _safeMint(to, tokenId);
    }

    /// @notice Ban to chuc soat ve tai cua
    function checkIn(uint256 tokenId) external onlyOwner {
        if (ownerOf(tokenId) == address(0)) revert NotTicketOwner();
        if (isCheckedIn[tokenId]) revert AlreadyCheckedIn();

        isCheckedIn[tokenId] = true;
        emit TicketCheckedIn(tokenId, ownerOf(tokenId));
    }

    /// @notice Hoan lai ve truoc su kien (Refund)
    /// @dev LO HONG 1 (NGHIEM TRONG): Vi pham CEI, chuyen tien TRUOC KHI burn hoac xoa trang thai!
    function refundTicket(uint256 tokenId) external {
        if (ownerOf(tokenId) != msg.sender) revert NotTicketOwner();
        if (isCheckedIn[tokenId]) revert AlreadyCheckedIn();

        uint256 refundAmount = ticketPrice;

        // LOI CEI NGUY HIEM: Chuyen tien ra ngoai truoc!
        (bool ok, ) = payable(msg.sender).call{value: refundAmount}("");
        if (!ok) revert TransferFailed();

        // Xoa trang thai qua muon -> Mo duong cho Reentrancy Attack!
        _burn(tokenId);
        hasPurchased[msg.sender] = false;
        emit TicketRefunded(msg.sender, tokenId, refundAmount);
    }

    /// @notice Tinh phi ban lai thu cap
    /// @dev LO HONG 3: Phep chia so nguyen lam tron xuong 0 do dung % thay vi basis point (1% = 100)
    function calculateResellFee(uint256 resellPrice) public view returns (uint256) {
        return (resellPrice * resellFeePercent) / 100;
    }

    /// @notice Ban to chuc doi gia ve
    /// @dev LO HONG 4: Khong phat event khi thay doi gia ve quan trong
    function setTicketPrice(uint256 newPrice) external onlyOwner {
        ticketPrice = newPrice;
    }

    function withdraw() external onlyOwner {
        (bool ok, ) = payable(owner()).call{value: address(this).balance}("");
        if (!ok) revert TransferFailed();
    }
}
