package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type group struct {
	army           string
	id             int
	units          int
	hp             int
	weaknesses     []string
	immunities     []string
	damageType     string
	damage         int
	initiative     int
	effectivePower int
}

type attackMove struct {
	target group
	attacker group
}

func (g *group) CalculatePower() {
	g.effectivePower = g.damage * g.units
}

// returns (immune, infection) tuple
func readGroups(input []string, boost int) ([]group, []group) {
	var immuneGroups []group
	var infectionGroups []group

	army := "immune"
	id := 1
	for _, line := range input {
		if line == "Immune System:" || line == "Infection:" {
			continue
		}
		if line == "" {
			// move to the next army
			army = "infection"
			id = 1
			continue
		}

		var group group
		if army == "infection" {
			group = readGroup(line, 0)
		} else {
			group = readGroup(line, boost)
		}
		group.id = id
		group.army = army
		id += 1
		if army == "immune" {
			immuneGroups = append(immuneGroups, group)
		} else {
			infectionGroups = append(infectionGroups, group)
		}
	}

	return immuneGroups, infectionGroups
}

func readGroup(line string, boost int) group {
	group := group{}

	// read all the numbers
	reNumeric := regexp.MustCompile(`(\d+) units each with (\d+) hit points.*with an attack that does (\d+) .* damage at initiative (\d+)`)
	numericMatch := reNumeric.FindStringSubmatch(line)
	for i, val := range numericMatch {
		if i == 0 {
			continue
		}
		num, _ := strconv.Atoi(val)
		if i == 1 {
			group.units = num
		} else if i == 2 {
			group.hp = num
		} else if i == 3 {
			group.damage = num + boost
		} else if i == 4 {
			group.initiative = num
		}
	}

	// read immunities and weaknesses - read the string, then split on ", "
	reImmunities := regexp.MustCompile(`.*immune to (.*)\)`)
	immunitiesMatch := reImmunities.FindStringSubmatch(line)

	reImmunitiesSemicolon := regexp.MustCompile(`.*immune to (.*);`)
	immunitiesMatchSemicolon := reImmunitiesSemicolon.FindStringSubmatch(line)

	// prefer semicolon match over ) match
	if len(immunitiesMatchSemicolon) > 1 {
		immunitiesMatch = immunitiesMatchSemicolon
	}

	var immunities []string
	if len(immunitiesMatch) > 1 {
		immunities = strings.Split(immunitiesMatch[1], ", ")
	}
	group.immunities = immunities

	reWeaknesses := regexp.MustCompile(`.*weak to (.*)\)`)
	weaknessesMatch := reWeaknesses.FindStringSubmatch(line)

	reWeaknessesSemicolon := regexp.MustCompile(`.*weak to (.*);`)
	weaknessesMatchSemicolon := reWeaknessesSemicolon.FindStringSubmatch(line)

	if len(weaknessesMatchSemicolon) > 1 {
		weaknessesMatch = weaknessesMatchSemicolon
	}

	var weaknesses []string
	if len(weaknessesMatch) > 1 {
		weaknesses = strings.Split(weaknessesMatch[1], ", ")
	}
	group.weaknesses = weaknesses

	// damage type
	reDamageType := regexp.MustCompile(`.*\d+ (\w+) damage`)
	group.damageType = reDamageType.FindStringSubmatch(line)[1]

	group.CalculatePower()
	return group
}

func readFile() []string {
	f, err := os.Open("input-24.txt")
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

// return true if immune wins
func play(immune []group, infection []group) bool {
	for {
		var totalKilled int
		immune, infection, totalKilled = playRound(immune, infection)
		if totalKilled == 0 || isWarDone(immune, infection) {
			return len(immune) > 0 && totalKilled != 0
		}		
	}
}

func countArmyUnits(army []group) (sum int) {
	for _, g := range army {
		sum += g.units
	}
	return
}

func isWarDone(immune []group, infection []group) bool {
	if len(immune) == 0 {
		fmt.Printf("Infection wins with %d units remaining\n", countArmyUnits(infection))
		return true
	} else if len(infection) == 0 {
		fmt.Printf("Immune wins with %d units remaining\n", countArmyUnits(immune))
		return true
	}
	return false
}

// sort groups by decreasing effective power, initiative
func sortByTurnPriority(groups []group) {
	sort.Slice(groups, func(i, j int) bool {
		if groups[i].effectivePower != groups[j].effectivePower {
			return groups[i].effectivePower > groups[j].effectivePower
		}
		return groups[i].initiative > groups[j].initiative
	})
}

func removeGroupFromArray(groups []group, groupToRemove group) []group {
	for i, group := range groups {
		if groupToRemove.id == group.id {
			groups = append(groups[:i], groups[i+1:]...)
		}
	}
	return groups
}

func playRound(immune []group, infection []group) ([]group, []group, int) {
	sortByTurnPriority(immune)
	sortByTurnPriority(infection)

	var attacks []attackMove
	attacks = append(attacks, selectTargets(immune, infection)...)
	attacks = append(attacks, selectTargets(infection, immune)...)
	return performAttacks(immune, infection, attacks)
}

func sortByInitiative(attacks []attackMove) {
	sort.Slice(attacks, func(i, j int) bool {
		return attacks[i].attacker.initiative >= attacks[j].attacker.initiative
	})
}

func findGroup(group group, groups []group) (*group, int) {
	for i, g := range groups {
		if g.id == group.id {
			return &g, i
		}
	}
	return nil, -1
}

func performAttacks(immune []group, infection []group, attacks []attackMove) ([]group, []group, int) {
	totalKilled := 0
	sortByInitiative(attacks)
	for _, attack := range attacks {
		var targetArmy, attackerArmy []group
		if attack.target.army == "immune" {
			targetArmy = immune
			attackerArmy = infection
		} else {
			targetArmy = infection
			attackerArmy = immune
		}

		attacker, _ := findGroup(attack.attacker, attackerArmy)		 
		if attacker == nil {
			continue
		}

		target, targetIdx := findGroup(attack.target, targetArmy)
		damage := calculateDamage(*attacker, *target)
		// kill enemy units
		killedUnits := damage / targetArmy[targetIdx].hp
		totalKilled += killedUnits
		targetArmy[targetIdx].units -= killedUnits
		// remove the group if they're all gone
		if targetArmy[targetIdx].units <= 0 {
			targetArmy = append(targetArmy[:targetIdx], targetArmy[targetIdx+1:]...)
			if attack.target.army == "immune" {
				immune = targetArmy
			} else {
				infection = targetArmy
			}
			continue
		}
		// recalculate effective power
		targetArmy[targetIdx].CalculatePower()
	}
	return immune, infection, totalKilled
}

func selectTargets(attackers []group, targets []group) (attacks []attackMove) {
	// calculate immune system attacks
	enemies := make([]group, len(targets))
	copy(enemies, targets)
	for _, group := range attackers {
		if len(enemies) == 0 {
			break
		}
		enemyToAttack := pickEnemy(group, enemies)
		if calculateDamage(group, enemyToAttack) == 0 {
			continue
		}
		enemies = removeGroupFromArray(enemies, enemyToAttack)
		attack := attackMove{target: enemyToAttack, attacker: group}
		attacks = append(attacks, attack)
	}
	return
}

// calculate the potential damage you can do
func calculateDamage(attacker group, target group) int {
	for _, immunity := range target.immunities {
		if attacker.damageType == immunity {
			return 0
		}
	}

	isWeak := false
	for _, weakness := range target.weaknesses {
		if attacker.damageType == weakness {
			isWeak = true
			break
		}
	}

	damage := attacker.damage * attacker.units
	if isWeak {
		damage *= 2
	}
	return damage
}

// sort groups by decreasing damage, effective power, initiative
func sortByAttackPriority(attacker group, groups []group) {
	sort.Slice(groups, func(i, j int) bool {
		damageToI := calculateDamage(attacker, groups[i])
		damageToJ := calculateDamage(attacker, groups[j])
		if damageToI != damageToJ {
			return damageToI > damageToJ
		}

		if groups[i].effectivePower != groups[j].effectivePower {
			return groups[i].effectivePower > groups[j].effectivePower
		}

		return groups[i].initiative > groups[j].initiative
	})
}

// pick an enemy to attack out of a list of possible options
func pickEnemy(attacker group, enemies []group) group {
	sortByAttackPriority(attacker, enemies)
	return enemies[0]
}

func main() {
	data := readFile()
	immune, infection := readGroups(data, 0)
	play(immune, infection)

	fmt.Printf("Part 2:\n")
	// part 2
	// bsearch over boost
	lo, hi := 0, 100000
	for lo < hi {
		boost := (lo + hi) / 2
		immune, infection := readGroups(data, boost)
		didWin := play(immune, infection)
		if didWin {
			hi = boost
		} else {
			lo = boost + 1
		}
		if lo == hi {
			break
		}
	}
}
