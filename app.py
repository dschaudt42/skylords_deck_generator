import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import random

"""
# Battleforge Reborn Deck Randomizer
Here starts the fun!!!!
"""

# Parameters
min_t1_units = 2
min_t2_units = 2
min_t3_units = 2
min_t4_units = 2

min_t1_buildings = 1
min_t2_buildings = 1
min_t3_buildings = 1
min_t4_buildings = 1

min_t1_spells = 1
min_t2_spells = 1
min_t3_spells = 1
min_t4_spells = 1

df = pd.read_csv('./data/card_db.csv')

colors = ['Nature', 'Fire', 'Frost', 'Shadow']
primary_colors = random.sample(colors, k=random.randint(1, 2))

resource_orbs = []
if len(primary_colors) == 1:
    resource_orbs = primary_colors * 4
else:
    resource_orbs = random.choices(primary_colors, k=4)


def color_count_dict(orbs):
    color_dict = {}
    fire_count = 0
    frost_count = 0
    nature_count = 0
    shadow_count = 0

    for color in orbs:
        if color == 'Frost':
            frost_count += 1
        if color == 'Fire':
            fire_count += 1
        if color == 'Nature':
            nature_count += 1
        if color == 'Shadow':
            shadow_count += 1

    color_dict['Frost'] = frost_count
    color_dict['Fire'] = fire_count
    color_dict['Nature'] = nature_count
    color_dict['Shadow'] = shadow_count
    return color_dict


def is_playable(card_orbs, resource_orbs_):
    is_playable_ = True
    card_count = color_count_dict(card_orbs)

    for key, value in card_count.items():
        if color_count_dict(resource_orbs_[:len(card_orbs)])[key] < value:
            is_playable_ = False
    return is_playable_


df['orb_list'] = df['orbs'].str.split(',').tolist()
df['is_playable'] = df['orb_list'].apply(is_playable, args=([resource_orbs]))
df_playable = df[df['is_playable'] is True]

units_filt_t1 = (df_playable['orbsamount'] == 1) & (df_playable['type'] == 'Unit')
units_filt_t2 = (df_playable['orbsamount'] == 2) & (df_playable['type'] == 'Unit')
units_filt_t3 = (df_playable['orbsamount'] == 3) & (df_playable['type'] == 'Unit')
units_filt_t4 = (df_playable['orbsamount'] == 4) & (df_playable['type'] == 'Unit')

buildings_filt_t1 = (df_playable['orbsamount'] == 1) & (df_playable['type'] == 'Building')
buildings_filt_t2 = (df_playable['orbsamount'] == 2) & (df_playable['type'] == 'Building')
buildings_filt_t3 = (df_playable['orbsamount'] == 3) & (df_playable['type'] == 'Building')
buildings_filt_t4 = (df_playable['orbsamount'] == 4) & (df_playable['type'] == 'Building')

spells_filt_t1 = (df_playable['orbsamount'] == 1) & (df_playable['type'] == 'Spell')
spells_filt_t2 = (df_playable['orbsamount'] == 2) & (df_playable['type'] == 'Spell')
spells_filt_t3 = (df_playable['orbsamount'] == 3) & (df_playable['type'] == 'Spell')
spells_filt_t4 = (df_playable['orbsamount'] == 4) & (df_playable['type'] == 'Spell')

final_deck = pd.DataFrame()

final_deck = final_deck.append(df_playable[units_filt_t1].sample(min_t1_units))
final_deck = final_deck.append(df_playable[units_filt_t2].sample(min_t2_units))
final_deck = final_deck.append(df_playable[units_filt_t3].sample(min_t3_units))
final_deck = final_deck.append(df_playable[units_filt_t4].sample(min_t4_units))

final_deck = final_deck.append(df_playable[buildings_filt_t1].sample(min_t1_buildings))
final_deck = final_deck.append(df_playable[buildings_filt_t2].sample(min_t2_buildings))
final_deck = final_deck.append(df_playable[buildings_filt_t3].sample(min_t3_buildings))
final_deck = final_deck.append(df_playable[buildings_filt_t4].sample(min_t4_buildings))

final_deck = final_deck.append(df_playable[spells_filt_t1].sample(min_t1_spells))
final_deck = final_deck.append(df_playable[spells_filt_t2].sample(min_t2_spells))
final_deck = final_deck.append(df_playable[spells_filt_t3].sample(min_t3_spells))
final_deck = final_deck.append(df_playable[spells_filt_t4].sample(min_t4_spells))

random_card_amount = 20 - final_deck.shape[0]
random_filler_cards = df_playable[~df_playable.index.isin(final_deck.index)].sample(random_card_amount)
final_deck = final_deck.append(random_filler_cards)

st.write(resource_orbs)

st.dataframe(final_deck.sort_values(by=['orbsamount'])[['name', 'faction', 'type', 'orbsamount']], width=600,
             height=550)

result = st.button("Generate Deck!")
