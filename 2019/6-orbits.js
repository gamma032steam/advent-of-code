const fs = require('fs');

class Planet {
    constructor(name) {
        this.name = name;
    }

    satellites = [];
    addSatellite(satellite) {
        satellite.push(satellite);
    }
    addOrbiting(planet) {
        this.orbiting = planet;
    }
}

function main() {
    input = fs.readFileSync('input/6-input.txt').toString().split('\r\n');
    //input = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN'.split(',');
    console.log(countOrbits(input));
    console.log(distance('YOU', 'SAN', input));
}

/** Find the total number of indirect and direct orbits */
function countOrbits(orbits) {
    planets = buildSystem(orbits);
    queue = ['COM', null];
    total = 0;
    level = 0;
    // BFS
    while (queue.length > 1) {
        node = queue.shift();
        // Add a null to indicate new levels
        // https://stackoverflow.com/questions/31247634/how-to-keep-track-of-depth-in-breadth-first-search
        if (node == null) {
            level++;
            queue.push(null);
            continue;
        }
        // The number of orbit associated with this object is equal to its level
        total += level;
        for (sat of planets[node].satellites) {
            queue.push(sat);
        }
    }
    return total;
}

/** Find the distance between two objects */
function distance(obj1, obj2, orbits) {
    planets = buildSystem(orbits);
    // Find the way to both planets
    path1 = pathTo(obj1, planets);
    path2 = pathTo(obj2, planets);
    // Find the latest common planet in the path
    dist = 0;
    while(true) {
        // Go backwards through the path to the first object
        node = path1.pop();
        // Seach for this in the second path
        for (step = 0; step < path2.length; step++) {
            planet = path2[step];
            // Is this a common planet?
            if (planet.name == node.name) {
                // Dist is the count of steps tracing back to the common planet
                // path.length - step - 1 represents the distance to the second object from the
                // common planet
                // Substract 2 as we want to count the jumps to orbit the same planet, not each other
                return dist + (path2.length - step -1) - 2;
            }
        }
        dist++;
    }
}

/** Find the path from the center of mass to an object */
function pathTo(obj, planets) {
    queue = [planets['COM']];
    // BFS pathfinder
    while (queue.length > 0) {
        node = queue.shift();
        if (node.name == obj) {
            break;
        }
        for (sat of node.satellites) {
            sat = planets[sat];
            sat.prev = node;
            queue.push(sat);
        }
    }

    curr = planets[obj];
    path = [curr];
    while (curr.name != 'COM') {
        path.unshift(curr.prev);
        curr = curr.prev;
    }
    return path;
}

/** Build a complete object literal of planets and planet objects */
function buildSystem(orbits) {
    let planets = {};
    // Keep track of all planets in an object
    for (orbit of orbits) {
        orbit = orbit.split(')');
        planet = new Planet(orbit[0]);
        satellite = new Planet(orbit[1]);
        planets[orbit[0].toString()] = planet;
        planets[orbit[1].toString()] = satellite;
    }

    // Link those satellites
    for (orbit of orbits) {
        orbit = orbit.split(')');
        planets[orbit[0].toString()].satellites.push(orbit[1].toString());
    }
    return planets;
} 

main();