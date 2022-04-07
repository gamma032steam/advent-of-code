const fs = require('fs');
const readline = require('readline-sync');

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/11-input.txt').toString().split(',').map(m => parseInt(m));
    let prog = addMemory(input);
    const tiles = paint(prog);
    render(tiles);
}

function paint(program) {
    // Colour of tiles
    const tiles = {};
    // Direction to step
    let direction = 'up';
    // Current position
    let x = 0, y = 0;
    // Program variables
    let currLoc = 0, currBase = 0;
    tiles['0/0'] = 1;
    while (true) {
        let key = x.toString() + '/' + y.toString();
        let tile;
        if (!tiles[key]) {
            // Never painted, so it's black
            tile = 0;            
        } else {
            tile = tiles[key];
        }
        // Feed in current colour  
        //console.log(program, currLoc, tile);
        let {prog: prog0, loc: loc0, out: out0, cont: cont0, base: base0} = parse(program, currLoc, tile, currBase);
        //console.log(prog0, loc0, out0, cont0)
        tiles[key] = out0;
        let {prog: prog1, loc: loc1, out: out1, cont: cont1, base: base1} = parse(prog0, loc0, null, base0);   
        //console.log(prog1, loc1, out1, cont1)
        currLoc = loc1;
        currBase = base1;
        program = prog1;
        if (cont1 == false) {
            break;
        }

        if (out1 == 0) {
            direction = turnLeft(direction);
        } else {
            direction = turnRight(direction);
        }

        switch (direction) {
            case 'up':
                y += 1;
                break;
            case 'right':
                x += 1;
                break;
            case 'down':
                y -= 1;
                break;
            case 'left':
                x -= 1;
        }
        
    }
    console.log('Tiles painted:', Object.keys(tiles).length);
    return tiles;
}

function render(tiles) {
    let minX = Number.MAX_SAFE_INTEGER, maxX = Number.MIN_SAFE_INTEGER;
    let minY = Number.MAX_SAFE_INTEGER, maxY = Number.MIN_SAFE_INTEGER;
    for (let coord in tiles) {
        let [x, y] = coord.split('/').map(m => parseInt(m));
        if (x < minX) { minX = x; }
        if (x > maxX) { maxX = x; }
        if (y < minY) { minY = y; }
        if (y > maxY) { maxY = y; }
    }
    console.log(minX, maxX, minY, maxY)
    for (let y = maxY; y >= minY; y--) {
        row = [];
        for (let x = minX; x <= maxX; x++) {
            let key = x.toString() + '/' + y.toString();
            if (tiles[key] == undefined) {
                row.push(' ');
            } else {
                if (tiles[key] == '0') {
                    row.push(' ');
                } else {
                    row.push('■')
                }
            }
        }
        console.log(row.join(''));
    }
}

function turnLeft(direction) {
    switch (direction) {
        case 'up':
            return 'left';
        case 'left':
            return 'down';
        case 'down':
            return 'right';
        case 'right':
            return 'up';
    }
}

function turnRight(direction) {
    switch (direction) {
        case 'up':
            return 'right';
        case 'right':
            return 'down';
        case 'down':
            return 'left';
        case 'left':
            return 'up';
    }
}

function parse(opcode, loc, input, base) {
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
                opcode = put(opcode, opcode[readLoc+1], parseInt(input), instruction[0], relativeBase);
                readLoc += 2;
                break;
                }
            case '04':
                {
                // Output
                let instruction = prependZero(opcode[readLoc], 3);
                let output = get(opcode, opcode[readLoc+1], instruction[0], relativeBase);
                readLoc += 2;
                return {prog: opcode, loc: readLoc, out: output, cont: true, base: relativeBase};
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