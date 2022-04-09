import pygame
import sys
import TwoPlayers
import ThreePlayers
import os

os.chdir("./Final Project/Chinese-checkers-1")

#ai: ai player
#h: human player
#TwoPlayers.TwoPlayers("ai", "h")

ThreePlayers.TreePlayers("h", "h", "h")