const fs = require('fs');
const assert = require('assert');

const width = 25, height = 6;

function main() {
    // Read in as a string, then convert to an int array
    let input = fs.readFileSync('./input/8-input.txt').toString().split('').map(m => parseInt(m));
    let layers = splitLayers(input);
    problem1(layers);
    let imLayers = splitImgLayers(input);
    let img = align(imLayers);
    render(img);
}

function align(layers) {
    let image = [];
    for (let i = 0; i < height; i++) {
        image[i] = [];
        for (let j = 0; j < width; j++) {
            let pixels = [];
            for (layer = 0; layer < layers.length; layer++) {
                pixels.push(layers[layer][i][j]);
            }
            let visiblePx = pixelAlign(pixels);
            // Not currently handling transparent
            if (visiblePx == 0) {
                visiblePx = ' ';
            } else {
                visiblePx = '■';
            }
            image[i].push(visiblePx);
        }
    }
    return image;
}

function render(image) {
    console.log(image[0])
    for (let i = 0; i < height; i++) {
        assert(image[i].length == width);
        console.log(image[i].join(''));
    }
}

/** Look down the layers for the first coloured pixel */
function pixelAlign(pixels) {
    for (px of pixels) {
        if (px != 2) {
            return px;
        }
    }
    // No B/W pixels, transparent
    return 2;
}

function problem1(layers) {
    let countZeroes = layers.map(l => countDigits(l, 0));
    let minZeroes = Math.min.apply(null, countZeroes);
    let leastZeroes = countZeroes.indexOf(minZeroes);
    console.log(countDigits(layers[leastZeroes], 1) * countDigits(layers[leastZeroes], 2));
}

function countDigits(array, digit) {
    let count = 0;
    for (let item of array) {
        if (item == digit) {
            count++;
        }
    }
    return count;
}

/** Break the file up into an array for each layer */
function splitLayers(file) {
    const size = width * height;
    const nLayers = file.length / size;
    let layers = [];
    for (let i = 0; i < nLayers; i++) {
        let layer = file.slice(i*size, (i+1)*size);
        layers.push(layer);
    }
    return layers;
}


/** Break the file up into a 2D image array for each layer */
function splitImgLayers(file) {
    const size = width * height;
    const nLayers = file.length / size;
    let layers = [];
    for (let i = 0; i < nLayers; i++) {
        let layer = file.slice(i*size, (i+1)*size);
        layers[i] = [];
        for (let j = 0; j < height; j++) {
            let row = layer.slice(j*width, (j+1)*width)
            layers[i].push(row)
        }
    }
    assert(layers.length == nLayers);
    return layers;
}
main();