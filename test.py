import pygame
import sys
import ThreePlayers
import TwoPlayers
import ThreePlayers
import FourPlayers
import SixPlayers
import os

os.chdir("./Final Project/Chinese-checkers-1")

#ai: ai player
#h: human player
#TwoPlayers.TwoPlayers("ai", "h")

#ThreePlayers.TreePlayers("h", "h", "ai")

#FourPlayers.FoorPlayers("h", "h", "h", "h")

SixPlayers.SixPlayers("h", "h", "h", "h", "h", "h")