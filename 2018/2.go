package main

import (
	"fmt"
	"os"
	"bufio"
)

func main() {
	f, err := os.Open("2018/input-2.txt")
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
	twos := 0
	threes := 0

	for _, id := range data {
		var characterCount = make(map[rune]int)
		for _, char := range id {
			if _, ok := characterCount[char]; ok {
				characterCount[char] += 1
			} else {
				characterCount[char] = 1
			}
		}
		
		hasTwos := false
		hasThrees := false
		
		for _, v := range characterCount {
			if v == 2 {
				hasTwos = true
			} else if v == 3 {
				hasThrees = true
			}
		}

		if hasTwos {
			twos += 1
		}
		if hasThrees {
			threes += 1
		}
	}

	checksum := twos * threes
	fmt.Println(checksum)

	// Part 2
	// Do this the O(n) way

	seen := make(map[string]bool)

	out:
	for _, id := range data {
		for i := 0; i < len(id); i++ {
			new_string := id[:i] + "*" + id[i+1:]
			if _, ok := seen[new_string]; ok {
				fmt.Println(new_string)
				break out
			}
			seen[new_string] = true
		}
	}
}
