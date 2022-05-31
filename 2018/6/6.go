package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type coord struct {
	x int
	y int
}

type closest struct {
	distance int
	closest int
	tied     bool
}

const maxDistance = 10000

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func readFile() []coord {
	f, err := os.Open("input-6.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)

	var data []coord

	for scanner.Scan() {
		line := scanner.Text()
		coordinates := strings.Split(line, ", ")
		x, _ := strconv.Atoi(coordinates[0])
		y, _ := strconv.Atoi(coordinates[1])
		data = append(data, coord{x: x, y: y})
	}

	return data
}

func findBounds(coords []coord) (minX int, maxX int, minY int, maxY int) {
	minX, maxX = coords[0].x, coords[0].x
	minY, maxY = coords[0].y, coords[0].y
	for _, c := range coords {
		minX = int(min(minX, c.x))
		maxX = int(max(maxX, c.x))
		minY = int(min(minY, c.y))
		maxY = int(max(maxY, c.y))
	}
	return
}

func manhattanDistance(a coord, b coord) int {
	return abs(a.x-b.x) + abs(a.y-b.y)
}

func distances(coords []coord) {
	minX, maxX, minY, maxY := findBounds(coords)
	closeToAll := 0

	// figure out what's closest to what in a 2d grid
	grid := make([][]*closest, maxY-minY+1)
	for i := minY; i <= maxY; i++ {
		grid[i-minY] = make([]*closest, maxX-minX+1)
		for j := minX; j <= maxX; j++ {
			grid[i-minY][j-minX] = nil
			currentCoord := coord{x: j, y: i}
			totalDistance := 0
			// calculate the distance to every coordinate
			for k, c := range coords {
				distance := manhattanDistance(c, currentCoord)
				totalDistance += distance
				if grid[i-minY][j-minX] == nil || grid[i-minY][j-minX].distance > distance {
					grid[i-minY][j-minX] = &closest{distance: distance, tied: false, closest: k}
				} else if grid[i-minY][j-minX].distance == distance {
					grid[i-minY][j-minX].tied = true
				}
			}
			if totalDistance < maxDistance {
				closeToAll += 1
			}
		}
	}

	// do a count to see which coordinate has the most matches
	count := make(map[int]int)
	invalid := make(map[int]bool)

	for i := minY; i <= maxY; i++ {
		for j := minX; j <= maxX; j++ {
			tile := grid[i-minY][j-minX]
			// disclude any coordinate with an edge tile
			if i == minY || i == maxY || j == minX || j == maxX {
				invalid[tile.closest] = true
			}
			// tied tiles don't count
			if tile.tied {
				continue
			}
			if _, ok := count[tile.closest]; !ok {
				count[tile.closest] = 0
			}
			count[tile.closest] += 1
		}
	}

	largest := -1
	for key, value := range count {
		if _, ok := invalid[key]; ok {
			continue
		}
		largest = max(largest, value)
	}

	fmt.Printf("Part 1: %d\n", largest)
	fmt.Printf("Part 2: %d\n", closeToAll)
}

func main() {
	data := readFile()
	distances(data)
}
