package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("2018/input-1.txt")
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
	sum := 0
	for _, num := range data {
		n, _ := strconv.Atoi(num)
		sum = sum + n
	}
	fmt.Println(sum)

	// Part 2
	sum = 0
	var set = make(map[int]bool)
	out:
	for true {
		for _, num := range data {
			n, _ := strconv.Atoi(num)
			sum = sum + n
			if _, ok := set[sum]; ok {
				fmt.Println(sum)
				break out
			}
			set[sum] = true
		}
	}
}
