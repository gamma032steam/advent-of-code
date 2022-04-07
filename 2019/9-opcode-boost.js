const fs = require('fs');
const readline = require('readline-sync');

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/13-input.txt').toString().split(',').map(m => parseInt(m));
    let prog = addMemory(input);
    //console.log(prog)
    parse(prog);
}

function parse(opcode) {
    let readLoc = 0, relativeBase = 0;
    while (readLoc < opcode.length) {
        switch (getCode(opcode[readLoc])) {
            case '99':
                return opcode;
            case '01': 
                {
                // Add
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2], relativeBase);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1], relativeBase);
                opcode = put(opcode, opcode[readLoc+3], num1+num2, instruction[0], relativeBase);
                readLoc += 4;
                break;
                }
            case '02': 
                {
                // Multiply
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2], relativeBase);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1], relativeBase);
                opcode = put(opcode, opcode[readLoc+3], num1*num2, instruction[0], relativeBase);
                readLoc += 4;
                break;
                }
            case '03':
                {
                // Input
                let instruction = prependZero(opcode[readLoc], 3);
                let read = readline.question("Input: ");
                opcode = put(opcode, opcode[readLoc+1], parseInt(read), instruction[0], relativeBase);
                readLoc += 2;
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                console.log(get(opcode, opcode[readLoc+1], instruction[0], relativeBase));
                readLoc += 2;
                break;
                }
            case '05':
                {
                // Jump-if-true
                let instruction = prependZero(opcode[readLoc], 4);
                if (get(opcode, opcode[readLoc+1], instruction[1], relativeBase) != 0) {
                    readLoc = get(opcode, opcode[readLoc+2], instruction[0], relativeBase);
                } else {
                    readLoc += 3;
                }
                break;
                }
            case '06':
                {
                // Jump-if-false
                let instruction = prependZero(opcode[readLoc], 4);
                if (get(opcode, opcode[readLoc+1], instruction[1], relativeBase) == 0) {
                    readLoc = get(opcode, opcode[readLoc+2], instruction[0], relativeBase);
                } else {
                    readLoc += 3;
                }
                break;
                }
            case '07':
                {
                // Less than
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2], relativeBase);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1], relativeBase);
                if (num1 < num2) {
                    opcode = put(opcode, opcode[readLoc+3], 1, instruction[0], relativeBase);
                } else {
                    opcode = put(opcode, opcode[readLoc+3], 0, instruction[0], relativeBase);
                }
                readLoc += 4;
                break;
                }
            case '08':
                {
                // Equal to
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2], relativeBase);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1], relativeBase);
                if (num1 == num2) {
                    opcode = put(opcode, opcode[readLoc+3], 1, instruction[0], relativeBase);
                } else {
                    opcode = put(opcode, opcode[readLoc+3], 0, instruction[0], relativeBase);
                }
                readLoc += 4;
                break;
                }
            case '09':
                {
                // Relative base adjustment
                let instruction = prependZero(opcode[readLoc], 3);
                let offset = get(opcode, opcode[readLoc+1], instruction[0], relativeBase);
                relativeBase += offset;
                readLoc += 2;
                break;
                }
        }
    }
}

/** Get a value from the opcode via the specified mode */
function get(opcode, parameter, mode, offset) {
    if (mode == '0') {
        return opcode[parameter]
    } else if (mode == '1') {
        return parameter;
    } else if (mode == '2') {
        return opcode[offset+parameter];
    }
}

/** Put a value in to the opcode */
function put(opcode, position, value, mode, offset) {
    if (mode == '0') {
        opcode[position] = value;
    } else if (mode == '2') {
        opcode[offset+=position] = value;
    }
    return opcode;
}

/** Grabs the last two numbers from an opcode instruction */
function getCode(instruction) {
    let code = prependZero(instruction, 2);
    return code.slice(code.length - 2).join('');
}

/** Adds the 'default' zeroes before instructions */
function prependZero(instruction, n) {
    instruction = instruction.toString().split('');
    while (instruction.length < n) {
        instruction.unshift('0');
    }
    return instruction;
}

/** Adds a thousand memory positions */
function addMemory(opcode) {
    let zeroes = [];
    for (let i = 0; i  < 1000; i++) {
        zeroes[i] = 0;
    }
    return opcode.concat(zeroes);
}

main();