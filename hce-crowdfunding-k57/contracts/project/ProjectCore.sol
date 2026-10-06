// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Cong gay quy co co che hoan tien
/// @author Nguyen Nguyen Phuong (23K4300034) & Hoang Manh Tuong (23K4300042)
contract ProjectCore {
    address public immutable creator;
    uint256 public immutable goal;
    uint256 public immutable deadline;
    uint256 public totalRaised;
    bool public fundsClaimed;

    mapping(address => uint256) public contributions;

    event Contributed(address indexed contributor, uint256 amount);
    event FundsClaimed(address indexed creator, uint256 amount);
    event RefundIssued(address indexed contributor, uint256 amount);

    error CampaignEnded();
    error GoalNotReached();
    error GoalAlreadyMet();
    error RefundNotAllowed();
    error NotCreator();
    error TransferFailed();
    error NoFundsToRefund();
    error ZeroAmount();

    constructor(uint256 _goalWei, uint256 _durationSeconds) {
        require(_goalWei > 0, "Muc tieu phai lon hon 0");
        creator = msg.sender;
        goal = _goalWei;
        deadline = block.timestamp + _durationSeconds;
    }

    /// @notice Nguoi dung dong gop ETH vao du an
    function contribute() external payable {
        if (block.timestamp >= deadline) revert CampaignEnded();
        if (totalRaised >= goal) revert GoalAlreadyMet();
        if (msg.value == 0) revert ZeroAmount();

        contributions[msg.sender] += msg.value;
        totalRaised += msg.value;

        emit Contributed(msg.sender, msg.value);
    }

    /// @notice Chu du an rut toan bo quy khi dat hoac vuot muc tieu
    function claimFunds() external {
        if (msg.sender != creator) revert NotCreator();
        if (totalRaised < goal) revert GoalNotReached();
        if (fundsClaimed) revert CampaignEnded();

        // Checks - Effects - Interactions: Cap nhat trang thai truoc
        fundsClaimed = true;
        uint256 payoutAmount = totalRaised;
        emit FundsClaimed(creator, payoutAmount);

        // Chuyen tien sau
        (bool ok, ) = payable(creator).call{value: payoutAmount}("");
        if (!ok) revert TransferFailed();
    }

    /// @notice Nguoi ung ho tu rut lai tien neu het han ma khong dat muc tieu
    function refund() external {
        if (block.timestamp < deadline) revert RefundNotAllowed();
        if (totalRaised >= goal) revert RefundNotAllowed();

        uint256 balance = contributions[msg.sender];
        if (balance == 0) revert NoFundsToRefund();

        // Xoa so du ve 0 truoc de chong loi tai nhap (Reentrancy)
        contributions[msg.sender] = 0;
        emit RefundIssued(msg.sender, balance);

        // Chuyen tra tien
        (bool ok, ) = payable(msg.sender).call{value: balance}("");
        if (!ok) revert TransferFailed();
    }

    function timeLeft() external view returns (uint256) {
        if (block.timestamp >= deadline) return 0;
        return deadline - block.timestamp;
    }
}