package main

import (
	"fmt"
	"container/heap"
)

type pair struct {
	x int
	y int
}

type situation struct {
	tool string
	position pair
}

type state struct {
	distance int
	tool string
	position pair
}

type PriorityQueue []*state

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].distance < pq[j].distance
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x any) {
	item := x.(*state)
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	*pq = old[0 : n-1]
	return item
}


func getGeo() [][]int {
	targetX := 9
	targetY := 796
	tX := targetX + 100
	tY := targetY + 100
	depth := 6969

	// depth := 510
	// tX := 30
	// tY := 30
	// targetX := 10
	// targetY := 10

	geo := make([][]int, (tY+1))
	for i := range geo {
		geo[i] = make([]int, (tX+1))
	}

	// set up known values
	for y := 0; y <= tY; y++ {
		geo[y][0] = y * 48271
	}
	for x := 0; x <= tX; x++ {
		geo[0][x] = x * 16807
	}

	// fill in X-1,Y * X,Y-1 rule
	for y := 1; y <= tY; y++ {
		for x := 1; x <= tX; x++ {
			geo[y][x] = ((geo[y-1][x] + depth) % 20183) * ((geo[y][x-1] + depth) % 20183)
		}
	}

	geo[targetY][targetX] = 0
	return geo
}


func main() {
	// part 1
	geo := getGeo()
	fmt.Printf("%v", geo)

	targetX := 9
	targetY := 796
	tX := targetX + 100
	tY := targetY + 100
	depth := 6969

	// depth := 510
	// tX := 30
	// tY := 30
	// targetX := 10
	// targetY := 10


	risk := 0
	// convert to ero and sum risk
	for y := 0; y <= tY; y++ {
		for x := 0; x <= tX; x++ {
			geo[y][x] = ((geo[y][x] + depth) % 20183) % 3
			risk += geo[y][x]
		}
	}
	fmt.Println(risk)
	fmt.Printf("%v", geo)

	// part 2 - dijkstra's
	init := state{distance: 0, tool: "torch", position: pair{0, 0}}
	pq := make(PriorityQueue, 1)
	pq[0] = &init
	heap.Init(&pq)
	
	best := map[situation]int{{position: pair{0, 0}, tool: "torch"}: 0}

	for len(pq) > 0 {
		if len(pq) % 1500 == 0 {
			fmt.Println(len(pq))
		}

		curr := heap.Pop(&pq).(*state)
		currSit := situation{position: curr.position, tool: curr.tool}
		if best[currSit] < curr.distance {
			continue
		}

		var candidates []state
		// switching to a valid tool
		currTileType := geo[curr.position.y][curr.position.x]
		validGear := make([]string, 2)

		if currTileType == 0 {
			// rocky
			validGear[0] = "climbing"
			validGear[1] = "torch"
		} else if currTileType == 1 {
			// wet
			validGear[0] = "climbing"
			validGear[1] = "neither"
		} else {
			// narrow
			validGear[0] = "neither"
			validGear[1] = "torch"
		}

		for _, gear := range validGear {
			if gear != curr.tool {
				candidates = append(candidates, state{position: curr.position, tool: gear, distance: curr.distance + 7})
			}
		}

		// moving
		dirs := []pair{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
		for _, dir := range dirs {
			newPos := pair{curr.position.x + dir.x, curr.position.y + dir.y}
			// check if out of bounds
			if newPos.x < 0 || newPos.x > tX || newPos.y < 0 || newPos.y > tY {
				continue
			}

			// check if we don't have the right gear
			newTileType := geo[newPos.y][newPos.x]
			var badGear string
			if newTileType == 0 {
				// rocky
				badGear = "neither"
			} else if newTileType == 1 {
				// wet
				badGear = "torch"
			} else {
				// narrow
				badGear = "climbing"
			}
			if (curr.tool == badGear) {
				continue
			}

			candidates = append(candidates, state{position: newPos, tool: curr.tool, distance: curr.distance + 1})
		}

		for _, cand := range candidates {
			sit := situation{position: cand.position, tool: cand.tool}
			if b, ok := best[sit]; !ok || b > cand.distance {
				c := cand
				heap.Push(&pq, &c)
				best[sit] = cand.distance
			} 
		}
	}

	fmt.Println(best[situation{tool: "torch", position: pair{targetX, targetY}}])
}