package main

import (
	"fmt"
	"os"
	"bufio"
	"regexp"
	"sort"
	"strings"
)

type node struct {
	name string
}

type edge struct {
	from, to node
}

type job struct {
	worker int
	timeRemaining int
	task node
}

func (n *node) timeToComplete() int {
	for _, c := range n.name {
		return int(c - 'A') + 1
	}
	return -1
} 

const BASE_TIME = 60
const WORKERS = 5

// sort with largest characters first
func sortAlphabetically(nodes []node) {
	sort.Slice(nodes, func(i, j int) bool {
		return nodes[i].name > nodes[j].name
	})
}

func readEdge(line string, re *regexp.Regexp) edge {
	match := re.FindStringSubmatch(line)
	return edge{from: node{match[1]}, to: node{match[2]}}
}

// builds an adjacency list and inbound count
func buildGraph(edges []edge) (map[node]int, map[node][]node) {
	inbound := make(map[node]int)
	graph := make(map[node][]node)

	for _, e := range edges {
		// inbound count
		inbound[e.to] += 1

		// adjacency list
		if _, ok := graph[e.from]; !ok {
			graph[e.from] = []node{}
		}
		if _, ok := graph[e.to]; !ok {
			graph[e.to] = []node{}
		}
		graph[e.from] = append(graph[e.from], e.to)
	}
	return inbound, graph
}

func topSort(inbound map[node]int, graph map[node][]node) []node {
	// initial stack is nodes with 0 inbound
	var stack []node
	for u, _ := range graph {
		if _, ok := inbound[u]; !ok {
			stack = append(stack, u)
		}
	}

	var order []node
	for len(stack) > 0 {
		// pick smallest alphabetical option from stack
		sortAlphabetically(stack)
		u := stack[len(stack) - 1]
		stack = stack[:len(stack) - 1]

		order = append(order, u)
		for _, v := range graph[u] {
			inbound[v] -= 1
			if inbound[v] == 0 {
				stack = append(stack, v)
			}
		}
	}
	return order
}

func printNodeOrder(nodes []node) {
	var sb strings.Builder
	for _, node := range nodes {
		sb.WriteString(node.name)
	}
	fmt.Printf("Part 1: %s\n", sb.String())
}

func readFile() []edge {
	f, err := os.Open("input-7.txt")
	if err != nil {
		fmt.Println(err)
	}

	scanner := bufio.NewScanner(f)

	var data []edge
	re := regexp.MustCompile(`Step (.) must be finished before step (.) can begin.`)

	for scanner.Scan() {
		data = append(data, readEdge(scanner.Text(), re))
	}
	
	return data
}

func timeToComplete(inbound map[node]int, graph map[node][]node) {
	// initial stack is nodes with 0 inbound
	var stack []node
	for u, _ := range graph {
		if _, ok := inbound[u]; !ok {
			stack = append(stack, u)
		}
	}

	// track what each worker's jobs
	time := -1
	assignedJobs := make(map[int]*job)

	for len(stack) > 0 || len(assignedJobs) > 0 {
		// 1 second passes
		time += 1
		for worker, job := range assignedJobs {
			job.timeRemaining -= 1
			if job.timeRemaining == 0 {
				// job is complete, dependent tasks are unblocked
				for _, v := range graph[job.task] {
					inbound[v] -= 1
					if inbound[v] == 0 {
						stack = append(stack, v)
					}
				}
				delete(assignedJobs, worker)
			}
		}

		// if workers are able, they can take something off the stack
		sortAlphabetically(stack)

		for worker := 0; worker < WORKERS; worker ++ {
			if len(stack) == 0 {
				continue
			}
			if _, ok := assignedJobs[worker]; !ok {
				// pick smallest alphabetical option from stack
				task := stack[len(stack) - 1]
				stack = stack[:len(stack) - 1]
				assignedJobs[worker] = &job{worker: worker, task: task, timeRemaining: BASE_TIME + task.timeToComplete()}
			}
		}		

	}
	fmt.Printf("Part 2: %d\n", time)
}

func main() {
	data := readFile()
	
	// part 1
	inbound, graph := buildGraph(data)
	order := topSort(inbound, graph)
	printNodeOrder(order)
	inbound, graph = buildGraph(data)
	timeToComplete(inbound, graph)
}