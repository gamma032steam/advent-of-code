#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define WIDTH 32
#define HEIGHT 32

#define HP 200
// part 2: just do a manual binary search with this number
#define ELF_ATTACK 34
#define GOBLIN_ATTACK 3

#define NOT_ENTITY -10000
#define HIGH_NUM 10000

#define HEALTH_DEBUG 1

void print_game(char game[HEIGHT][WIDTH], int health[HEIGHT][WIDTH])
{
    for (int i = 0; i < HEIGHT; i++)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            if (HEALTH_DEBUG == 1 && (game[i][j] == 'G' || game[i][j] == 'E'))
            {
                printf("%d ", health[i][j]);
            }
            else
            {
                printf("%c ", game[i][j]);
            }
        }
        printf("\n");
    }
}

void read_game(char game[HEIGHT][WIDTH], int health[HEIGHT][WIDTH], FILE *fptr)
{
    for (int i = 0; i < HEIGHT; i++)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            char c;
            if (fscanf(fptr, " %c", &c) != 1)
            {
                printf("bad char");
                exit(1);
            }
            game[i][j] = c;
            if (c == 'G' || c == 'E')
            {
                health[i][j] = HP;
            }
            else
            {
                health[i][j] = NOT_ENTITY;
            }
        }
    }
}

int valid_position(int i, int j)
{
    return i >= 0 && i < HEIGHT && j >= 0 && j < WIDTH;
}

int game_done(char game[HEIGHT][WIDTH])
{
    int e_cnt = 0;
    int g_cnt = 0;
    for (int i = 0; i < HEIGHT; i++)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            char c = game[i][j];
            if (c == 'E')
            {
                e_cnt++;
            }
            else if (c == 'G')
            {
                g_cnt++;
            }
        }
    }
    if (e_cnt == 0) {
        printf("Goblins win with %d remaining!\n", g_cnt);
    } else if (g_cnt == 0) {
        printf("Elves win with %d remaining!\n", e_cnt);
    }

    return e_cnt == 0 || g_cnt == 0;
}

int remaining_hitpoints(int health[HEIGHT][WIDTH])
{
    int total = 0;
    for (int i = 0; i < HEIGHT; i++)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            int hp = health[i][j];
            if (hp > 0)
            {
                total += hp;
            }
        }
    }
    return total;
}

void get_adjacent(int out[2][4])
{
    // returns two parallel arrays, in reading order.
    // up
    out[0][0] = -1;
    out[1][0] = 0;

    // left
    out[0][1] = 0;
    out[1][1] = -1;

    // right
    out[0][2] = 0;
    out[1][2] = 1;

    // down
    out[0][3] = 1;
    out[1][3] = 0;
}

void perform_attack(int i, int j, char game[HEIGHT][WIDTH], int health[HEIGHT][WIDTH])
{
    // actually does the attack on an enemy at (i, j). hits the enemy and kills it if it's dead.
    int attack;
    if (game[i][j] == 'G') {
        attack = ELF_ATTACK;
    } else {
        attack = GOBLIN_ATTACK;
    }
    health[i][j] -= attack;
    if (health[i][j] <= 0)
    {
        health[i][j] = NOT_ENTITY;
        game[i][j] = '.';
    }
}

char find_other_type(int i, int j, char game[HEIGHT][WIDTH])
{
    char target;
    if (game[i][j] == 'G')
    {
        return 'E';
    }
    else if (game[i][j] == 'E')
    {
        return 'G';
    }
    else
    {
        printf("trying to move something that's not an entity");
        exit(1);
    }
}

int attack(int i, int j, char game[HEIGHT][WIDTH], int health[HEIGHT][WIDTH])
{
    // tries to attack. returns 0 if there was no target.
    int adj[2][4];
    get_adjacent(adj);
    char target = find_other_type(i, j, game);

    int best_i = HIGH_NUM, best_j = HIGH_NUM, best_hp = HIGH_NUM;
    // search adjacent
    for (int k = 0; k < 4; k++)
    {
        int target_i = i + adj[0][k], target_j = j + adj[1][k];

        if (valid_position(target_i, target_j) == 0)
        {
            continue;
        }

        if (game[target_i][target_j] != target)
        {
            continue;
        }

        int enemy_hp = health[target_i][target_j];
        if (enemy_hp == NOT_ENTITY)
        {
            printf("found an enemy that's not an enemy");
            exit(1);
        }

        if (enemy_hp < best_hp)
        {
            best_i = target_i;
            best_j = target_j;
            best_hp = enemy_hp;
        }
    }
    // no valid targets
    if (best_hp == HIGH_NUM)
    {
        return 0;
    }
    perform_attack(best_i, best_j, game, health);

    return 1;
}

void find_target(int i, int j, char game[HEIGHT][WIDTH], char target, int out[3])
{
    // finds a target. prefer closest enemies, then reading order.

    // 0 if unseen, 1 if seen
    int seen[HEIGHT][WIDTH] = {{0}};
    seen[i][j] = 1;

    int i_queue[HEIGHT * WIDTH];
    i_queue[0] = i;
    int j_queue[HEIGHT * WIDTH];
    j_queue[0] = j;
    int first_element = 0, last_element = 0;

    int best_i = HIGH_NUM, best_j = HIGH_NUM;

    int adj[2][4];
    get_adjacent(adj);

    // run a bfs
    int found = 0;
    while (found == 0 && first_element <= last_element)
    {
        // do one level of the bfs
        int start = first_element, end = last_element + 1;
        for (int k = start; k < end; k++)
        {
            int curr_i = i_queue[k], curr_j = j_queue[k];
            //  found an enemy

            if (game[curr_i][curr_j] == target)
            {
                // choose best by reading order
                if (curr_i < best_i || (curr_i == best_i && curr_j < best_j))
                {
                    best_i = curr_i;
                    best_j = curr_j;
                    found = 1;
                }
            }

            // search adjacent
            if (game[curr_i][curr_j] != '.' && !(curr_i == i && curr_j == j))
            {
                continue;
            }
            for (int k = 0; k < 4; k++)
            {
                int target_i = curr_i + adj[0][k], target_j = curr_j + adj[1][k];
                if (valid_position(target_i, target_j) == 0)
                {
                    continue;
                }

                if (seen[target_i][target_j] == 1)
                {
                    continue;
                }

                last_element += 1;
                i_queue[last_element] = target_i;
                j_queue[last_element] = target_j;
                seen[target_i][target_j] = 1;
            }
        }

        first_element = end;
    }
    //  found one
    out[0] = 1;
    out[1] = best_i;
    out[2] = best_j;

    // game done
    if (found == 0)
    {
        out[0] = 0;
        return;
    }
}

void shortest_path(int i, int j, int goal_i, int goal_j, char game[HEIGHT][WIDTH], int new_pos[2])
{
    // another BFS
    // 0 if unseen, 1 if seen
    int dist[HEIGHT][WIDTH];
    for (int x = 0; x < HEIGHT; x++) {
        for (int y = 0; y < WIDTH; y++) {
            dist[x][y] = HIGH_NUM;
        }
    }

    int i_queue[HEIGHT * WIDTH];
    i_queue[0] = goal_i;
    int j_queue[HEIGHT * WIDTH];
    j_queue[0] = goal_j;
    int first_element = 0, last_element = 0;

    int adj[2][4];
    get_adjacent(adj);

    // run a bfs
    int distance = 0;
    while (first_element <= last_element)
    {
        // do one level of the bfs
        int start = first_element, end = last_element + 1;
        for (int k = start; k < end; k++)
        {
            int curr_i = i_queue[k], curr_j = j_queue[k];

            if (game[curr_i][curr_j] == '.' || (curr_i == goal_i && curr_j == goal_j))
            {
                dist[curr_i][curr_j] = distance;
            }
            else
            {
                continue;
            }

            // get adjacent
            for (int k = 0; k < 4; k++)
            {
                int target_i = curr_i + adj[0][k], target_j = curr_j + adj[1][k];
                if (valid_position(target_i, target_j) == 0)
                {
                    continue;
                }

                if (dist[target_i][target_j] != HIGH_NUM)
                {
                    continue;
                }

                last_element += 1;
                i_queue[last_element] = target_i;
                j_queue[last_element] = target_j;
                dist[target_i][target_j]++;
            }
        }
        first_element = end;
        distance += 1;
    }

    // now get the best candidate
    int best_i, best_j;
    int best_dist = HIGH_NUM;
    for (int k = 0; k < 4; k++)
    {
        int target_i = i + adj[0][k], target_j = j + adj[1][k];
        if (valid_position(target_i, target_j) == 0)
        {
            continue;
        }
        if (dist[target_i][target_j] < best_dist)
        {
            best_i = target_i;
            best_j = target_j;
            best_dist = dist[target_i][target_j];
        }
    }

    new_pos[0] = best_i;
    new_pos[1] = best_j;

    if (best_dist == HIGH_NUM) {
        // don't move
        new_pos[0] = i;
        new_pos[1] = j;
    }
}

int move(int i, int j, char game[HEIGHT][WIDTH], int health[HEIGHT][WIDTH], int new_pos[2])
{
    // given the (i, j) of a G or E, make a step towards the closest enemy.
    // assumes there are no immediately adjacent enemies.
    char target = find_other_type(i, j, game);
    int out[3];
    find_target(i, j, game, target, out);
    if (out[0] == 0)
    {
        new_pos[0] = i;
        new_pos[1] = j;
        return 0;
    }


    shortest_path(i, j, out[1], out[2], game, new_pos);

    game[new_pos[0]][new_pos[1]] = game[i][j];
    health[new_pos[0]][new_pos[1]] = health[i][j];
    game[i][j] = '.';
    health[i][j] = NOT_ENTITY;

    return 1;
}

int main(int argc, char **argv)
{
    // read the game board
    FILE *fptr;

    if ((fptr = fopen("input.txt", "r")) == NULL)
    {
        printf("Error! opening file");

        // Program exits if the file pointer returns NULL.
        exit(1);
    }

    char game[HEIGHT][WIDTH];
    int health[HEIGHT][WIDTH];
    read_game(game, health, fptr);
    print_game(game, health);

    int round = 0;
    while (1) {
        int used_turn[HEIGHT][WIDTH] = {{0}};
        for (int i = 0; i < HEIGHT; i++)
        {
            for (int j = 0; j < WIDTH; j++)
            {
                if ((game[i][j] == 'G' || game[i][j] == 'E') && used_turn[i][j] == 0)
                {
                    // perform a turn

                    // try to attack from where the unit is
                    int moved = attack(i, j, game, health);
                    if (moved == 1)
                    {
                        used_turn[i][j] = 1;
                        continue;
                    }
                    // otherwise, move towards the nearest enemy
                    int new_pos[2];
                    move(i, j, game, health, new_pos);

                    // move-attack
                    attack(new_pos[0], new_pos[1], game, health);
                    
                    used_turn[new_pos[0]][new_pos[1]] = 1;

                    // game done?
                    if (game_done(game) == 1) {
                        int outcome = remaining_hitpoints(health) * round;
                        printf("final score: %d\n", outcome);
                        print_game(game, health);
                        exit(0);
                    }

                }
            }
        }
        round++;
        printf("Turn %d\n", round);
        print_game(game, health);
    }
}