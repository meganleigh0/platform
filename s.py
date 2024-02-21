import pandas as pd
import numpy as np
import re
from anytree import Node, RenderTree
from utils.logger import Logger  # Make sure this import matches the location of your Logger class

def process_mbom(var):
    # Initialize logger
    logger = Logger(var)
    
    logger.log_entry("MBOM processing started")

    # Load file
    df_lim = load_mbom(var)[1]
    logger.log_entry("MBOM file loaded", shape=str(df_lim.shape))
    
    # Assign unique id to each line
    df_lim = set_ids(df_lim)
    logger.log_entry("Unique IDs assigned", shape=str(df_lim.shape))

    # Assign station point
    df_lim = assign_station_point(df_lim)
    logger.log_entry("Station points assigned", shape=str(df_lim.shape))
    
    # Search standards
    mbom_ops = search_swh(df_lim)
    logger.log_entry("Standards searched and mapped")

    # Map standards to assemblies
    df_lim['Operations'] = df_lim['mbomID'].map(mbom_ops).fillna(0)
    logger.log_entry("Operations mapped to assemblies", shape=str(df_lim.shape))
   
    # Translate to tree structure
    nodes = build_tree(df_lim)
    logger.log_entry("Tree structure built")

    # Cascade station definitions
    propagate_station(nodes[100001])  # Assuming 100001 is the root ID, adjust as necessary
    logger.log_entry("Station definitions propagated through tree")
    
    # Convert to dataframe
    df_final = tree_to_df(nodes)
    logger.log_entry("Tree converted back to DataFrame", shape=str(df_final.shape))

    # Save the log to a CSV
    logger.save_to_csv(f"logs/{var}_process_log.csv")

    return df_final

# Ensure all required functions (load_mbom, set_ids, assign_station_point, search_swh, build_tree, propagate_station, tree_to_df) are properly defined and include logging where applicable.
