const fs = require('fs');


function main() {
    let input = fs.readFileSync('./input/8-input.txt').toString().split('').map(m => parseInt(m));
}

main();