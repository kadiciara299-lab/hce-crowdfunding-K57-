// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../contracts/project/ProjectCore.sol";

contract ProjectCoreNegativeTest {
    ProjectCore public project;

    function setUp() public {
        project = new ProjectCore(2 ether, 100);
    }

    function testFail_UnauthorizedWithdraw() external {
        project.withdrawFunds();
    }

    function testFail_RefundBeforeDeadline() external {
        project.claimRefund();
    }

    function testFail_ContributionBelowMinimum() external payable {
        (bool success, ) = address(project).call{value: 500}(
            abi.encodeWithSignature("contribute()")
        );
        require(!success, "Giao dich phai bi chan");
    }
}
