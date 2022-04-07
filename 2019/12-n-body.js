const fs = require('fs');

class Moon {
    constructor([x, y, z]) {
        this.pos = [x, y, z];
        this.v = [0, 0, 0];
    }
}

function main() {
    const input = fs.readFileSync('./input/12-input.txt').toString().split('\r\n').map(e => readInput(e));
    simulate(input);
    console.log(firstRepeat(input));
}

function firstRepeat(input) {
    let xs = [input[0][0], input[1][0], input[2][0], input[3][0]];
    let ys = [input[0][1], input[1][1], input[2][1], input[3][1]];
    let zs = [input[0][2], input[1][2], input[2][2], input[3][2]];
    let xMult = repeatMultiple(xs);
    let yMult = repeatMultiple(ys);
    let zMult = repeatMultiple(zs);
    console.log(xMult, yMult, zMult);
    console.log(lcm3(xMult, yMult, zMult));
}

function simulate(initialPositions) {
    // Set up
    const moons = [];
    const original = [];
    for (let m of initialPositions) {
        moons.push(new Moon(m));
        original.push(m);
    }

    // Step through time
    let time = 1;
    while (time <= 50) {
        //console.log('step', time)
        for (let m = 0; m < moons.length; m++) {
            // Calculate gravity
            for (let j = 0; j < moons.length; j++) {
                if (j != m) {
                    for (let i = 0; i < 3; i++) {
                        moons[m].v[i] += Math.sign(moons[j].pos[i] - moons[m].pos[i]);           
                    }
                }
            }
        }   
        // Move
        for (let m = 0; m < moons.length; m++) {
            for (let i = 0; i < 3; i++) {
                moons[m].pos[i] += moons[m].v[i];
            }
            //console.log(moons[m].pos)
        }
        time++;
    }

    const totalEnergy = moons.map(m => calculateEnergy(m)).reduce((a,b) => a + b, 0);
    console.log('Energy ' + totalEnergy);
}

function repeatMultiple(initPos) {
    let pos = initPos.slice();
    let velocity = [0, 0, 0, 0];
    let step = 1;
    while (step == 1 || !arrayEq(pos,initPos)) {
        //console.log(pos, initPos)
        // Update velocities
        for (let i = 0; i < initPos.length; i++) {
            for (let j = 0; j < initPos.length; j++) {
                if (i != j) {
                    velocity[i] += Math.sign(pos[j] - pos[i]);
                }
            }
        }

        // Update positions
        for (let i = 0; i < initPos.length; i++) {
            pos[i] += velocity[i];
        }
        step++;
    }
    return step;
}

function lcm3(a, b, c) {
    return lcm2(a, lcm2(b,c));
}

function lcm2(a, b) {
    return a*b/gcd(a,b);
}

function gcd(a, b) {
    while (b) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function arrayEq(arr1, arr2) {
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] != arr2[i]) {
            return false;
        }
    }
    return true;
}

function calculateEnergy(moon) {
    const kinetic = moon.v.map(v => Math.abs(v)).reduce((a,b) => a + b, 0);
    const potential = moon.pos.map(v => Math.abs(v)).reduce((a,b) => a + b, 0);
    return kinetic*potential;
}

function readInput(input) {
    const inner = input.slice(1, input.length-1).split(',');
    const vector = [inner[0].slice(2), inner[1].slice(3), inner[2].slice(3)];
    return vector.map(e => parseInt(e));
}
main();