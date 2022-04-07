const fs = require('fs');
const TreeMap = require('treemap-js');

function main() {
    let input = fs.readFileSync('./input/10-input.txt').toString().split('\r\n').map(m => m.split(''));
    bestLocation(input);
    vaporise(input, 26, 29);
    //vaporise(input, 8, 3);
}

function bestLocation(map) {
    max = -1;
    best = [];
    // Look through for asteroids
    for (let y = 0; y < map.length; y++) {
        for (let x = 0; x < map[0].length; x++) {
            if (map[y][x] == '#') {
                s = score(map, x, y);
                if (s > max) {
                    max = s;
                    best = [x, y];
                }
            }
        }
    }
    console.log(max, best);
}

function score(map, xLoc, yLoc) {
    visible = 0;
    for (let y = 0; y < map.length; y++) {
        for (let x = 0; x < map[0].length; x++) {
            if (!(x == xLoc && y == yLoc) && map[y][x] == '#') {
                hasCollision = collision(map, xLoc, yLoc, x, y);
                if (!hasCollision) {
                    visible++;
                }
            }
        }
    }
    return visible;
}

function collision(map, xLoc, yLoc, x, y) {
    // x,y is another star that is not the focus
    let dx = x - xLoc, dy = y - yLoc;
    let mult = gcd(Math.abs(dx), Math.abs(dy));
    let sx = dx / mult, sy = dy / mult;
    let lookX = xLoc + sx, lookY = yLoc + sy;
    // Scan in bounds, stepping through to see if there are any asteroids blocking the view
    let collision = false;
    while (lookX >= 0 && lookX < map[0].length && lookY >= 0 && lookY < map.length) {
        if (lookX == x && lookY == y) {
            break;
        }
        if (map[lookY][lookX] == '#') {
            collision = true;
            break;
        }
        lookX += sx;
        lookY += sy;
    }
    return collision;
}

function gcd(a, b) {
    while (b) {
        let t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function vaporise(map, x, y) {
    let bearings = scan(map, x, y);
    let removed = 0;
    while (removed <= 30) {
        bearings.each((points, bearing) => {
            if (points != []) {
                for (let planet = 0; planet < points.length; planet++) {
                    if (map[points[planet][1]][points[planet][0]] == '#' && !collision(map, x, y, points[planet][0], points[planet][1])) {
                        removed++;
                        console.log('Point ' + removed + ' is ' + points[planet][0] + '-' + +points[planet][1] + ' '+ bearing);
                        map[points[planet][1]][points[planet][0]] = '.';
                        break;
                    }
                }
            }
        })
    }
}

function scan(map, xLoc, yLoc) {
    let bearings = new TreeMap();
    for (let y = 0; y < map.length; y++) {
        for (let x = 0; x < map[0].length; x++) {
            if (!(x == xLoc && y == yLoc) && map[y][x] == '#') {
                let bearing = angle(xLoc, yLoc, x, y);
                if (bearings.get(bearing) != null) {
                    bearings.get(bearing).push([x,y]);
                } else {
                    bearings.set(bearing, [[x,y]]);
                }
            }
        }
    }
    return bearings;
}

/** Finds the bearing from point 1 to point 2  */
function angle(x1, y1, x2, y2) {
    // Relative vector delta x, delta y
    let dx = x2-x1, dy = y1-y2;
    // Convert to degrees
    let degs = Math.atan2(dy, dx)*180/Math.PI;
    // Convert negative degrees
    if (degs <= 0) {
        degs += 360; 
    }
    // Switch the direction
    let bearing = 360-degs;
    // Adjust reference plane to be positive y
    if (bearing < 270) {
        // Second, third and fourth quadrants
        bearing += 90;
    } else {
        // First quadrant values
        bearing -= 270;
    }

    return bearing; 
}

main();