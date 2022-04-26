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
	f, err := os.Open("2018/3/input-3.txt")
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
		for i := x + 1; i <= x + width; i++ {
			for j := y + 1; j <= y + height; j++ {
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

	// Part 2
	doesClaimOverlap := make(map[int]bool)
	// store the claim ids for each tile
	tiles := make(map[pair][]int)

	for _, claim := range data {
		var id, x, y, width, height int
		fmt.Sscanf(claim, "#%d @ %d,%d: %dx%d", &id, &x, &y, &width, &height)
		doesClaimOverlap[id] = false
		// generate all the coordinates relative to the top-left															
		for i := x + 1; i <= x + width; i++ {
			for j := y + 1; j <= y + height; j++ {
				p := pair{i, j}
				for _, overlap_id := range tiles[p] {
					doesClaimOverlap[overlap_id] = true
				}
				if len(tiles[p]) > 0 {
					doesClaimOverlap[id] = true
				}
				
				// add the current id
				if _, ok := tiles[p]; !ok {
					tiles[p] = []int{id}
				} else {
					tiles[p] = append(tiles[p], id)
				}
			}
		}
	}

	// look for the claim with no overlap
	for id, doesOverlap := range doesClaimOverlap {
		if (!doesOverlap) {
			fmt.Println(id)
			break
		}
	}
}
