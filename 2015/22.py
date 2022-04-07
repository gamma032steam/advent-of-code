# Magic Missile costs 53 mana. It instantly does 4 damage.

# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.

# Shield costs 113 mana. It starts an effect that lasts for 6 turns. 
# While it is active, your armor is increased by 7.

# Poison costs 173 mana. It starts an effect that lasts for 6 turns. 
# At the start of each turn while it is active, it deals the boss 3 damage.

# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. 
# At the start of each turn while it is active, it gives you 101 new mana.

start_my_hp = 50
start_my_mana = 500

start_boss_hp = 55
boss_dmg = 8


from queue import PriorityQueue

# (mana_used, turn, boss_hp, my_hp, my_mana, shield, poison, recharge)
moves = PriorityQueue()
moves.put((0, 0, start_boss_hp, start_my_hp, start_my_mana, 0, 0, 0))

while not moves.empty():
    curr = moves.get()
    mana_used, turn, boss_hp, my_hp, my_mana, shield, poison, recharge = curr

    # apply poison
    if poison > 0:
        boss_hp -= 3
        poison -= 1
    
    # apply recharge
    if recharge > 0:
        my_mana += 101
        recharge -= 1

    # apply part 2
    if turn % 2 == 0:
        my_hp -= 1

    if my_hp <= 0:
        continue
    if boss_hp <= 0:
        print(mana_used)
        exit()

    if turn % 2 == 0:
        # my turn
        if shield > 0:
            shield -= 1
        
        # magic missile
        if my_mana >= 53:
            moves.put((mana_used + 53, turn + 1, boss_hp - 4, my_hp, my_mana - 53, shield, poison, recharge)) 

        # drain
        if my_mana >= 73:
            moves.put((mana_used + 73, turn + 1, boss_hp - 2, my_hp + 2, my_mana - 73, shield, poison, recharge))

        # shield
        if shield == 0 and my_mana >= 113:
            moves.put((mana_used + 113, turn + 1, boss_hp, my_hp, my_mana - 113, 6, poison, recharge))

        # poision
        if poison == 0 and my_mana >= 173:
            moves.put((mana_used + 173, turn + 1, boss_hp, my_hp, my_mana - 173, shield, 6, recharge))

        # recharge
        if recharge == 0 and my_mana >= 229:
            moves.put((mana_used + 229, turn + 1, boss_hp, my_hp, my_mana - 229, shield, poison, 5))

    else:
        # boss turn
        if shield > 0:
            my_hp -= 1
            shield -= 1
        else:
            my_hp -= boss_dmg

        moves.put((mana_used, turn + 1, boss_hp, my_hp, my_mana, shield, poison, recharge))
            