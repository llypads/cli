pragma solidity ^0.4.17;

contract Repo {
    mapping(address => bool) admins;
    mapping (string => bytes32) refs;
    mapping (bytes32 => bytes32) anchors;
    string headRef;

    modifier onlyAdmin {
        require(admins[msg.sender]);
        _;
    }

    event Bounty(
        address indexed sender,
        uint32 bountyId,
        uint256 amount,
        string status
    );

    event Proposal(
        address indexed sender,
        bytes32 indexed bountyId,
        bytes32 indexed gitHash,
        bytes32 proposalId,
        bytes32 anchorAddress,
        bytes32 contentAddress
    );

    event Payout(
        bytes32 indexed bountyId,
        bool indexed success
    );

    function Repo(string head) public {
        admins[msg.sender] = true;
        headRef = head;
    }

    function setHead(string nextHeadRef) public onlyAdmin {
        headRef = nextHeadRef;
    }

    function getHead() public constant returns (string) {
        return headRef;
    }

    function getRef(string ref) public constant returns (bytes32) {
        return refs[ref];
    }

    function getAnchor(bytes32 hash) public constant returns (bytes32 content_address) {
        content_address = anchors[hash];
    }

    function push(string ref, bytes32 hash, bytes32 content_address) public {
        refs[ref] = hash;
        anchors[hash] = content_address;
    }

    function createBounty(uint32 bountyid, string status) public payable onlyAdmin {
        Bounty(
            msg.sender,
            bountyid,
            msg.value,
            status
        );
    }

    function rewardBounty(bytes32 bountyId, address recipient, uint256 amount) public onlyAdmin {
        Payout(bountyId, recipient.send(amount));
    }

    function propose(bytes32 bountyId, bytes32 gitHash, bytes32 anchorAddress, bytes32 contentAddress) public {
        Proposal(
            msg.sender,
            bountyId,
            gitHash,
            bytes32(keccak256(msg.sender, bountyId)),
            anchorAddress,
            contentAddress
        );
    }
}
