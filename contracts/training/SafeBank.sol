// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SafeBankCEI — Ngan hang an toan bang cach ap dung Checks-Effects-Interactions
/// @notice Khac phuc lo hong Reentrancy ma khong can thu vien ngoai, tiet kiem gas toi da
contract SafeBankCEI {
    mapping(address => uint256) public balances;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    error NoBalance();
    error TransferFailed();

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Cach 1: Cap nhat so sach TRUOC khi chuyen tien ra ngoai
    function withdraw() external {
        // 1. Checks: Kiem tra dieu kien
        uint256 bal = balances[msg.sender];
        if (bal == 0) revert NoBalance();

        // 2. Effects: Xoa so du truoc tren bien trang thai (cap nhat so sach truoc)
        balances[msg.sender] = 0;
        emit Withdrawn(msg.sender, bal);

        // 3. Interactions: Chuyen ETH ra ngoai sau cung bang call
        (bool ok, ) = msg.sender.call{value: bal}("");
        if (!ok) revert TransferFailed();
    }

    function bankBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

/// @title SafeBankGuard — Ngan hang an toan bang khoa chong goi lai (ReentrancyGuard)
/// @notice Mo phong co che nonReentrant cua OpenZeppelin
contract SafeBankGuard {
    mapping(address => uint256) public balances;
    bool private _locked;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    error NoBalance();
    error TransferFailed();
    error ReentrantCall();

    modifier nonReentrant() {
        if (_locked) revert ReentrantCall();
        _locked = true;
        _;
        _locked = false;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Cach 2: Su dung chot chan khoa trang thai nonReentrant
    function withdraw() external nonReentrant {
        uint256 bal = balances[msg.sender];
        if (bal == 0) revert NoBalance();

        balances[msg.sender] = 0;
        emit Withdrawn(msg.sender, bal);

        (bool ok, ) = msg.sender.call{value: bal}("");
        if (!ok) revert TransferFailed();
    }

    function bankBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
