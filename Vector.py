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

    def drawVector(self, originVector, screen, color=[0,0,0]):

        startPos = pygame.Vector2(originVector.x, originVector.y)
        endPos = pygame.Vector2(originVector.x + self.x, (originVector.y + self.y))
        startPosFlipped = pygame.Vector2(startPos.x, height - startPos.y-Vector2.initialHeight)
        endPosFlipped = pygame.Vector2(endPos.x, height-endPos.y-Vector2.initialHeight)
        pygame.draw.line(screen, color, startPosFlipped, endPosFlipped, 3)
        return endPos

    @staticmethod
    def addVectors(vec1, vec2):

        x = vec1.x+vec2.x
        y = vec1.y + vec2.y

        return Vector2(math.sqrt(x ** 2 + y ** 2), math.atan2(y, x))

    @staticmethod
    def avgVector(listOfVectors):
        if not listOfVectors:
            return Vector2(0,0)

        cumulativeX = 0
        cumulativeY = 0
        totalVectors = len(listOfVectors)

        # Iterate through the list and sum up the vectors incrementally
        for i in range(totalVectors):
            cumulativeX += listOfVectors[i].x
            cumulativeY += listOfVectors[i].y
            for j in range(i):
                cumulativeX += listOfVectors[j].x
                cumulativeY += listOfVectors[j].y

        # Divide by the total number of vectors
        avgX = cumulativeX / totalVectors
        avgY = cumulativeY / totalVectors

        # Convert back to polar coordinates (r, theta)
        avgR = math.sqrt(avgX ** 2 + avgY ** 2)
        avgTheta = math.atan2(avgY, avgX)

        return Vector2(avgR, avgTheta)



