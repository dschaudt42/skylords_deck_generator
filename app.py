import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import random
import configparser as cp

"""
# Battleforge Reborn Deck Randomizer
Here starts the fun!!!!
"""

colors = ['Nature', 'Fire', 'Frost', 'Shadow']


def color_count_dict(orbs):
    return {color: orbs.count(color) for color in colors}


def is_playable(card_orbs, resource_orbs_):
    """
    Determines, weather a card with requirements `card_orbs` is playable,
    when the orbs listed in`resource_orbs_` are built.
    :param card_orbs: List of strings, which can be "Nature", "Fire", "Frost" or "Shadow"
    :param resource_orbs_: List of strings, which can be "Nature", "Fire", "Frost" or "Shadow"
    :return: Boolean value
    """
    card_count = color_count_dict(card_orbs)

    for key, value in card_count.items():
        if color_count_dict(resource_orbs_[:len(card_orbs)])[key] < value:
            return False
    return True


def gen_deck(min_tn_units, min_tn_buildings, min_tn_spells, max_n_colors=2, min_n_colors=1):
    """
    Generates a random deck fitting to the parameters given.
    :param min_tn_units: List of integers, which determine how many units each tier must include
    :param min_tn_buildings: List of integers, which determine how many buildings each tier must include
    :param min_tn_spells: List of integers, which determine how many spells each tier must include
    :param max_n_colors: Integer, which gives the maximum amount of colors that can be present in a deck
    :param min_n_colors: Integer, which gives the minimum amount of colors that can be present in a deck
    :return: resource_orbs, final_deck - a tuple which has the picked orb colors and the generated deck as its elements.
    """
    df = pd.read_csv('./data/card_db.csv')

    # The colors of the orbs are chosen
    primary_colors = random.sample(colors, k=random.randint(min_n_colors, max_n_colors))

    resource_orbs = []
    if len(primary_colors) == 1:
        resource_orbs = primary_colors * 4
    else:
        resource_orbs = random.choices(primary_colors, k=4)

    df['orb_list'] = df['orbs'].str.split(',').tolist()
    df['is_playable'] = df['orb_list'].apply(is_playable, args=([resource_orbs]))
    df_playable = df[df['is_playable']]

    units_filt_tn = [(df_playable['orbsamount'] == n) & (df_playable['type'] == 'Unit') for n in range(1, 5)]
    buildings_filt_tn = [(df_playable['orbsamount'] == n) & (df_playable['type'] == 'Building') for n in range(1, 5)]
    spells_filt_tn = [(df_playable['orbsamount'] == n) & (df_playable['type'] == 'Spell') for n in range(1, 5)]

    final_deck = pd.DataFrame()

    # Adds the minimum required cards to the deck
    for n in range(4):
        final_deck = final_deck.append(df_playable[units_filt_tn[n]].sample(min_tn_units[n]))
        final_deck = final_deck.append(df_playable[buildings_filt_tn[n]].sample(min_tn_buildings[n]))
        final_deck = final_deck.append(df_playable[spells_filt_tn[n]].sample(min_tn_spells[n]))

    # Fills the deck with random, playable cards
    random_card_amount = 20 - final_deck.shape[0]
    random_filler_cards = df_playable[~df_playable.index.isin(final_deck.index)].sample(random_card_amount)
    final_deck = final_deck.append(random_filler_cards)

    return resource_orbs, final_deck


def gen_pve_deck():
    """
    Generates a deck with parameters fitting for a PvE Deck. These are the parameters used in the program previously.
    :return: resource_orbs, final_deck - a tuple which has the picked orb colors and the generated deck as its elements.
    """
    pve_parser = cp.RawConfigParser()
    config_path = r"config.txt"
    pve_parser.read(config_path)

    min_tn_units = [int(t) for t in pve_parser.get("PvE-config", "min_tn_units").split(',')]
    min_tn_buildings = [int(t) for t in pve_parser.get("PvE-config", "min_tn_buildings").split(',')]
    min_tn_spells = [int(t) for t in pve_parser.get("PvE-config", "min_tn_spells").split(',')]
    max_n_colors = int(pve_parser.get("PvE-config", "max_n_colors"))
    min_n_colors = int(pve_parser.get("PvE-config", "min_n_colors"))

    return gen_deck(min_tn_units, min_tn_buildings, min_tn_spells, max_n_colors, min_n_colors)


def gen_pvp_deck():
    """
    Generates a deck with parameters fitting for a PvP Deck. These parameters have been chosen by me kind of arbitrarily
    but in a way, that seemed fitting for a PvP Deck.
    :return: resource_orbs, final_deck - a tuple which has the picked orb colors and the generated deck as its elements.
    """
    pvp_parser = cp.RawConfigParser()
    config_path = r"config.txt"
    pvp_parser.read(config_path)

    min_tn_units = [int(t) for t in pvp_parser.get("PvP-config", "min_tn_units").split(',')]
    min_tn_buildings = [int(t) for t in pvp_parser.get("PvP-config", "min_tn_buildings").split(',')]
    min_tn_spells = [int(t) for t in pvp_parser.get("PvP-config", "min_tn_spells").split(',')]
    max_n_colors = int(pvp_parser.get("PvP-config", "max_n_colors"))
    min_n_colors = int(pvp_parser.get("PvP-config", "min_n_colors"))

    return gen_deck(min_tn_units, min_tn_buildings, min_tn_spells, max_n_colors, min_n_colors)


def write_deck(gamemode=0):
    """
    Generates a deck fitting to the given game mode and writes it to the application
    :param gamemode: Integer, 0 for PvE, 1 for PvP
    :return: None
    """
    if gamemode == 0:
        resource_orbs, final_deck = gen_pve_deck()
    else:
        resource_orbs, final_deck = gen_pvp_deck()

    st.write(resource_orbs)
    st.dataframe(final_deck.sort_values(by=['orbsamount'])[['name', 'faction', 'type', 'orbsamount']], width=600,
                 height=550)


def main():
    # Before clicking anything, the main app only consists of two buttons - one for a PvE deck and one for a PvP deck.
    # Clicking one of them will generate a deck and write it to the app.
    if st.button("Generate PvE Deck!"):
        write_deck(0)

    if st.button("Generate PvP Deck!"):
        write_deck(1)


if __name__ == '__main__':
    main()
