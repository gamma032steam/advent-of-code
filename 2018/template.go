package main

import (
	"fmt"
	"os"
	"bufio"
)

func main() {
	f, err := os.Open("2018/input-0.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var data []string

	for scanner.Scan() {
		data = append(data, scanner.Text())
	}
	
}
