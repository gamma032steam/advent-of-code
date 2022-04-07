const fs = require('fs');

/** Read the input file and pass it into the algorithm */
function main() {
    let input = fs.readFileSync('./input/1-input.txt').toString().split('\n');
    console.log('Q1: ' + fuelShip(input));
    console.log('Q2: ' + fuelTotalShip(input));
}

/** Solve Q1 */
function fuelShip(masses) {
    // Map masses to fuel requirement and sum
    return masses.map(m => fuelModule(m)).reduce((a, b) => a + b, 0);
}

/** Solve Q2 */
function fuelTotalShip(masses) {
    return masses.map(m => fuelTotalModule(m)).reduce((a, b) => a + b, 0);
}

/** Calculate fuel cost of a module (Q1) */
function fuelModule(mass) {
    return (Math.floor(mass/3) - 2);
}

/** Calculate the fuel cost of a module and its fuel (Q2) */
function fuelTotalModule(mass) {
    let totalFuel = 0;
    let fuelReq = fuelModule(mass);

    while (fuelReq > 0) {
        totalFuel += fuelReq;
        // Recursively calculate the fuel required for this fuel
        fuelReq = fuelModule(fuelReq);
    }
    return totalFuel;
}

/** Put Q1 into one line, just for fun */
function oneline() {
    console.log(fs.readFileSync('./input/1-input.txt').toString().split('\n').map(m => Math.floor(m/3)-2).reduce((a, b) => a + b, 0));
}

main()