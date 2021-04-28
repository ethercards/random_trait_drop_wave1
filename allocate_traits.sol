//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.3;

import "interface/IRNG.sol";
import "interface/Strings.sol";

contract allocate_traits {
    using Strings for *;

    IRNG               rng;
    bytes32 public     stash;
    bool    public     random_processed;
    bool    public     data_folder_set;
    bool    public     _FuzeBlown;
    string  public     baseURI;

    
    uint256 constant   num_og = 90;
    uint256 constant   num_alphas = 900;
    uint256 constant   num_founders = 9000;
    uint256 public     random;
    uint256 public     og_rand;
    uint256 public     alpha_rand;
    uint256 public     founder_rand;

    event ProcessRandom();

    address owner;
    
    modifier onlyOwner() {
        require(msg.sender == owner,"Unauthorised");
        _;
    }

    constructor(address _owner,IRNG _rng) {
        owner = _owner;
        rng = _rng;
    }

    function the_big_red_button() external onlyOwner {
        require(!_FuzeBlown,"You can ony use the BIG RED BUTTON if the fuzes are not blown");
        stash = rng.requestRandomNumber();
        burnDataFolder();
    }

    function ready_to_process() public view returns (bool) {
        return rng.isRequestComplete(stash);
    }

    function process_random() external onlyOwner {
        require(_FuzeBlown,"You need to press the BIG RED BUTTON");
        require(ready_to_process(),"The random number is not ready yet");
        random = rng.randomNumber(stash);
        uint mask = 0xffffffffffffffff; // 8 bytes or 64 bits
        og_rand = (random & mask);
        alpha_rand = (random >> 64) & mask;
        founder_rand = (random >> 128) & mask;
        random_processed = true;
        emit ProcessRandom();
    }

    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(random_processed,"Randomization not complete");
        uint id = tokenId;
        if (tokenId < 10) {
            //
        } else if (tokenId < 100) {
            id = ((tokenId + og_rand) % 90) + 10;
        } else if (tokenId < 1000) {
            id = ((tokenId + alpha_rand) % 900) + 100;
        } else if (tokenId < 10000){
            id = ((tokenId + founder_rand) % 9000) + 1000;
        }
        return iTokenURI(id);
    }

    function setDataFolder(string memory _baseURI) external onlyOwner {
        require(!_FuzeBlown,"This data can no longer be changed");
        baseURI = _baseURI;
        data_folder_set = true;
    }

    function burnDataFolder() internal onlyOwner {
        require(data_folder_set,"This data can no longer be changed");
        _FuzeBlown = true;
    }

    function iTokenURI(uint256 tokenId) public view returns (string memory) {
        // reformat to directory structure as below
        string memory folder = (tokenId % 100).toString(); 
        string memory file = tokenId.toString();
        string memory slash = "/";
        return string(abi.encodePacked(baseURI,folder,slash,file,".json"));
    }

}