// Swap L17 from doubleDigits to doubleOnly for Q2

const inputLow = 240298;
const inputHigh = 784956;

function main() {
    console.log('Q1/2: ' + validPasswords().length);
}

/** Returns a list of valid passwords */
function validPasswords() {
    passwords = [];
    // Step through the entire integer range
    for (test = inputLow; test <= inputHigh; test++) {
        // Break up the number to a list of ints
        testArray = test.toString().split('').map(n => parseInt(n));
        if (ascendingDigits(testArray) && doubleDigits(testArray)) {
            passwords.push(test);
        }
    }
    return passwords;
}

/** Enforces ascending rule */
function ascendingDigits(password) {
    for (i = 0; i < (password.length-1); i++) {
        if (password[i] > password[i+1]) {
            return false;
        }
    }
    return true;
}

/** Enforces double rule */
function doubleDigits(password) {
    for (i = 0; i < (password.length-1); i++) {
        if (password[i] == password[i+1]) {
            return true;
        }
    }
    return false;
}

/** Enforces adjacent digits */
function doubleOnly(password) {
    // Count number sequences
    let count = 1;
    let number = password[0];
    for (i = 1; i < password.length; i++) {
        if (number == password[i]) {
            count++;
        } else {
            // Check for a double before moving on
            if (count == 2) {
                return true;
            }
            // Start a new count
            count = 1;
            number = password[i];
        }
    }
    if (count == 2) {
        return true;
    }
    return false;
}

main();