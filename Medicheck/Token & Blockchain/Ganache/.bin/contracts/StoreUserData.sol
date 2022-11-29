pragma solidity >= 0.4.22 <0.9.0;

contract StoreUserData {

    string public payload;

    function setPayload(string memory content) public {
        payload = content;
    }

}
