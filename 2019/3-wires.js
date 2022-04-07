// O(N) algorithm for both questions

const fs = require('fs');

class Coordinate {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    move(direction) {
        switch (direction) {
            case 'L':
                this.x -= 1;
                break;
            case 'R':
                this.x += 1;
                break;
            case 'U':
                this.y += 1;
                break;
            case 'D':
                this.y -= 1;
        }
    }

    toString() {
        return (this.x + '/' + this.y);
    }
}

function main() {
    input = fs.readFileSync('./input/3-input.txt').toString().split('\n').map(p => p.split(','));
    intersection(...input);
}

/** Find the closest intersection between two wires */
function intersection(wire1, wire2) {
    path1 = trace(wire1);
    path2 = trace(wire2);
    console.log('Via manhattan:' + closestIntersection(path1, path2));
    console.log('Via steps: ' + smallestDelay(path1, path2));
}

/** Find the points traversed from a list of instructions */
function trace(vectors) {
    let points = {};
    let currentPosition = new Coordinate(0, 0);
    let steps = 0;
    let instructions = vectors.map(v => parseInstruction(v));

    while (instructions.length > 0) {
        currentPosition.move(instructions[0].direction);
        steps++;
        // Only keep the first write
        if (!points[currentPosition]) {
            // Store the number of steps as the key (Q2)
            points[currentPosition] = steps;
        }
        instructions[0].magnitude -= 1;
        if (instructions[0].magnitude == 0) {
            instructions.shift();
        }
    }

    return points;
}

/** Reads an instruction in */
function parseInstruction(instruction) {
    let direction = instruction.charAt(0);
    let magnitude = parseInt(instruction.slice(1));
    return {'direction': direction, 'magnitude': magnitude};
}

/** Finds the distance to the closest intersection via Manhattan distance */
function closestIntersection(path1, path2) {
    let closest = Number.MAX_SAFE_INTEGER;
    for (coord in path1) {
        if (path2[coord]) {
            coordComponents = coord.split('/').map(x => parseInt(x));
            // Manhattan
            distance = Math.abs(coordComponents[0]) + Math.abs(coordComponents[1]);
            if (distance < closest) {
                closest = distance;
            }
        }
    }

    return closest;
}

/** Finds the distance to the closest intersection, via number of steps */
function smallestDelay(path1, path2) {
    let closest = Number.MAX_SAFE_INTEGER;
    for (coord in path1) {
        if (path2[coord]) {
            distance = path1[coord] + path2[coord];
            if (distance < closest) {
                closest = distance;
            }
        }
    }

    return closest;
}

main();