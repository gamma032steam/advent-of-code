package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func B2i(b bool) int {
	if b {
		return 1
	}
	return 0
}

func consider(rules [][][]int, i int, candidates []string, seen map[string]bool) []string {
	candidateString := strings.Join(candidates[:], ",")
	num := strconv.Itoa(i)
	candidateString = num + candidateString
	if _, ok := seen[candidateString]; ok {
		return make([]string, 0)
	}
	seen[candidateString] = true

	if i == len(rules) {
		return candidates
	}
	// find the valid mapping via backtracking
	options := getOptions(rules[i])
	opcode := rules[i][1][0]

	for _, option := range options {
		// skip if the option has already been used in a different position,
		// or the opcode position has already been assigned
		bad := false
		for i, val := range candidates {
			if i == opcode {
				if !(val == option || val == "") {
					bad = true
					break
				} 
			} else if val == option {
				bad = true
				break
			}
		}
		if bad {
			continue
		}

		candidates[opcode] = option
		ans := consider(rules, i+1, candidates, seen)
		if len(ans) > 0 {
			return ans
		}
		candidates[opcode] = ""
	}
	return make([]string, 0)
}

func getOptions(rule [][]int) []string {
	var ops []string
	beforeValA := rule[1][1]
	beforeRegA := rule[0][rule[1][1]]

	beforeValB := rule[1][2]
	beforeRegB := rule[0][rule[1][2]]

	C := rule[1][3]
	afterC := rule[2][C]

	if afterC == beforeRegA+beforeRegB {
		ops = append(ops, "addr")
	}
	if afterC == beforeRegA+beforeValB {
		ops = append(ops, "addi")
	}
	if afterC == beforeRegA*beforeRegB {
		ops = append(ops, "mulr")
	}
	if afterC == beforeRegA*beforeValB {
		ops = append(ops, "muli")
	}
	if afterC == beforeRegA&beforeRegB {
		ops = append(ops, "banr")
	}
	if afterC == beforeRegA&beforeValB {
		ops = append(ops, "bani")
	}
	if afterC == beforeRegA|beforeRegB {
		ops = append(ops, "borr")
	}
	if afterC == beforeRegA|beforeValB {
		ops = append(ops, "bori")
	}
	if afterC == beforeRegA {
		ops = append(ops, "setr")
	}
	if afterC == beforeValA {
		ops = append(ops, "seti")
	}
	if afterC == B2i(beforeValA > beforeRegB) {
		ops = append(ops, "gtir")
	}
	if afterC == B2i(beforeRegA > beforeValB) {
		ops = append(ops, "gtri")
	}
	if afterC == B2i(beforeRegA > beforeRegB) {
		ops = append(ops, "gtrr")
	}
	if afterC == B2i(beforeValA == beforeRegB) {
		ops = append(ops, "eqir")
	}
	if afterC == B2i(beforeRegA == beforeValB) {
		ops = append(ops, "eqri")
	}
	if afterC == B2i(beforeRegA == beforeRegB) {
		ops = append(ops, "eqrr")
	}
	return ops
}

func readArray(str string, re *regexp.Regexp) []int {
	match := re.FindStringSubmatch(str)
	var array []int
	for i, val := range match {
		if i == 0 {
			continue
		}
		num, _ := strconv.Atoi(val)
		array = append(array, num)
	}

	return array
}

func run(mapping []string, prog [][]int, i int, registers []int) {
	if i == len(prog) {
		return
	}

	line := prog[i]
	beforeValA := line[1]
	beforeRegA := registers[line[1]]

	beforeValB := line[2]
	beforeRegB := registers[line[2]]

	c := line[3]

	operation := mapping[line[0]]
	switch operation {
	case "addr":
		registers[c] = beforeRegA + beforeRegB
	case "addi":
		registers[c] = beforeRegA + beforeValB
	case "mulr":
		registers[c] = beforeRegA * beforeRegB
	case "muli":
		registers[c] = beforeRegA * beforeValB
	case "banr":
		registers[c] = beforeRegA & beforeRegB
	case "bani":
		registers[c] = beforeRegA & beforeValB
	case "borr":
		registers[c] = beforeRegA | beforeRegB
	case "bori":
		registers[c] = beforeRegA | beforeValB
	case "setr":
		registers[c] = beforeRegA
	case "seti":
		registers[c] = beforeValA
	case "gtir":
		registers[c] = B2i(beforeValA > beforeRegB)
	case "gtri":
		registers[c] = B2i(beforeRegA > beforeValB)
	case "gtrr":
		registers[c] = B2i(beforeRegA > beforeRegB)
	case "eqir":
		registers[c] = B2i(beforeValA == beforeRegB)
	case "eqri":
		registers[c] = B2i(beforeRegA == beforeValB)
	case "eqrr":
		registers[c] = B2i(beforeRegA == beforeRegB)
	}

	run(mapping, prog, i+1, registers)
}

func main() {
	f, err := os.Open("./input-16.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var data []string
	for scanner.Scan() {
		data = append(data, scanner.Text())
	}

	// build the 3d array
	var rules [][][]int

	reArray := regexp.MustCompile(`\[(\d+), (\d+), (\d+), (\d+)\]`)
	reOp := regexp.MustCompile(`^(\d+) (\d+) (\d+) (\d+)$`)

	i := 0
	for i < len(data) {
		var parts [][]int

		var before, op, after []int

		before = readArray(data[i][8:], reArray)
		op = readArray(data[i+1], reOp)
		after = readArray(data[i+2][8:], reArray)

		parts = append(parts, before, op, after)

		rules = append(rules, parts)

		i += 4
	}

	// part 1
	moreThanThreeOps := 0
	for i, _ := range rules {
		validOps := getOptions(rules[i])
		if len(validOps) >= 3 {
			moreThanThreeOps++
		}
	}
	fmt.Printf("ans: %d\n", moreThanThreeOps)

	// part 2
	assignment := make([]string, 16)
	seen := make(map[string]bool)
	mapping := consider(rules, 0, assignment, seen)
	fmt.Printf("%q\n", mapping)
	
	f2, err := os.Open("./input2-16.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f2.Close()

	scanner2 := bufio.NewScanner(f2)

	var prog [][]int
	for scanner2.Scan() {
		line := scanner2.Text()
		prog = append(prog, readArray(line, reOp))
	}
	reg := []int{0, 0, 0, 0}
	run(mapping, prog, 0, reg)
	fmt.Printf("%v\n", reg)
}
