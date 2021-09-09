import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import random

"""
# Battleforge Reborn Deck Randomizer
Here starts the fun!!!!
"""

def main():
    df = pd.read_csv('./data/card_db.csv')

    # Parameters
    # Minimum number of units/buildings/spells to put into tier n
    min_tn_units = [2, 2, 2, 2]
    min_tn_buildings = [1, 1, 1, 1]
    min_tn_spells = [1, 1, 1, 1]

    # Max/min number of different colours to put into the deck
    max_n_colors = 2
    min_n_colors = 1

    # The colors of the orbs are chosen
    colors = ['Nature', 'Fire', 'Frost', 'Shadow']
    primary_colors = random.sample(colors, k=random.randint(min_n_colors, max_n_colors))

    resource_orbs = []
    if len(primary_colors) == 1:
        resource_orbs = primary_colors * 4
    else:
        resource_orbs = random.choices(primary_colors, k=4)

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

    st.write(resource_orbs)

    st.dataframe(final_deck.sort_values(by=['orbsamount'])[['name', 'faction', 'type', 'orbsamount']], width=600,
                 height=550)

    result = st.button("Generate Deck!")


if __name__ == '__main__':
    main()
