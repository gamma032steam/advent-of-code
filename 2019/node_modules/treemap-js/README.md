# TreeMap.js
A binary tree based map (aka dictionary) data type for Javascript, keeping keys sorted at all times. Provides `O(log n)` average case performance for inserting, retrieving and removing values.

## Installation
Works with Node and in the browser.

### Node
Install via `npm install treemap-js`. Then access the TreeMap like this:

```javascript
const TreeMap = require("treemap-js");
```

### Browser
Include `TreeMap.js` in your HTML. `TreeMap` is automatically appended to the `window` object.

## Usage
```javascript
var map = new TreeMap();

map.set("my first key", "hello");    // keys can be strings, numbers or booleans. Values can be any data type
map.set("second key", [ 1, 3, 4 ]);
map.get("my first key");    // returns "hello"

map.set("my first key", 2342);
map.get("my first key");    // returns 2342

map.getLength();    //  returns 2

map.getMinKey();    // returns "my first key"
map.getMaxKey();    // returns "second key"

map.each(function (value, key) {
    // do something...
});

map.remove("my first key");
map.getLength();    // returns 1

map.getTree();    // returns the backing tree object
```
