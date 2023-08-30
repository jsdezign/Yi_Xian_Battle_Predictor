import math
import random

#TODO test flawed test new hexagram

class Card:
    def __init__(self, name="", atk=0.0, defense=0.0, hp=0.0, max_hp_add=0,
                 max_hp_reduce=0, qi_cost=0, qi_add=0, atk_add=0, sword_intent_add=0, flaw=0, weakened=0,
                 starpower_add=0,
                 ignore_defense=0,
                 cloud_sword=False, cloud_sword_atk_add=0, cloud_sword_chase=False,
                 cloud_sword_ignore_defense=0, cloud_sword_regeneration_add=0,
                 cloud_sword_strikes=0, cloud_sword_defense=0, cloud_sword_atk=0,
                 for_cloud_sword_defense=0, for_cloud_sword_qi_add=0, for_cloud_sword_atk=0,
                 injured_chase=False, injured_defense=0, injured_defense_for_hp=0,
                 spirit_sword=False,
                 internalinjury_add=0,
                 hexagram_chase=False, heaven_hexagram=0, hexagram=False, hexagram_rythm=0, hexagram_add=0,
                 hexagram_flaw=0, hexagram_weaken=0, hexagram_hp=0, hexagram_atk=0, hexagram_def=0,
                 post_action=False, star_point=False, alt_card=None,
                 regeneration_add=0, formacide_add=0, cittadharma_add=0, guard_up=0,
                 consumed=False,
                 chase=False, level=1, repeat=1, strikes=1, zzz=False):
        self.hexagram_hp = hexagram_hp
        self.hexagram_weaken = hexagram_weaken
        self.hexagram_flaw = hexagram_flaw
        self.weakened = weakened
        self.flaw = flaw
        self.hexagram_rythm = hexagram_rythm
        self.heaven_hexagram = heaven_hexagram
        self.hexagram_chase = hexagram_chase
        self.zzz = zzz
        self.spirit_sword = spirit_sword
        self.cloud_sword_regeneration_add = cloud_sword_regeneration_add
        self.injured_defense = injured_defense
        self.injured_defense_for_hp = injured_defense_for_hp
        self.injured_chase = injured_chase
        self.cloud_sword_atk = cloud_sword_atk
        self.cloud_sword_defense = cloud_sword_defense
        self.cloud_sword_strikes = cloud_sword_strikes
        self.cloud_sword_ignore_defense = cloud_sword_ignore_defense
        self.cloud_sword_chase = cloud_sword_chase
        self.cloud_sword_atk_add = cloud_sword_atk_add
        self.for_cloud_sword_atk = for_cloud_sword_atk
        self.for_cloud_sword_qi_add = for_cloud_sword_qi_add
        self.for_cloud_sword_defense = for_cloud_sword_defense
        self.ignore_defense = ignore_defense
        self.cloud_sword = cloud_sword
        self.sword_intent_add = sword_intent_add
        self.atk_add = atk_add
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
    def __init__(self, name, cards, destiny=100, cultivation=100, max_hp=100, regeneration=0, internal_injury=0,
                 starpower=0, hexagram=0, defense=0, guard_up=0, always_injure=False, ignore_defense=0, flaw=0,
                 weakened=0, hexagram_consumed=0):
        self.hexagram_consumed = hexagram_consumed
        self.weakened = weakened
        self.flaw = flaw
        self.ignore_defense = ignore_defense
        self.always_injure = always_injure
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
        self.atk = 0
        self.decrease_atk = 0
        self.slot = 0
        self.successive_cloud_sword = 0
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


def check_wincon(self, opponent, turn):
    if opponent.hp <= 0:
        print("")
        print("")
        print(self.name + " wins after " + str(int(turn)) + " turns")
        return True
    if self.hp <= 0:
        print("")
        print("")
        print(opponent.name + " wins after " + str(int(turn)) + " turns")
        return True
    else:
        return False


def resolve_card(self, opponent, card):
    # Skip consume and continuous cards
    if card.consumed and self.played_cards[self.slot % 8] == 1:
        self.slot += 1
        ncard = self.cards[self.slot % 8]
        resolve_card(self, opponent, ncard)
    else:
        # Check qi cost
        if card.qi_cost > self.qi:
            print(self.name + " waits for qi")
            self.qi += 1
            self.hp += self.cittadharma
            return
        self.qi -= card.qi_cost
        # Repeat attacks (Five thunder)
        print(self.name + " uses " + card.name)
        i = 0
        while i < card.repeat:
            enemy_hp_before = opponent.hp
            flaw = 1
            weakened = 1
            if opponent.flaw > 0:
                flaw = 1.4
            if opponent.weakened > 0:
                weakened = 0.6
            damage = 0
            defense = 0
            healing = 0
            boost = self.sword_intent + self.atk
            # Cloud Sword logic
            if self.successive_cloud_sword > 0 and card.cloud_sword:
                if card.cloud_sword_atk > 0:
                    card.atk = card.cloud_sword_atk
                if card.cloud_sword_strikes > 0:
                    card.strikes = card.cloud_sword_strike
                if card.cloud_sword_defense > 0:
                    card.defense += card.cloud_sword_defense
                self.atk += card.cloud_sword_atk_add
                self.regeneration += card.cloud_sword_regeneration_add
                self.ignore_defense += card.cloud_sword_ignore_defense

                # Cloud Sword Avalanche deals damage for every successive cloud sword card played
                card.atk += card.for_cloud_sword_atk * self.successive_cloud_sword
                card.defense += card.for_cloud_sword_defense * self.successive_cloud_sword
                card.qi_add += card.for_cloud_sword_qi_add * self.successive_cloud_sword

                if card.cloud_sword_chase:
                    card.chase = True
            if not card.cloud_sword:
                self.successive_cloud_sword = 0
            else:
                self.successive_cloud_sword += 1

            # Post Action logic
            if card.post_action and self.played_cards[self.slot % 8 == 1]:
                pass
                # TODO
            # Star Point logic
            if self.slot % 8 in self.star_points:
                boost += self.starpower
                if card.star_point:
                    card = card.alt_card
            # Hexagram logic
            if card.hexagram:
                if card.hexagram_atk > 0 and self.hexagram > 0:
                    card.atk = card.hexagram_atk
                    self.hexagram -= 1
                    self.hexagram_consumed += 1
                if card.hexagram_def > 0 and self.hexagram > 0:
                    card.defense += card.hexagram_def
                    self.hexagram -= 1
                    self.hexagram_consumed += 1
                if card.hexagram_hp > 0 and self.hexagram > 0:
                    card.hp += card.hexagram_hp
                    self.hexagram -= 1
                    self.hexagram_consumed += 1

                if card.hexagram_flaw > 0 and self.hexagram > 0:
                    opponent.flaw += card.hexagram.flaw
                    self.hexagram -= 1
                    self.hexagram_consumed += 1
                if card.hexagram_weakened > 0 and self.hexagram > 0:
                    opponent.weakened += card.hexagram.weakened
                    self.hexagram -= 1
                    self.hexagram_consumed += 1

                if card.hexagram_chase and self.hexagram > 0:
                    card.chase = True
                    self.hexagram -= 1
                    self.hexagram_consumed += 1

            if card.atk > 0:
                # i dont know how exactly flaw + weakened works
                for _ in range(card.strikes):
                    damage = boost + card.atk
                    damage = math.floor(damage * flaw)
                    damage = min(math.floor(damage * weakened), 1)
                    # this might not be correct in edge cases with reduced atk (is it possible to strike for 0 damage?)
                    if damage > 0:
                        deal_damage(damage, opponent)
                        print(card.name + " deals " + str(damage) + " damage")
            # Check injured after all strikes
            if enemy_hp_before > opponent.hp or self.always_injure:
                # TODO lifesteal from unrestrained sword and wood
                if card.injured_defense > 0:
                    card.defense = card.injured_defense
                if card.injured_defense_for_hp > 0:
                    card.defense = card.injured_defense_for_hp * (enemy_hp_before - opponent.hp)
                if card.injured_chase:
                    card.chase = True

            defense += card.defense
            # formacide add
            self.formacide += card.formacide_add
            # formacide dmg
            self.hexagram += card.hexagram_add
            self.hexagram += min(card.hexagram_rythm, self.hexagram_consumed)
            damage = card.hexagram_add * self.formacide
            if damage > 0:
                deal_damage(damage, opponent)
                print(card.name + " deals " + str(damage) + " damage")
            if card.heaven_hexagram and self.hexagram >= 3:
                card.chase = True

            # citta-dharma
            healing += card.qi_add * self.cittadharma
            healing += card.hp
            self.qi += card.qi_add
            # defense
            self.defense += defense
            # max hp
            self.max_hp += card.max_hp_add
            opponent.max_hp -= card.max_hp_reduce
            opponent.hp = min(opponent.max_hp, opponent.hp)
            # healing
            self.hp = min(self.max_hp, self.hp + healing)
            # attack
            self.atk += card.atk_add
            # sword intent
            if card.atk > 0:
                self.sword_intent = 0
            self.sword_intent += card.sword_intent_add
            # regeneration
            self.regeneration += card.regeneration_add
            # debuffs
            opponent.internal_injury += card.internal_injury
            opponent.flaw += card.flaw
            opponent.weakened += card.weakened

            self.played_cards[self.slot % 8] = 1
            i += 1

        self.slot += 1
        if card.chase:
            chase(self, card, opponent)


def chase(self, card, opponent):
    print(card.name + " chases")
    ncard = self.cards[self.slot % 8]
    resolve_card(self, opponent, ncard)


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
    self, opponent = choose_starting_player(player1, player2)
    turn = 1
    for a in range(turns):
        # Start of turn
        print("Start of turn " + str(turn))
        self.hp = min(self.hp + self.regeneration, self.max_hp)
        if self.internal_injury > 0:
            reduce_hp(self.internal_injury, self)
        self.defense = math.floor(self.defense / 2)
        if check_wincon(self, opponent, turn):
            break
        # Resolve card
        card = self.cards[self.slot % 8]
        if not card.zzz:
            resolve_card(self, opponent, card)

            # Print
            print_battle_status(player1, player2)
            if check_wincon(self, opponent, turn):
                break
            # End of turn
            if check_wincon(self, opponent, turn):
                break
        print("-----------------------------------------")
        # Change active player
        b = self
        self = opponent
        opponent = b
        turn += .5
    self.reset_status()
    opponent.reset_status()


def print_battle_status(player1, player2):
    hp_bar1 = '=' * int((player1.hp / player1.max_hp * 30)) if player1.max_hp != 0 else ""
    hp_bar2 = '=' * int((player2.hp / player2.max_hp * 30)) if player2.max_hp != 0 else ""

    print(f"{player1.name} has {player1.hp:.1f}hp left [{hp_bar1:30}]")
    print(f"{player2.name} has {player2.hp:.1f}hp left [{hp_bar2:30}]")


nini = Card("Skip Turn")
normal_attack = Card("Normal Attack", 3, level=1)

# CLOUD SPIRIT SWORD SECT
# MEDITATION PHASE

# FOUNDATION PHASE

# VIRTUOSO PHASE

cloud_sword_spirit_coercion_1 = Card("Cloud Sword - Spirit Coercion", atk=7, cloud_sword=True, for_cloud_sword_qi_add=1,
                                     level=1)
cloud_sword_spirit_coercion_2 = Card("Cloud Sword - Spirit Coercion", atk=11, cloud_sword=True,
                                     for_cloud_sword_qi_add=1, level=2)
cloud_sword_spirit_coercion_3 = Card("Cloud Sword - Spirit Coercion", atk=15, cloud_sword=True,
                                     for_cloud_sword_qi_add=1, level=3)
# IMMORTALITY PHASE
cloud_sword_flash_wind_1 = Card("Cloud Sword - Flash Wind", atk=4, cloud_sword=True, cloud_sword_chase=True, level=1)
cloud_sword_flash_wind_2 = Card("Cloud Sword - Flash Wind", atk=8, cloud_sword=True, cloud_sword_chase=True, level=2)
cloud_sword_flash_wind_3 = Card("Cloud Sword - Flash Wind", atk=12, cloud_sword=True, cloud_sword_chase=True, level=3)

cloud_sword_moon_shade_1 = Card("Cloud Sword - Moon Shade", defense=1, cloud_sword=True, cloud_sword_atk_add=2, level=1)
cloud_sword_moon_shade_2 = Card("Cloud Sword - Moon Shade", defense=2, cloud_sword=True, cloud_sword_atk_add=3, level=2)
cloud_sword_moon_shade_3 = Card("Cloud Sword - Moon Shade", defense=3, cloud_sword=True, cloud_sword_atk_add=4, level=3)

giant_kun_spirit_sword_1 = Card("Giant Kun Spirit Sword", atk=10, defense=10, qi_cost=3, chase=True, spirit_sword=True)
giant_kun_spirit_sword_2 = Card("Giant Kun Spirit Sword", atk=13, defense=13, qi_cost=3, chase=True, spirit_sword=True)
giant_kun_spirit_sword_3 = Card("Giant Kun Spirit Sword", atk=16, defense=16, qi_cost=3, chase=True, spirit_sword=True)

flow_cloud_chaos_sword_1 = Card("Flow Cloud Chaos Sword", atk=2, strikes=4, qi_cost=1, level=1)
flow_cloud_chaos_sword_2 = Card("Flow Cloud Chaos Sword", atk=2, strikes=5, qi_cost=1, level=2)
flow_cloud_chaos_sword_3 = Card("Flow Cloud Chaos Sword", atk=2, strikes=6, qi_cost=1, level=3)

# INCARNATION PHASE

cloud_sword_dragon_roam_1 = Card("Cloud Sword - Dragon Roam", atk=2, strikes=2, cloud_sword=True, cloud_sword_defense=3,
                                 injured_chase=True, level=1)
cloud_sword_dragon_roam_2 = Card("Cloud Sword - Dragon Roam", atk=2, strikes=3, cloud_sword=True, cloud_sword_defense=5,
                                 injured_chase=True, level=2)
cloud_sword_dragon_roam_3 = Card("Cloud Sword - Dragon Roam", atk=2, strikes=4, cloud_sword=True, cloud_sword_defense=7,
                                 injured_chase=True, level=3)

cloud_sword_step_lightly_1 = Card("Cloud Sword - Step Lightly", atk=2, strikes=2, defense=3, cloud_sword=True,
                                  for_cloud_sword_defense=3, level=1)
cloud_sword_step_lightly_2 = Card("Cloud Sword - Step Lightly", atk=2, strikes=3, defense=4, cloud_sword=True,
                                  for_cloud_sword_defense=4, level=2)
cloud_sword_step_lightly_3 = Card("Cloud Sword - Step Lightly", atk=2, strikes=4, defense=5, cloud_sword=True,
                                  for_cloud_sword_defense=5, level=3)

# CHARACTER CARDS
cloud_sword_pray_rain_1 = Card(name="Cloud Sword - Pray Rain", atk=3, strikes=3, cloud_sword=True,
                               cloud_sword_regeneration_add=2,
                               level=1)
cloud_sword_pray_rain_2 = Card(name="Cloud Sword - Pray Rain", atk=4, strikes=3, cloud_sword=True,
                               cloud_sword_regeneration_add=3,
                               level=2)
cloud_sword_pray_rain_3 = Card(name="Cloud Sword - Pray Rain", atk=5, strikes=3, cloud_sword=True,
                               cloud_sword_regeneration_add=4,
                               level=3)

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

# VIRTUOSO PHASE
divine_power_elixir_1 = Card(name="Divine Power Elixir", consumed=True, atk_add=1, level=1)
divine_power_elixir_2 = Card(name="Divine Power Elixir", consumed=True, atk_add=2, level=2)
divine_power_elixir_3 = Card(name="Divine Power Elixir", consumed=True, atk_add=3, level=3)

# INCARNATION PHASE
ice_spirit_guard_elixir_1 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=2, consumed=True, level=1)
ice_spirit_guard_elixir_2 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=3, consumed=True, level=2)
ice_spirit_guard_elixir_3 = Card(name="Ice Spirit Guard Elixir", qi_cost=1, guard_up=4, consumed=True, level=3)

# DECKS
BallfireDeck1 = [hexagram_formacide_2, hexagram_formacide_1, heaven_hexagram_3, flame_hexagram_3,
                 dance_of_the_dragonfly_3, five_thunders_2, heaven_hexagram_1,
                 thunder_hexagram_rythm_2]
BallfireDeck2 = [hexagram_formacide_2, heaven_hexagram_3, flame_hexagram_3, dance_of_the_dragonfly_3, five_thunders_2,
                 heaven_hexagram_1,
                 thunder_hexagram_rythm_2, normal_attack]
CloudSword1 = [divine_power_elixir_2, cloud_sword_dragon_roam_2, cloud_sword_moon_shade_3, cloud_sword_flash_wind_2,
               cloud_sword_pray_rain_1, cloud_sword_spirit_coercion_2, giant_kun_spirit_sword_2,
               flow_cloud_chaos_sword_2]
NormalAttacks = [normal_attack, normal_attack, normal_attack, normal_attack, normal_attack, normal_attack,
                 normal_attack,
                 normal_attack]
Nini = [nini, nini, nini, nini, nini, nini, nini, nini]

# Battle
ballfire_1 = Player("Ballfire", cultivation=104, max_hp=115, cards=BallfireDeck2, hexagram=2)
enemy = Player("Enemy", cards=NormalAttacks)
hua_qinrui_1 = Player("Hua Qinrui", cultivation=77, max_hp=132, cards=NormalAttacks, guard_up=1)
long_yao_1 = Player("Long Yao", cultivation=87, max_hp=117, cards=CloudSword1, ignore_defense=2)

simulate_battle(ballfire_1, enemy)
