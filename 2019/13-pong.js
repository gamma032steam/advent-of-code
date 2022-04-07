const fs = require('fs');
const readline = require('readline-sync');

function main() {
    const input = fs.readFileSync('./input/13-input.txt').toString().split(',').map(m => parseInt(m));
    const game = parse(input);
    // Part 1:
    //render(game);
    play(input);
}

var paddlePos, ballPos;

function play(game) {
    // Manually insert quarter
    game[0] = 2;
    game = addMemory(game);
    
    let grid = {};
    let currProg = game, currLoc = 0, currCont = true, currBase = 0;
    while (currCont) {
        let {prog:prog0, loc:loc0, out:out0, cont:cont0, base:base0} = run(currProg, currLoc, currBase);
        //console.log(prog0, loc0, out0, cont0, base0);
        currCont = cont0;
        currBase = base0;
        currProg = prog0;
        currLoc = loc0;
        let key = out0[0] + '/' + out0[1];
        grid[key] = out0[2];
        draw(grid);
    }
}

function render(game) {
    let tiles = groupThrees(game);
    let grid = {};
    for (t of tiles) {
        let key = t[0] + '/' + t[1];
        grid[key] = t[2];
    }
    draw(grid);
    console.log(count(grid, 2))
}

function count(grid, tileKey) {
    let num = 0;
    for (loc in grid) {
        if (grid[loc] == tileKey) {
            num++;
        }
    }
    return num;
}

function draw(tiles) {
    // Uncomment for a delay between frames
    //sum = 1;
    //for (let i = 0; i <= 10000000; i++) {
    //    sum *= i;
    //}
    let minX = Number.MAX_SAFE_INTEGER, maxX = Number.MIN_SAFE_INTEGER;
    let minY = Number.MAX_SAFE_INTEGER, maxY = Number.MIN_SAFE_INTEGER;
    for (let coord in tiles) {
        let [x, y] = coord.split('/').map(m => parseInt(m));
        if (x < minX) { minX = x; }
        if (x > maxX) { maxX = x; }
        if (y < minY) { minY = y; }
        if (y > maxY) { maxY = y; }
    }
    for (let y = minY; y <= maxY; y++) {
        row = [];
        for (let x = minX; x <= maxX; x++) {
            let key = x.toString() + '/' + y.toString();
            if (tiles[key] == undefined) {
                row.push(' ');
            } else {
                row.push(tileSet(tiles[key]));
                if (tiles[key] == 3) {
                    paddlePos = x;
                } else if (tiles[key] == 4) {
                    ballPos = x;
                }
            }
        }
        console.log(row.join(''));
    }
    if (tiles['-1/0']) {
        console.log('Score ' + tiles['-1/0']);
    }
}

function tileSet(num) {
    switch (num) {
        case 0:
            return ' ';
        case 1:
            return '■';
        case 2:
            return '+';
        case 3:
            return '-';
        case 4:
            return 'O'; 
    }
}

function groupThrees(array) {
    const out = [];
    for (let i = 0; i < array.length; i +=3 ) {
        out.push(array.slice(i, i+3));
    }
    return out;
}

// INTCODE INTERPRETER - STEPS

function run(opcode, loc, base) {
    let triple = [];
    let readLoc = loc, relativeBase = base;
    while (readLoc < opcode.length) {
        switch (getCode(opcode[readLoc])) {
            case '99':
                return {prog: opcode, loc: readLoc, out: null, cont: false, base: relativeBase};
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
                //let read = readline.question("Input: ");
                let read;
                if (ballPos == paddlePos) {
                    read = 0;
                } else if (ballPos > paddlePos) {
                    read = 1;
                } else {
                    read = -1;
                }
                opcode = put(opcode, opcode[readLoc+1], parseInt(read), instruction[0], relativeBase);
                readLoc += 2;
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                let output = get(opcode, opcode[readLoc+1], instruction[0], relativeBase);
                readLoc += 2;
                triple.push(output);
                if (triple.length == 3) {
                    return {prog: opcode, loc: readLoc, out: triple, cont: true, base: relativeBase};
                }
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
    return {prog: opcode, loc: readLoc, out: null, cont: false};
}

// INTCODE INTERPRETER - WHOLE

function parse(opcode) {
    let output = [];
    let readLoc = 0, relativeBase = 0;
    while (readLoc < opcode.length) {
        switch (getCode(opcode[readLoc])) {
            case '99':
                return output;
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
                output.push(get(opcode, opcode[readLoc+1], instruction[0], relativeBase));
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