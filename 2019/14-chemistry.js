const fs = require('fs');

function main() {
    const input = fs.readFileSync('./input/14-input.txt').toString().split('\r\n').map(r => r.split(' => ').map(e => e.split(', ')));
    console.log(oreRequired(input));
    rank(input)
}

/** Ranks materials from how far they are from ORE */
function rank(input) {
    let reactions = input.slice();
    while (reactions.length > 0) {
        
    }
}

/** Finds the number of ore for 1 fuel */
function oreRequired(reactions) {
    const reactionMap = buildReactionMap(reactions);
    let materials = ['1 FUEL'], last = [];
    // Continue reacting until we reach the base
    while (!arrayEq(materials, last)) {
        last = materials.slice();
        // Try to reduce each
        // Start from empty to avoid more than one step at once
        let newMats = [];
        for (let i = 0; i < materials.length; i++) {
            newMats = newMats.concat(reduceMat(materials[i], reactionMap, false));
        } 
        materials = groupCommon(newMats);
    }
    console.log(materials);
    // Now force the remainder until only ore is left
    last = [];
    while (!arrayEq(materials, last)) {
        last = materials.slice();
        // Try to reduce each
        // Start from empty to avoid more than one step at once
        let newMats = [];
        for (let i = 0; i < materials.length; i++) {
            newMats = newMats.concat(reduceMat(materials[i], reactionMap, true));
        } 
        materials = groupCommon(newMats);
    }
    console.log(materials);
}

/** Find the reaction to make this material */
function reduceMat(material, map, force) {
    // Calculate how many times the reaction needs to be performed
    let nAvailable = parseInt(material.split(' ')[0]), nReaction, output = null;
    for (let reaction in map) {
        if (material.split(' ')[1] == reaction.split(' ')[1]) {
            //console.log(material.split(' ')[1]);
            output = map[reaction].slice();
            nReaction = parseInt(reaction.split(' ')[0]);
        }
    }
    let nReactions = Math.floor(nAvailable/nReaction);
    // Can't react: Not enough reactant or no reaction to do
    if (!force) {
        if (nAvailable < nReaction) {
            return [material];
        }
    }

    if (force) {
        nReactions = Math.ceil(nAvailable/nReaction);
    }

    if (output == null) {
        return [material];
    }

    for (let i = 0; i < output.length; i++) {
        let [n, e] = output[i].split(' ');
        n = parseInt(n) * nReactions;
        output[i] = n.toString() + ' ' + e;
    }
    let leftover = nAvailable % nReaction;
    if (!force && leftover != 0) {
        output.push(leftover.toString() + ' ' + material.split(' ')[1]);
    }

    return output;
}

/** Combine idential elements into one element */
function groupCommon(elements) {
    let final = [];
    for (let i = 0; i < elements.length; i++) {
        found = false;
        // Look for the element in the new list
        for (let j = 0; j < final.length; j++) {
            if (final[j].split(' ')[1] == elements[i].split(' ')[1]) {
                // Join
                let [n, e] = final[j].split(' ');
                n = parseInt(n) + parseInt(elements[i].split(' ')[0]);
                final[j] = n.toString() + ' ' + e;
                found = true;
                break;
            }
        }
        if (!found) {
            // Add
            final.push(elements[i]);
        }
    }
    return final;
}

/** Builds a hashmap of the reactions in reverse */
function buildReactionMap(reactions) {
    reactionMap = {};
    for (let reaction of reactions) {
        reactionMap[reaction[1][0]] = reaction[0];
    }
    return reactionMap;
}

function arrayEq(arr1, arr2) {
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] != arr2[i]) {
            return false;
        }
    }
    return true;
}

main();