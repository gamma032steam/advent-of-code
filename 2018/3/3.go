package main

import (
	"fmt"
	"os"
	"bufio"
)

type pair struct {
	x int
	y int
}

func main() {
	f, err := os.Open("2018/input-3.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var data []string

	for scanner.Scan() {
		data = append(data, scanner.Text())
	}

	// Part 1
	seenOnce := make(map[pair]bool)
	overlap := make(map[pair]bool)

	for _, claim := range data {
		// input comes in as #1 @ 850,301: 23x12
		var id, x, y, width, height int
		fmt.Sscanf(claim, "#%d @ %d,%d: %dx%d", &id, &x, &y, &width, &height)
		// generate all the coordinates relative to the top-left															
		for i := x; i <= x + width; i++ {
			for j := y; y <= y + height; j++ {
				p := pair{i, j}
				if _, ok := seenOnce[p]; ok {
					overlap[p] = true
				}
				seenOnce[p] = true
			}
		}
	}

	// count the overlap
	println(len(overlap))
}
