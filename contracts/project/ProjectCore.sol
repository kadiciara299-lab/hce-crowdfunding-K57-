// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ProjectCore - Nền tảng gây quỹ sinh viên có hoàn tiền
 * @notice Phiên bản hoàn thiện sau Cross-Audit Lab 14
 */
contract ProjectCore {
    address public immutable creator;
    uint256 public immutable targetAmount;
    uint256 public immutable deadline;
    uint256 public totalContributed;
    bool public fundsWithdrawn;

    uint256 public constant MIN_CONTRIBUTION = 10**15; // 0.001 ETH

    mapping(address => uint256) public contributions;

    event Contributed(address indexed contributor, uint256 amount, uint256 currentTotal);
    event GoalReached(uint256 totalAmount);
    event FundsWithdrawn(address indexed creator, uint256 amount);
    event RefundIssued(address indexed contributor, uint256 amount);

    error InvalidParameters();
    error ContributionTooLow(uint256 sentAmount, uint256 minAmount);
    error CampaignActive(uint256 currentTime, uint256 deadline);
    error CampaignEnded();
    error NotCreator();
    error GoalNotMet(uint256 total, uint256 target);
    error GoalAlreadyMet();
    error NoFundsToRefund();
    error AlreadyWithdrawn();
    error TransferFailed();

    constructor(uint256 _targetAmountWei, uint256 _durationSeconds) {
        if (_targetAmountWei == 0 || _durationSeconds == 0) revert InvalidParameters();
        creator = msg.sender;
        targetAmount = _targetAmountWei;
        deadline = block.timestamp + _durationSeconds;
    }

    function contribute() external payable {
        if (block.timestamp > deadline) revert CampaignEnded();
        if (fundsWithdrawn) revert AlreadyWithdrawn();
        if (msg.value < MIN_CONTRIBUTION) {
            revert ContributionTooLow(msg.value, MIN_CONTRIBUTION);
        }

        contributions[msg.sender] += msg.value;
        totalContributed += msg.value;

        emit Contributed(msg.sender, msg.value, totalContributed);

        if (totalContributed >= targetAmount) {
            emit GoalReached(totalContributed);
        }
    }

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
