package main

import (
	"fmt"
	"os"
	"bufio"
	"regexp"
	"strconv"
	"container/heap"
	"sort"
)

type position struct {
	x, y, z int
}

func (p *position) distanceToOrigin() int {
	return abs(p.x) + abs(p.y) + abs(p.z)
}

type bot struct {
	position position
	radius int
}

type area struct {
	lowX, lowY, lowZ, highX, highY, highZ int
	botsInArea int
}

type PriorityQueue []*area

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// max heap
	return pq[i].botsInArea > pq[j].botsInArea
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x any) {
	item := x.(*area)
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	*pq = old[0 : n-1]
	return item
}

func toInt(str string) int {
	i, _ := strconv.Atoi(str) 
	return i
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

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

func manhattanDistance(a position, b position) int {
	return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)
}

func readBot(line string, re *regexp.Regexp) bot {
	matches := re.FindStringSubmatch(line)
	x, y, z, r := toInt(matches[1]), toInt(matches[2]), toInt(matches[3]), toInt(matches[4])
	return bot{position{x, y, z}, r}
}

func readFile() []bot {
	f, err := os.Open("input-23.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var bots []bot

	re := regexp.MustCompile(`pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)`)	
	for scanner.Scan() {
		line := scanner.Text()
		bots = append(bots, readBot(line, re))
	}
	
	return bots
}

// PART 1

func findHighestRadiusBot(bots []bot) bot {
	var bestBot bot
	bestRadius := -1
	for _, bot := range bots {
		if bot.radius > bestRadius {
			bestRadius = bot.radius
			bestBot = bot
		}
	}

	return bestBot
}

func botsInRange(scanningBot bot, bots []bot) (inRange int) {
	for _, bot := range bots {
		if manhattanDistance(scanningBot.position, bot.position) <= scanningBot.radius {
			inRange += 1
		} 
	}
	return
}

// PART 2

// finds the closest point in a linear, inclusive range to a target point
func closestPointInRange(low int, high int, target int) int {
	if target < low {
		return low
	} else if target > high {
		return high
	} else {
		return target
	}
}

func isBotInRangeOfArea(targetArea area, targetBot bot) bool {
	closestX := closestPointInRange(targetArea.lowX, targetArea.highX, targetBot.position.x)
	closestY := closestPointInRange(targetArea.lowY, targetArea.highY, targetBot.position.y)
	closestZ := closestPointInRange(targetArea.lowZ, targetArea.highZ, targetBot.position.z)
	closestPointInArea := position{closestX, closestY, closestZ}
	return manhattanDistance(closestPointInArea, targetBot.position) <= targetBot.radius
}

func countBotsInArea(area area, bots[]bot) (inArea int) {
	for _, bot := range bots {
		if isBotInRangeOfArea(area, bot) {
			inArea += 1
		}
	}
	return
}

// split a cube area into 8 even cubes
func divideArea(areaToDivide area) []area {
	var areas []area
	midX := (areaToDivide.highX + areaToDivide.lowX) / 2
	midY := (areaToDivide.highY + areaToDivide.lowY) / 2
	midZ := (areaToDivide.highZ + areaToDivide.lowZ) / 2
	for _, x := range [][]int{{areaToDivide.lowX, midX},{midX+1, areaToDivide.highX}} {
		for _, y := range [][]int{{areaToDivide.lowY, midY},{midY+1, areaToDivide.highY}} {
			for _, z := range [][]int{{areaToDivide.lowZ, midZ},{midZ+1, areaToDivide.highZ}} {
				if x[0] > x[1] || y[0] > y[1] || z[0] > z[1] {
					continue
				}
				areas = append(areas, area{x[0], y[0], z[0], x[1], y[1], z[1], -1})
			}
		}
	}
	return areas
}

// find the area that covers every bot
func findTotalArea(bots []bot) area {
	var minX, minY, minZ, maxX, maxY, maxZ int
	for _, bot := range bots {
		minX = min(minX, bot.position.x)
		maxX = max(maxX, bot.position.x)
		minY = min(minY, bot.position.y)
		maxY = max(maxY, bot.position.y)
		minZ = min(minZ, bot.position.z)
		maxZ = max(maxZ, bot.position.z)
	}
	return area{minX, minY, minZ, maxX, maxY, maxZ, -1}
}

func isPoint(a area) bool {
	return a.lowX == a.highX && a.lowY == a.highY && a.lowZ == a.highZ
}

func areaToPoint(a area) position {
	return position{a.lowX, a.lowY, a.lowZ}
}

// finds the points in range of the most bots
func bestPoints(bots []bot) []position {
	pq := make(PriorityQueue, 1)
	totalArea := findTotalArea(bots)
	totalArea.botsInArea = countBotsInArea(totalArea, bots)
	pq[0] = &totalArea
	heap.Init(&pq)

	// the number of bots the first singular point has in range
	firstPointCount := -1

	var points []position

	for len(pq) > 0 {
		// pick the area in range of the most bots
		curr := heap.Pop(&pq).(*area)

		if isPoint(*curr) {
			if firstPointCount == -1 {
				firstPointCount = curr.botsInArea
			} else if curr.botsInArea < firstPointCount {
				break
			}
			points = append(points, areaToPoint(*curr))
			continue
		}

		// split the area into smaller areas
		for _, newArea := range divideArea(*curr) {
			newArea.botsInArea = countBotsInArea(newArea, bots)
			areaCopy := newArea
			heap.Push(&pq, &areaCopy)
		}
	}
	return points
}

func sortByDistanceToOrigin(points []position) {
	sort.Slice(points, func(i, j int) bool {
		return points[i].distanceToOrigin() < points[j].distanceToOrigin()
	})
}

func main() {
	bots := readFile()
	
	// part 1
	bestBot := findHighestRadiusBot(bots)
	fmt.Printf("Part 1: %d\n", botsInRange(bestBot, bots))

	// part 2
	candidatePoints := bestPoints(bots)
	sortByDistanceToOrigin(candidatePoints)
	fmt.Printf("Part 2: %d\n", candidatePoints[0].distanceToOrigin())
}