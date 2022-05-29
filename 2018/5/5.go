package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
	"unicode"
)

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func readFile() string {
	f, err := os.Open("input-5.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var data string

	for scanner.Scan() {
		data = scanner.Text()
	}
	
	return data
}

func collapse(input string) string {
	for {
		oldLen := len(input)
		for c := 'a'; c <= 'z'; c++ {
			input = strings.Replace(input, string([]rune{c, unicode.ToUpper(c)}), "", -1) 
			input = strings.Replace(input, string([]rune{unicode.ToUpper(c), c}), "", -1) 

		}
		if oldLen == len(input) {
			break
		}
	}
	return input
}

func main() {
	// read the input string
	data := readFile()
	input := data

	// part 1
	fmt.Printf("Part 1: %d\n", len(collapse(input)))

	// part 2
	smallest := math.MaxInt32
	for c := 'a'; c <= 'z'; c++ {
		newString := strings.Clone(input)
		newString = strings.Replace(newString, string(c), "", -1)
		newString = strings.Replace(newString, string(unicode.ToUpper(c)), "", -1)
		smallest = min(smallest, len(collapse(newString)))
	}
	fmt.Printf("Part 2: %d\n", smallest)
}