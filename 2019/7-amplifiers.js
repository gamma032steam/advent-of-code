// This program is long because the opcode program was written differently for part 2.

const fs = require('fs');
const readline = require('readline-sync');

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/7-input.txt').toString().split(',').map(m => parseInt(m));
    console.log(maxSignal(input, [0, 1, 2, 3, 4], 0));
    console.log(bestFeedback(input));
}

function bestFeedback(opcode) {
    possibilities = perms([5,6,7,8,9]);
    let max = -1;
    for (poss of possibilities) {
        let score = scoreFeedback(opcode, poss);
        if (score > max) {
            max = score;
        }
    }
    return max;
}

function scoreFeedback(opcode, phase) {
    let programs = [];
    let positions = [];

    for (let p = 0; p < phase.length; p++) {
        let {prog, loc, out, cont} = run(opcode, phase[p], 0);
        programs[p] = prog.slice();
        positions[p] = loc;
    }

    let last = 0;
    let more = true;
    while (more) {
        for (let p = 0; p < phase.length; p++) {
            // Input
            let {prog:prog0, loc:loc0, out:out0, cont:cont0} = run(programs[p], last, positions[p]);
            if (!cont0) {
                return last;
            }
            // Output
            let {prog:prog1, loc:loc1, out:out1, cont:cont1} = run(prog0, null, loc0)
            programs[p] = prog1;
            positions[p] = loc1;
            last = out1;
        }
    }

    for (let p = 0; p < phase.length; p++) {
        let {prog, loc, out, cont} = run(programs[p], null, positions[p]);
        programs[p] = prog;
        positions[p] = loc;
    }
}

function perms(settings) {
    let permList = [];
    generate(settings, []);

    function generate(remaining, used) {
        if (remaining.length == 0) {
            permList.push(used);
        }

        for (let option = 0; option < remaining.length; option++) {
            let newRemaining = remaining.slice();
            let num = newRemaining.splice(option, 1)[0];
            let newUsed = used.slice();
            newUsed.push(num);
            generate(newRemaining, newUsed);
        }
    }
    return permList;
}

function maxSignal(opcode, settings, input) {
    if (settings.length == 0) {
        return input;
    }

    let max = -1;
    for (let opt = 0; opt < settings.length; opt++) {
        let out = parse(opcode, settings[opt], input);
        let rem = remove(settings, opt);
        let score = maxSignal(opcode, rem, out);
        if (score > max) {
            max = score;
        }
    }
    return max;
}

function remove(array, index) {
    let copy = array.slice();
    copy.splice(index, 1);
    return copy;
}

function run(opcode, input, location) {
    let readLoc = location;
    let output; 
    while (readLoc < opcode.length) {
        switch (getCode(opcode[readLoc])) {
            case '99':
                return {prog: opcode, loc: readLoc, out: null, cont: false};
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
                opcode[opcode[readLoc+1]] = input;
                readLoc += 2;
                return {prog: opcode, loc: readLoc, out: null, cont: true}
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                let output = get(opcode, opcode[readLoc+1], instruction[0]);
                readLoc += 2;
                return {prog: opcode, loc: readLoc, out: output, cont: true}
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

/** Parse the opcode, with predefined inputs */
function parse(opcode, phase, signal) {
    let phaseRead = false;
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
                // Read the phase as the first input, signal as the second
                if (!phaseRead) {
                    opcode[opcode[readLoc+1]] = phase;
                    phaseRead = true;
                } else {
                    opcode[opcode[readLoc+1]] = signal;
                }               
                readLoc += 2;
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                return get(opcode, opcode[readLoc+1], instruction[0]);
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