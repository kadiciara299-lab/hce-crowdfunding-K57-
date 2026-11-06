// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ProjectCore - Nền tảng gây quỹ sinh viên có hoàn tiền
 * @notice Cài đặt luồng cốt lõi theo docs/SPEC.md: Đóng góp -> Giải ngân / Hoàn tiền
 * @dev Bản vá Lab 10: Khắc phục lỗi kẹt quỹ khi đạt mục tiêu sớm trong withdrawFunds()
 */
contract ProjectCore {
    address public immutable creator;
    uint256 public immutable targetAmount;
    uint256 public immutable deadline;
    uint256 public totalContributed;
    bool public fundsWithdrawn;

    mapping(address => uint256) public contributions;

    event Contributed(address indexed contributor, uint256 amount, uint256 currentTotal);
    event GoalReached(uint256 totalAmount);
    event FundsWithdrawn(address indexed creator, uint256 amount);
    event RefundIssued(address indexed contributor, uint256 amount);

    error CampaignActive(uint256 currentTime, uint256 deadline);
    error CampaignEnded();
    error ZeroContribution();
    error NotCreator();
    error GoalNotMet(uint256 total, uint256 target);
    error GoalAlreadyMet();
    error NoFundsToRefund();
    error AlreadyWithdrawn();
    error TransferFailed();

    constructor(uint256 _targetAmountWei, uint256 _durationSeconds) {
        creator = msg.sender;
        targetAmount = _targetAmountWei;
        deadline = block.timestamp + _durationSeconds;
    }

    function contribute() external payable {
        if (block.timestamp > deadline) revert CampaignEnded();
        if (msg.value == 0) revert ZeroContribution();

        contributions[msg.sender] += msg.value;
        totalContributed += msg.value;

        emit Contributed(msg.sender, msg.value, totalContributed);

        if (totalContributed >= targetAmount) {
            emit GoalReached(totalContributed);
        }
    }

    /// @notice Sửa lỗi Lab 10: Cho phép rút tiền ngay khi đạt mục tiêu, không bắt buộc đợi deadline
    function withdrawFunds() external {
        if (msg.sender != creator) revert NotCreator();
        if (totalContributed < targetAmount && block.timestamp <= deadline) {
            revert CampaignActive(block.timestamp, deadline);
        }
        if (totalContributed < targetAmount) revert GoalNotMet(totalContributed, targetAmount);
        if (fundsWithdrawn) revert AlreadyWithdrawn();

        fundsWithdrawn = true;
        uint256 balance = address(this).balance;

        emit FundsWithdrawn(creator, balance);

        (bool success, ) = creator.call{value: balance}("");
        if (!success) revert TransferFailed();
    }

    function claimRefund() external {
        if (block.timestamp <= deadline) revert CampaignActive(block.timestamp, deadline);
        if (totalContributed >= targetAmount) revert GoalAlreadyMet();

        uint256 contributedAmount = contributions[msg.sender];
        if (contributedAmount == 0) revert NoFundsToRefund();

        contributions[msg.sender] = 0;

        emit RefundIssued(msg.sender, contributedAmount);

        (bool success, ) = msg.sender.call{value: contributedAmount}("");
        if (!success) revert TransferFailed();
    }
}
