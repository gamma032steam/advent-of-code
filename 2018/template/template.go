package main

import (
	"fmt"
	"os"
	"bufio"
)

func readFile() []string {
	f, err := os.Open("input-0.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var data []string

	for scanner.Scan() {
		data = append(data, scanner.Text())
	}
	
	return data
}

func main() {
	data := readFile()
	fmt.Print(data)	
}