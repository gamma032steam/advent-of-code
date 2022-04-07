const fs = require('fs');

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/2-input.txt').toString().split(',').map(m => parseInt(m));
    // Manual changes for Q1
    let opcode1 = input.slice();
    opcode1[1] = 12;
    opcode1[2] = 2;
    console.log('Q1: ' + parse(opcode1));
    console.log('Q2: ' + deconstruct(input, 19690720));
}

/** Find the noun and verb for a particular outut */
function deconstruct(opcode, result) {
    // Loop through possible inputs
    for (noun = 0; noun < 100; noun++) {
        for (verb = 0; verb < 100; verb++) {
            let testOpcode = [...opcode];
            testOpcode[1] = noun; 
            testOpcode[2] = verb;
            // See if the 'output' at the first position matches
            if (parse(testOpcode)[0] == result) {
                return ('Noun: ' + noun + ' verb: ' + verb); 
            }
        }
    }
}

/** Parse the opcode and return the resulting value */
function parse(opcode) {
    let readLoc = 0;
    while(true) {
        switch (opcode[readLoc]) {
            case 1:
                {
                opcode[opcode[readLoc+3]] = opcode[opcode[readLoc+1]] + opcode[opcode[readLoc+2]];
                break;
                }
            case 2:
                {
                opcode[opcode[readLoc+3]] = opcode[opcode[readLoc+1]] * opcode[opcode[readLoc+2]];
                break;
                }
            case 99:
                return opcode;
            default:
                return 'Invalid code: ' + opcode[readLoc] + ' at location ' + readLoc;
        }
        readLoc += 4;
    }
}

main();