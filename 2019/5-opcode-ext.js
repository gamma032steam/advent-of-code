const fs = require('fs');
const readline = require('readline-sync');

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/5-input.txt').toString().split(',').map(m => parseInt(m));
    parse(input);
}

function parse(opcode) {
    let readLoc = 0;
    while (readLoc < opcode.length) {
        switch (getCode(opcode[readLoc])) {
            case '99':
                return opcode;
            case '01': 
                {
                // Add
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2]);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1]);
                opcode[opcode[readLoc+3]] = num1 + num2;
                readLoc += 4;
                break;
                }
            case '02': 
                {
                // Multiply
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2]);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1]);
                opcode[opcode[readLoc+3]] = num1 * num2;
                readLoc += 4;
                break;
                }
            case '03':
                {
                // Input
                let read = readline.question("Input: ");
                opcode[opcode[readLoc+1]] = parseInt(read);
                readLoc += 2;
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                console.log(get(opcode, opcode[readLoc+1], instruction[0]));
                readLoc += 2;
                break;
                }
            case '05':
                {
                // Jump-if-true
                let instruction = prependZero(opcode[readLoc], 4);
                if (get(opcode, opcode[readLoc+1], instruction[1]) != 0) {
                    readLoc = get(opcode, opcode[readLoc+2], instruction[0]);
                } else {
                    readLoc += 3;
                }
                break;
                }
            case '06':
                {
                // Jump-if-false
                let instruction = prependZero(opcode[readLoc], 4);
                if (get(opcode, opcode[readLoc+1], instruction[1]) == 0) {
                    readLoc = get(opcode, opcode[readLoc+2], instruction[0]);
                } else {
                    readLoc += 3;
                }
                break;
                }
            case '07':
                {
                // Less than
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2]);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1]);
                if (num1 < num2) {
                    opcode[opcode[readLoc+3]] = 1;
                } else {
                    opcode[opcode[readLoc+3]] = 0;
                }
                readLoc += 4;
                break;
                }
            case '08':
                {
                // Equal to
                let instruction = prependZero(opcode[readLoc], 5);
                let num1 = get(opcode, opcode[readLoc+1], instruction[2]);
                let num2 = get(opcode, opcode[readLoc+2], instruction[1]);
                if (num1 == num2) {
                    opcode[opcode[readLoc+3]] = 1;
                } else {
                    opcode[opcode[readLoc+3]] = 0;
                }
                readLoc += 4;
                break;
                }
        }
    }
}

/** Get a value from the opcode via the specified mode */
function get(opcode, parameter, mode) {
    if (mode == '0') {
        return opcode[parameter]
    } else {
        return parameter;
    }
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

main();