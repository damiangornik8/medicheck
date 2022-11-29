pragma solidity >= 0.4.22 <0.9.0;

contract HelloWorld {

    string public payload;

    function setPayload(string memory content) public {
        payload = content;
    }

    function sayHello() public pure returns (string memory) {
        return 'Hello World!';
    }
}
