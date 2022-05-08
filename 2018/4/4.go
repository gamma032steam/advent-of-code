package main

import (
	"fmt"
	"os"
	"bufio"
	"time"
	"strconv"
	"regexp"
	"sort"
)

type event struct {
	time time.Time
	event string
	guard int
}

func readFile() []string {
	f, err := os.Open("input-4.txt")
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

func organiseLog(data []string) []event {
	re := regexp.MustCompile(`\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\] (.+)`)
	reGuard := regexp.MustCompile(`Guard #(\d+).+`)

	var events []event
	for _, line := range data {
		match := re.FindStringSubmatch(line)
		var dateParts []int
		var eventStr string
		guard := -1
		for i, val := range match {
			if i == 0 {
				continue
			} else if i != len(match) -1 {
				// part of the date
				part, _ := strconv.Atoi(val)
				dateParts = append(dateParts, part)
			} else {
				eventStr = val
				eventMatch := reGuard.FindStringSubmatch(eventStr)
				if eventMatch != nil {
					num, _ := strconv.Atoi(eventMatch[1])	
					guard = num
				}
			}
		}

		time := time.Date(dateParts[0], time.Month(dateParts[1]), dateParts[2], dateParts[3], dateParts[4], 0, 0, time.Local)
		e := event{time, eventStr, guard}
		events = append(events, e)
	}

	sort.Slice(events, func(i, j int) bool {
		return events[i].time.Before(events[j].time)
	})
	return events
}

func trackSleep(log []event) (minutesSlept map[int]int, sleepingTimes map[int][]int) {
	minutesSlept = make(map[int]int)
	sleepingTimes = make(map[int][]int)
	
	currGuard := -1
	sleepMinute := -1

	for _, e := range log {
		if e.guard != -1 {
			currGuard = e.guard
		} else if e.event == "falls asleep" {
			sleepMinute = e.time.Minute()
		} else {
			// add a guard
			if _, ok := minutesSlept[currGuard]; !ok {
				minutesSlept[currGuard] = 0
				mins := make([]int, 60)
				for i := 0; i < 60; i++ {
					mins[i] = 0
				}
				sleepingTimes[currGuard] = mins
			}

			// track the time and duration of the sleep
			wakeMinute := e.time.Minute()
			for t := sleepMinute; t < wakeMinute; t++ {
				sleepingTimes[currGuard][t] += 1
			}
			minutesSlept[currGuard] += wakeMinute - sleepMinute
		}
	}

	return
}

func part1(minutesSlept map[int]int, sleepingTimes map[int][]int) {
	// find the sleepiest guard
	sleepiestGuard := -1
	maxSleepDuration := -1
	for guard, duration := range minutesSlept {
		if duration > maxSleepDuration {
			maxSleepDuration = duration
			sleepiestGuard = guard
		}
	}

	// find the minute they slept the most
	maxSleepMinute := -1
	maxSleepTimes := -1

	for time, freq := range sleepingTimes[sleepiestGuard] {
		if freq > maxSleepTimes {
			maxSleepTimes = freq
			maxSleepMinute = time
		}
	}

	res := maxSleepMinute * sleepiestGuard
	fmt.Printf("%d\n", res)
}

func part2(sleepingTimes map[int][]int) {
	predictableGuard, predictableFreq, predictableMinute := -1, -1, -1

	for guard, freqArray := range sleepingTimes {
		for time, freq := range freqArray {
			if freq > predictableFreq {
				predictableFreq = freq
				predictableMinute = time
				predictableGuard = guard
			}
		}
	}	

	res := predictableGuard * predictableMinute
	fmt.Printf("%d\n", res)
}

func main() {
	data := readFile()
	log := organiseLog(data)
	minutesSlept, sleepingTimes := trackSleep(log)	
	part1(minutesSlept, sleepingTimes)
	part2(sleepingTimes)
}
