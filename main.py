import math
import random


class Card:
    def __init__(self, name="", atk=0.0, defense=0.0, hexagram_atk=0, hexagram_def=0, hp=0.0, max_hp_add=0,
                 max_hp_reduce=0, qi_cost=0, qi_add=0,
                 hexagram_add=0, starpower_add=0,
                 internalinjury_add=0, hexagram=False, post_action=False, star_point=False, alt_card=None,
                 regeneration_add=0, formacide_add=0, cittadharma_add=0, guard_up=0,
                 consumed=False,
                 chase=False, level=1, repeat=1, strikes=1):
        self.max_hp_reduce = max_hp_reduce
        self.star_point = star_point
        self.alt_card = alt_card
        self.post_action = post_action
        self.consumed = consumed
        self.hexagram = hexagram
        self.hexagram_def = hexagram_def
        self.hexagram_atk = hexagram_atk
        self.strikes = strikes
        self.repeat = repeat
        self.regeneration_add = regeneration_add
        self.guard_up = guard_up
        self.chase = chase
        self.level = level
        self.cittadharma_add = cittadharma_add
        self.formacide_add = formacide_add
        self.max_hp_add = max_hp_add
        self.hp = hp
        self.internalinjury_add = internalinjury_add
        self.starpower_add = starpower_add
        self.hexagram_add = hexagram_add
        self.qi_add = qi_add
        self.name = name
        self.atk = atk
        self.defense = defense
        self.qi_cost = qi_cost


class Player:
    def __init__(self, name, destiny, cultivation, max_hp, cards, regeneration=0, internal_injury=0, starpower=0, hexagram=0, defense=0, guard_up=0):
        # TODO: starting hexagram etc.
        self.name = name
        self.destiny = destiny
        self.cultivation = cultivation
        self.max_hp = max_hp
        self.star_points = [2, 5]
        self.cards = cards

        self.regeneration = regeneration
        self.internal_injury = internal_injury
        self.starpower = starpower
        self.hexagram = hexagram
        self.defense = defense
        self.qi = 0
        self.hp = self.max_hp
        self.guard_up = guard_up
        self.cittadharma = 0
        self.formacide = 0
        self.sword_intent = 0
        self.attack = 0
        self.slot = 0
        self.played_cards = [0, 0, 0, 0, 0, 0, 0, 0]

    def reset_status(self):
        self.regeneration = 0
        self.internal_injury = 0
        self.starpower = 0
        self.hexagram = 0
        self.defense = 0
        self.qi = 0
        self.hp = self.max_hp
        self.guard_up = 0
        self.cittadharma = 0
        self.formacide = 0


def choose_starting_player(player1, player2):
    starting_player = None
    second_player = None
    if player1.cultivation > player2.cultivation:
        starting_player = player1
        second_player = player2
    if player1.cultivation < player2.cultivation:
        starting_player = player2
        second_player = player1
    if player1.cultivation == player2.cultivation:
        starting_player, second_player = random.sample([player1, player2], 2)

    return starting_player, second_player


def check_wincon(active_player, inactive_player, turn):
    if inactive_player.hp <= 0:
        print("")
        print("")
        print(active_player.name + " wins after " + str(int(turn)) + " turns")
        return True
    if active_player.hp <= 0:
        print("")
        print("")
        print(inactive_player.name + " wins after " + str(int(turn)) + " turns")
        return True
    else:
        return False


def resolve_card(active_player, inactive_player, card):
    # Get card from player deck

    # Skip consume and continuous cards
    if card.consumed and active_player.played_cards[active_player.slot % 8] == 1:
        active_player.slot += 1
        ncard = active_player.cards[active_player.slot % 8]
        resolve_card(active_player, inactive_player, ncard)
    else:
        # Check qi cost
        if card.qi_cost > active_player.qi:
            print(active_player.name + " waits for qi")
            active_player.qi += 1
            active_player.hp += active_player.cittadharma
            return
        active_player.qi -= card.qi_cost
        # Repeat attacks (Five thunder)
        print(active_player.name + " uses " + card.name)
        i = 0
        while i < card.repeat:
            damage = 0
            defense = 0
            healing = 0
            boost = active_player.sword_intent + active_player.attack
            # Star Point logic
            if card.post_action and active_player.played_cards[active_player.slot % 8 == 1]:
                card = card.alt_card
            if active_player.slot % 8 in active_player.star_points:
                boost += active_player.starpower
                if card.star_point:
                    card = card.alt_card
            # Hexagram logic
            if card.hexagram and active_player.hexagram > 0:
                for _ in range(card.strikes):
                    damage = boost + card.hexagram_atk
                    if damage > 0:
                        deal_damage(damage, inactive_player)
                        print(card.name + " deals " + str(damage) + " damage")
                defense += card.hexagram_def
                active_player.hexagram -= 1
                # TODO other hexagram effects (hp) (also hexagram should decrease for each instance of randomness)
            else:
                for _ in range(card.strikes):
                    damage = boost + card.atk
                    if damage > 0:
                        deal_damage(damage, inactive_player)
                        print(card.name + " deals " + str(damage) + " damage")
                defense += card.defense
            # formacide add
            active_player.formacide += card.formacide_add
            # formacide dmg
            active_player.hexagram += card.hexagram_add
            damage = card.hexagram_add * active_player.formacide
            if damage > 0:
                deal_damage(damage, inactive_player)
                print(card.name + " deals " + str(damage) + " damage")

            # citta-dharma
            healing += card.qi_add * active_player.cittadharma
            healing += card.hp
            active_player.qi += card.qi_add
            # defense
            active_player.defense += defense
            # max hp
            active_player.max_hp += card.max_hp_add
            inactive_player.max_hp -= card.max_hp_reduce
            inactive_player.hp = min(inactive_player.max_hp, inactive_player.hp)
            # healing
            active_player.hp = min(active_player.max_hp, active_player.hp + healing)

            active_player.played_cards[active_player.slot % 8] = 1
            i += 1

        active_player.slot += 1
        if card.chase:
            print(card.name + " chases")
            ncard = active_player.cards[active_player.slot % 8]
            resolve_card(active_player, inactive_player, ncard)


def deal_damage(damage, damaged_player):
    damaged_player.defense -= damage
    if damaged_player.defense <= 0:
        damage_after_def = 0 - damaged_player.defense
        damaged_player.defense = 0
        reduce_hp(damage_after_def, damaged_player)
    return damage


def reduce_hp(damage, damaged_player):
    if damaged_player.guard_up <= 0:
        damaged_player.hp -= damage
    else:
        print(damaged_player.name + " consumes a stack of Guard Up")
        damaged_player.guard_up -= 1


def simulate_battle(player1, player2, turns=100):
    active_player, inactive_player = choose_starting_player(player1, player2)
    turn = 1
    for a in range(turns):
        # Start of turn
        print("Start of turn " + str(turn))
        active_player.hp = min(active_player.hp + active_player.regeneration, active_player.max_hp)
        if active_player.internal_injury > 0:
            reduce_hp(active_player.internal_injury, active_player)
        active_player.defense = math.floor(active_player.defense / 2)
        if check_wincon(active_player, inactive_player, turn):
            break
        # Resolve card
        card = active_player.cards[active_player.slot % 8]
        resolve_card(active_player, inactive_player, card)

        # Print
        print_battle_status(player1, player2)
        if check_wincon(active_player, inactive_player, turn):
            break
        # End of turn
        if check_wincon(active_player, inactive_player, turn):
            break
        print("-----------------------------------------")
        # Change active player
        b = active_player
        active_player = inactive_player
        inactive_player = b
        turn += .5
    active_player.reset_status()
    inactive_player.reset_status()


def print_battle_status(player1, player2):
    hp_bar1 = '=' * int((player1.hp / player1.max_hp * 30)) if player1.max_hp != 0 else ""
    hp_bar2 = '=' * int((player2.hp / player2.max_hp * 30)) if player2.max_hp != 0 else ""

    print(f"{player1.name} has {player1.hp:.1f}hp left [{hp_bar1:30}]")
    print(f"{player2.name} has {player2.hp:.1f}hp left [{hp_bar2:30}]")


normal_attack = Card("Normal Attack", 3, level=1)

# HEPTASTAR PAVILION
# MEDITATION PHASE
shifting_stars_1 = Card("Shifting Stars", 5, level=1)
shifting_stars_2 = Card("Shifting Stars", 8, level=2)
shifting_stars_3 = Card("Shifting Stars", 8, level=3)
# TODO add star points

dotted_around_1 = Card("Dotted Around", qi_add=1, starpower_add=1, defense=2, level=1)
dotted_around_2 = Card("Dotted Around", qi_add=2, starpower_add=1, defense=3, level=2)
dotted_around_3 = Card("Dotted Around", qi_add=1, starpower_add=2, defense=4, level=3)

# VIRTUOSO PHASE

thunder_hexagram_rythm_1 = Card("Thunder Hexagram Rythm", atk=4.5, hexagram_atk=9, hexagram=True, hexagram_add=3,
                                level=1)
thunder_hexagram_rythm_2 = Card("Thunder Hexagram Rythm", atk=5, hexagram_atk=10, hexagram=True, hexagram_add=4,
                                level=2)
thunder_hexagram_rythm_3 = Card("Thunder Hexagram Rythm", atk=5.5, hexagram_atk=11, hexagram=True, hexagram_add=5,
                                level=3)

# IMMORTALITY PHASE
astral_move_fly_1 = Card(name="Astral Move - Fly", chase=True, atk=2, strikes=2, level=1)
astral_move_fly_2 = Card(name="Astral Move - Fly", chase=True, atk=4, strikes=2, level=2)
astral_move_fly_3 = Card(name="Astral Move - Fly", chase=True, atk=6, strikes=2, level=3)
# TODO

hexagram_formacide_1 = Card(name="Hexagram Formacide", formacide_add=3, consumed=True, level=1)
hexagram_formacide_2 = Card(name="Hexagram Formacide", formacide_add=4, consumed=True, level=2)
hexagram_formacide_3 = Card(name="Hexagram Formacide", formacide_add=5, consumed=True, level=3)

flame_hexagram_1 = Card(name="Flame Hexagram", hexagram_add=3, max_hp_reduce=2, level=1)
flame_hexagram_2 = Card(name="Flame Hexagram", hexagram_add=4, max_hp_reduce=4, level=2)
flame_hexagram_3 = Card(name="Flame Hexagram", hexagram_add=5, max_hp_reduce=6, level=3)

dance_of_the_dragonfly_1 = Card(name="Dance of the Dragonfly", hexagram=True, chase=True, hexagram_atk=5, atk=0,
                                level=1)
dance_of_the_dragonfly_2 = Card(name="Dance of the Dragonfly", hexagram=True, chase=True, hexagram_atk=9, atk=0,
                                level=2)
dance_of_the_dragonfly_3 = Card(name="Dance of the Dragonfly", hexagram=True, chase=True, hexagram_atk=13, atk=0,
                                level=3)

dance_of_the_dragonfly_1_NO_CHASE = Card(name="Dance of the Dragonfly", atk=5, level=1)
dance_of_the_dragonfly_2_NO_CHASE = Card(name="Dance of the Dragonfly", atk=9, level=2)
dance_of_the_dragonfly_3_NO_CHASE = Card(name="Dance of the Dragonfly", atk=13, level=3)
# TODO HEXAGRAM CHASE

thunder_and_lightning_1 = Card(name="Thunder and Lightning", atk=5, hexagram_atk=10, repeat=2, hexagram_add=True,
                               qi_add=1, level=1)
thunder_and_lightning_2 = Card(name="Thunder and Lightning", atk=6.5, hexagram_atk=13, repeat=2, hexagram_add=True,
                               qi_add=1, level=2)
thunder_and_lightning_3 = Card(name="Thunder and Lightning", atk=8, hexagram_atk=16, repeat=2, hexagram_add=True,
                               qi_add=1, level=3)

# INCARNATION PHASE
heaven_hexagram_1 = Card(name="Heaven Hexagram", hexagram_add=1, qi_add=1, chase=True, level=1)
heaven_hexagram_2 = Card(name="Heaven Hexagram", hexagram_add=2, qi_add=2, chase=True, level=2)
heaven_hexagram_3 = Card(name="Heaven Hexagram", hexagram_add=3, qi_add=3, chase=True, level=3)
# TODO chase condition

# _five_thunders_1 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=8, hexagram_atk=8, repeat=5, level=1)
# _five_thunders_2 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=10, hexagram_atk=10, repeat=5, level=2)
# _five_thunders_3 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=12, hexagram_atk=12, repeat=5, level=3)

five_thunders_1 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=0.3 * 8, hexagram_atk=8, repeat=5,
                       level=1)
five_thunders_2 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=0.3 * 10, hexagram_atk=10, repeat=5,
                       level=2)
five_thunders_3 = Card(name="Five Thunders", qi_cost=1, hexagram=True, atk=0.3 * 12, hexagram_atk=12, repeat=5,
                       level=3)

propitious_omen_1_HEXAGRAM = Card(name="Propitious Omen", qi_add=2, hexagram_add=3, level=1)
propitious_omen_2_HEXAGRAM = Card(name="Propitious Omen", qi_add=2, hexagram_add=5, level=2)
propitious_omen_3_HEXAGRAM = Card(name="Propitious Omen", qi_add=2, hexagram_add=7, level=3)
# TODO choose highest attribute between qi, hexagram, star power to increase

# SIDE JOBS
# ELIXIRIST
ice_spirit_guard_elixir_1 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=2, consumed=True, level=1)
ice_spirit_guard_elixir_2 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=3, consumed=True, level=2)
ice_spirit_guard_elixir_3 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=4, consumed=True, level=3)

# Decks
deck1 = [hexagram_formacide_3,  flame_hexagram_2, heaven_hexagram_2, five_thunders_3, astral_move_fly_1, thunder_hexagram_rythm_3,
         dance_of_the_dragonfly_1, flame_hexagram_1]
deck2 = [normal_attack, normal_attack, normal_attack, normal_attack, normal_attack, normal_attack, normal_attack,
         normal_attack]

# Battle
ballfire = Player("Ballfire", 100, 84, 100, deck1)
enemy = Player("Hua Qinrui", 100, 77, 132, deck2, guard_up=1)

simulate_battle(ballfire, enemy)
