import math
import pygame

width, height = 1280, 720
class Vector2:
    initialHeight = 10
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta
        cartesian = self.toCartesian()
        self.x = cartesian[0]
        self.y = cartesian[1]

    def toCartesian(self):
        return self.r * math.cos(self.theta), self.r * math.sin(self.theta)

    def drawVector(self, originVector, screen):

        startPos = pygame.Vector2(originVector.x, originVector.y)
        endPos = pygame.Vector2(originVector.x + self.x, (originVector.y + self.y))
        startPosFlipped = pygame.Vector2(startPos.x, height - startPos.y-Vector2.initialHeight)
        endPosFlipped = pygame.Vector2(endPos.x, height-endPos.y-Vector2.initialHeight)
        pygame.draw.line(screen, "black", startPosFlipped, endPosFlipped, 3)
        return endPos