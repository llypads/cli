pragma solidity ^0.4.0;

contract LillyRepo {
    mapping(address => bool) admins;
    mapping(address => bool) committers;
    mapping (string => string) refs;
    string headRef;
    string[] refKeys;
    string[] objects;

    function LillyRepo(string head) public {
        admins[msg.sender] = true;
        committers[msg.sender] = true;
        headRef = head;
    }

    function getHead() public constant returns (string) {
        return headRef;
    }

    function getRef(string ref) public constant returns (string hash) {
        hash = refs[ref];
    }

    function refCount() public constant returns (uint) {
        return refKeys.length;
    }

    function getRefKey(uint index) public constant returns (string ref) {
        ref = refKeys[index];
    }

    function push(string ref, string hash, string content_address) public {
        if (!refs[ref] == "0x0") {
          refKeys.push(ref);
        }
        refs[ref] = hash;

        objects.push(content_address);
    }

    function addObject(string hash) public {
        objects.push(hash);
    }

    function getObject(uint index) public constant returns (string hash) {
        return objects[index];
    }

    function objectCount() public constant returns (uint) {
        return objects.length;
    }
}
