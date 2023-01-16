import pygame
from random import randrange
import time

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dark_red = (200, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)

tilePixelWH = 29  
borderWH = 5  
width = 30
height = 16
mineCount = 80
lost = 0
won = 0
start_t = time.perf_counter()
total_t = 0


class Tile:
    mine = False
    clicked = False
    marked = False
    neighbourMines = 0
    mineProbability = 0
    analyzed = False
    neighbourIndices = []

        
class Minesweeper:
    width = 10
    height = 10
    mineCount = 10
    flagCount = 10
    uncoveredtiles = 0
    firstClick = True
    gameOver = False
    gameWon = False
    field = []
    last_clickedX = -1
    last_clickedY = -1
        
    def __init__(self, width, height, mineCount):
        self.width = width
        self.height = height
        self.mineCount = min(mineCount, width*height-9)
        self.flagCount = self.mineCount
        for x in range(width):
            self.field.append([])
            for y in range(height):
                self.field[x].append([])
                self.field[x][y] = Tile()
                                 
    def updateCellNeighbourCount(self, x, y):
        self.field[x][y].neighbourMines = self.getCellNeighbourMineCount(x, y)
                
    def getNeighbouringIndices(self, x, y):
        neighbours = []
        if x > 0:
            neighbours.append((x-1,y))
            if y > 0:
                neighbours.append((x-1,y-1))
            if y < ms.height - 1:
                neighbours.append((x-1,y+1))
        if y < ms.height - 1:
            neighbours.append((x,y+1))
        if y > 0:
            neighbours.append((x,y-1))
        if x < ms.width - 1:
            neighbours.append((x+1,y))
            if y > 0:
                neighbours.append((x+1,y-1))
            if y < ms.height - 1:
                neighbours.append((x+1,y+1))
        return neighbours

    def getCellNeighbourMineCount(self, x, y):
        mines = 0
        if x > 0:
            if (self.field[x-1][y].mine):
                mines += 1
            if y > 0:
                if (self.field[x-1][y-1].mine):
                    mines += 1
            if y < self.height - 1:
                if (self.field[x-1][y+1].mine):
                    mines += 1
        if y < self.height - 1:
            if (self.field[x][y+1].mine):
                mines += 1
        if y > 0:
            if (self.field[x][y-1].mine):
                mines += 1
        if x < self.width - 1:
            if (self.field[x+1][y].mine):
                mines += 1
            if y > 0:
                if (self.field[x+1][y-1].mine):
                    mines += 1
            if y < self.height - 1:
                if (self.field[x+1][y+1].mine):
                    mines += 1
        return mines
        
    def getCellFromTuple(self, t):
        return self.field[t[0]][t[1]]
        
    def resetField(self):
        self.flagCount = self.mineCount
        self.uncoveredtiles = 0
        self.gameOver = False
        self.gameWon = False
        self.firstClick = True
        for x in range(self.width):
            for y in range(self.height):
                self.field[x][y].mine = False
                self.field[x][y].clicked = False
                self.field[x][y].marked = False
                self.field[x][y].neighbourMines = 0
                self.field[x][y].neighbourIndices = self.getNeighbouringIndices(x,y)
                self.field[x][y].mineProbability = 0
        
    def generateField(self, safeX, safeY):
        minesToGenerate = self.mineCount
        while (minesToGenerate):
            x = randrange(self.width)
            y = randrange(self.height)
            if ((x != safeX) or (y != safeY)) and ((x != safeX-1) or (y != safeY)) and ((x != safeX-1) or (y != safeY-1)) and ((x != safeX-1) or (y != safeY+1)) and ((x != safeX) or (y != safeY+1)) and ((x != safeX) or (y != safeY-1)) and((x != safeX+1) or (y != safeY+1)) and ((x != safeX+1) or (y != safeY)) and ((x != safeX+1) or (y != safeY-1)) and self.field[x][y].mine == False:
                self.field[x][y].mine = True
                minesToGenerate -= 1
        for x in range(self.width):
            for y in range(self.height):
                self.field[x][y].neighbourMines = self.getCellNeighbourMineCount(x, y)
                self.field[x][y].neighbourIndices = self.getNeighbouringIndices(x, y)
        
    def setFlag(self, x, y):
        if (self.field[x][y].clicked) or (self.gameOver) or (self.gameWon):
            return
        if (not self.field[x][y].marked) and (self.flagCount > 0):
            self.field[x][y].marked = True
            self.flagCount -= 1
        elif (self.field[x][y].marked):
            self.field[x][y].marked = False
            self.flagCount += 1

    def uncoverNeighbours(self, x, y, ms_ai):
        if x > 0:
            if (not self.field[x-1][y].mine):
                self.click(x-1, y, ms_ai)
            if y > 0:
                if (not self.field[x-1][y-1].mine):
                    self.click(x-1, y-1, ms_ai)
            if y < self.height - 1:
                if (not self.field[x-1][y+1].mine):
                    self.click(x-1, y+1, ms_ai)
        if y < self.height - 1:
            if (not self.field[x][y+1].mine):
                self.click(x, y+1, ms_ai)
        if y > 0:
            if (not self.field[x][y-1].mine):
                self.click(x, y-1, ms_ai)
        if x < self.width - 1:
            if (not self.field[x+1][y].mine):
                self.click(x+1, y, ms_ai)
            if y > 0:
                if (not self.field[x+1][y-1].mine):
                    self.click(x+1, y-1, ms_ai)
            if y < self.height - 1:
                if (not self.field[x+1][y+1].mine):
                    self.click(x+1, y+1, ms_ai)
        
    def click(self, x, y, ms_ai):
        if (self.gameOver) or (self.gameWon):
            return
        if (self.firstClick):
            self.generateField(x, y)
            self.firstClick = False
            self.click(x, y, ms_ai)
        elif (not self.field[x][y].clicked):
            self.field[x][y].clicked = True
            self.uncoveredtiles += 1
            if self.field[x][y].mine:
                self.gameOver = True
            else:
                if (self.field[x][y].marked == True):
                    self.field[x][y].marked = False
                    self.flagCount += 1
                if (self.uncoveredtiles == self.width*self.height - self.mineCount):
                    self.gameWon = True
                ms_ai.updateKnowledge(self, x, y)
                if (self.field[x][y].neighbourMines == 0):
                    self.uncoverNeighbours(x, y, ms_ai)

        self.last_clickedX = x
        self.last_clickedY = y

class knowledgeData: 
    tiles = []
    mineCount = 0
    x = -1
    y = -1

class Minesweeper_AI:
    knowledge = []
    guesses = 0
    moves = 0
    printKnowledge = False
    def __init__(self):
        pass
        
    def randomMove(self, ms):
        mv = (randrange(ms.width), randrange(ms.height))
        while ((ms.getCellFromTuple(mv).clicked) or (ms.getCellFromTuple(mv).mineProbability == 1)):
            mv = (randrange(ms.width), randrange(ms.height))
        return mv
        
    def contains(self, small, big):
        return set(small).issubset(set(big))
        
    def generateProbabilities(self, ms):
        flagsSet = (ms.mineCount-ms.flagCount)
        defaultProbability = (ms.flagCount) / (ms.width*ms.height-flagsSet-ms.uncoveredtiles)
        for x in range(ms.width):
            for y in range(ms.height):
                ms.field[x][y].analyzed = False
                if ms.field[x][y].clicked:
                    ms.field[x][y].mineProbability = 0
                elif not ms.field[x][y].mineProbability == 1:
                    ms.field[x][y].mineProbability = defaultProbability
        for kd in self.knowledge:
            if (kd.tiles != []):
                newProbability = kd.mineCount / len(kd.tiles)
                for cell in kd.tiles:
                    if (not ms.getCellFromTuple(cell).clicked) and (not ms.getCellFromTuple(cell).marked):
                        if (not ms.getCellFromTuple(cell).analyzed):
                            ms.getCellFromTuple(cell).mineProbability = newProbability
                            ms.getCellFromTuple(cell).analyzed = True
                        if (ms.getCellFromTuple(cell).analyzed) and (ms.getCellFromTuple(cell).mineProbability < newProbability):
                            ms.getCellFromTuple(cell).mineProbability = newProbability
        
    def getMinProbabilityCell(self, ms):
        minProb = 1
        cell = None
        for x in range(ms.width):
            for y in range(ms.height):
                if not ms.field[x][y].clicked:
                    if ms.field[x][y].mineProbability <= minProb:
                        cell = (x, y)
                        minProb = ms.field[x][y].mineProbability
        return cell
        
    def move(self, ms):
        for x in range(ms.width):
            for y in range(ms.height):
                if ((ms.field[x][y].marked) and (ms.field[x][y].mineProbability < 1)) or (not (ms.field[x][y].marked) and (ms.field[x][y].mineProbability == 1)):
                    ms.setFlag(x,y)
        if ms.firstClick:
            self.moves+=1
            return self.randomMove(ms)
        if ms.gameWon:
            return
        for kd in self.knowledge:
            if (kd.mineCount == 0) and (len(kd.tiles) > 0):
                self.moves+=1
                return kd.tiles[0]
            
        self.generateProbabilities(ms)
        cell = self.getMinProbabilityCell(ms)
        self.moves+=1
        self.guesses+=1
        return cell
        
    def updateKnowledge(self, ms, x, y):
        if (ms.field[x][y].clicked):
            kd = knowledgeData()
            kd.mineCount = ms.field[x][y].neighbourMines
            kd.x = x
            kd.y = y
            updatedKnowledge = []
            if (not ms.field[x][y].mine):
                for kd2 in self.knowledge:
                    if ((x, y) in kd2.tiles):
                        kd2.tiles.remove((x,y))
                        updatedKnowledge.append(kd2)
            if kd.mineCount == 0:
                return
            kd.tiles = ms.getNeighbouringIndices(x,y)
            for cell in ms.field[x][y].neighbourIndices:
                if ms.getCellFromTuple(cell).clicked:
                    kd.tiles.remove(cell)
            self.knowledge.append(kd)
            newKnowledge = []
            for kd3 in updatedKnowledge:
                if len(kd3.tiles) > 1:
                    for kd2 in self.knowledge:
                        if (kd2 != kd3):
                            if (len(kd2.tiles) > 0) and self.contains(kd3.tiles, kd2.tiles):
                                newkd = knowledgeData()
                                newkd.tiles = [x for x in kd2.tiles if x not in kd3.tiles]
                                newkd.mineCount = kd2.mineCount - kd3.mineCount
                                newKnowledge.append(newkd)
            self.knowledge = self.knowledge + newKnowledge    
            for kd2 in self.knowledge:
                if len(kd2.tiles) == kd2.mineCount : 
                    for cell in kd2.tiles:
                        ms.getCellFromTuple(cell).mineProbability = 1
            for x in range(ms.width):
                for y in range(ms.height):
                    if (ms.field[x][y].mineProbability == 1):
                        for kd2 in self.knowledge:
                            if (x,y) in kd2.tiles:
                                kd2.tiles.remove((x,y))
                                kd2.mineCount -= 1
            
def drawMS(screen, font, ms):
    for x in range(ms.width):
        for y in range(ms.height):
            if ((ms.field[x][y].clicked) or (ms.gameOver)) and (ms.field[x][y].mine):
                if ms.last_clickedX == x and ms.last_clickedY == y:
                        pygame.draw.rect(screen, dark_red, (borderWH+(tilePixelWH+borderWH)*x,borderWH+(tilePixelWH+borderWH)*y,tilePixelWH,tilePixelWH), 0) 
                else:
                    pygame.draw.rect(screen, red, (borderWH+(tilePixelWH+borderWH)*x,borderWH+(tilePixelWH+borderWH)*y,tilePixelWH,tilePixelWH), 0) 
                if (ms.field[x][y].marked):
                    srf = font.render("!", True, white)
                    screen.blit(srf, ((borderWH+(tilePixelWH+borderWH)*x+tilePixelWH//2.5,borderWH+(tilePixelWH+borderWH)*y+tilePixelWH//4)))
            elif (ms.field[x][y].clicked) and (not ms.field[x][y].mine):
                pygame.draw.rect(screen, white, (borderWH+(tilePixelWH+borderWH)*x,borderWH+(tilePixelWH+borderWH)*y,tilePixelWH,tilePixelWH), 0) 
                font.render(str(ms.field[x][y].neighbourMines), True, blue)
                if ms.field[x][y].neighbourMines > 0:
                    srf = font.render(str(ms.field[x][y].neighbourMines), True, blue)
                    screen.blit(srf, ((borderWH+(tilePixelWH+borderWH)*x+tilePixelWH//2.5,borderWH+(tilePixelWH+borderWH)*y+tilePixelWH//4)))
            else:
                pygame.draw.rect(screen, black, (borderWH+(tilePixelWH+borderWH)*x,borderWH+(tilePixelWH+borderWH)*y,tilePixelWH,tilePixelWH), 0) 
                if (ms.field[x][y].marked):
                    srf = font.render("!", True, white)
                    screen.blit(srf, ((borderWH+(tilePixelWH+borderWH)*x+tilePixelWH//2.5,borderWH+(tilePixelWH+borderWH)*y+tilePixelWH//4)))

def mouseToField(x, y):
    fieldX = int(x / (tilePixelWH+borderWH))
    fieldY = int(y / (tilePixelWH+borderWH))
    return [fieldX, fieldY]
              
def printText(ms, ms_ai, font, screen):
        
    if (ms.gameOver):
        srf = font_text.render("BOOM - Game Over.", True, black)
        screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,10)))
    elif (ms.gameWon):
        srf = font_text.render("Game Won!", True, black)
        screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,10)))
    else:
        srf = font_text.render("Playing..", True, black)
        screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,10)))
            
    srf = font_text.render("Flags: " + str(ms.flagCount), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,40)))
        
    srf = font_text.render("SESSION STATS", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,90)))
    srf = font_text.render("Games: "+ str(won+lost), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,110)))
    if (won+lost>0):
        percentage = round((won/(won+lost))*100,2)
    else:
        percentage = "-" 
    srf = font_text.render("Wins: "+ str(won) + ", "+str(percentage)+"%", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,130)))
    srf = font_text.render("Losses: "+ str(lost), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,150)))
    srf = font_text.render("Best Time: "+ str(round(bestTime,2))+"s", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,170)))
        
    srf = font_text.render("AI STATS", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,200)))
    srf = font_text.render("Moves: "+ str(ms_ai.moves), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,220)))
    srf = font_text.render("Guesses: "+ str(ms_ai.guesses), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,240)))
    if (won+lost > 0):
        srf = font_text.render("Avg time/game: "+ str(round(total_t / (won+lost),2))+"s", True, black)
        screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,260)))
            
    srf = font_text.render("CONTROLS", True, black)
    (srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,310)))
    srf = font_text.render("Left click -> Uncover Tile", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,330)))
    srf = font_text.render("Right click -> Set Mine", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,350)))
    srf = font_text.render("Spacebar -> Reset Game", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,370))) 
    srf = font_text.render("Enter -> Next AI Move", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,390))) 
    srf = font_text.render("L -> Toggle AI Loop", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,410)))
    srf = font_text.render("Miniproject by Sankalp Varshney", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,450))) 
    srf = font_text.render("ML/70/2015272/6th Sem", True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,470)))
            
    srf = font.render(str(fieldCoord[0]) + ", " + str(fieldCoord[1]), True, black)
    screen.blit(srf, ((ms.width*(tilePixelWH+borderWH)+borderWH+10,ms.height*(tilePixelWH+borderWH)+borderWH-60)))

pygame.init()
ms = Minesweeper(width, height, mineCount)
font = pygame.font.SysFont("comicsansms", 12)
font_text = pygame.font.SysFont("arialms", 22)
screen = pygame.display.set_mode((ms.width*(tilePixelWH+borderWH)+borderWH+250, ms.height*(tilePixelWH+borderWH)+borderWH))

bestTime = 0
first = True
running = True
ai_loop = False
waitForNG = False
ms_ai = Minesweeper_AI()

while running:
    fieldCoord = mouseToField(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ms.resetField()
                ms_ai.knowledge = []
                waitForNG = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                mv = ms_ai.move(ms)
                if mv is not None:
                    ms.click(mv[0],mv[1], ms_ai)
                    print("=>"+str(mv))
            if event.key == pygame.K_l:
                start_t = time.perf_counter()
                ai_loop = not ai_loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if (fieldCoord[0] < ms.width) and (fieldCoord[1] < ms.height):
                    ms.click(fieldCoord[0], fieldCoord[1], ms_ai)
            if pygame.mouse.get_pressed()[2]:
                if (fieldCoord[0] < ms.width) and (fieldCoord[1] < ms.height):
                    ms.setFlag(fieldCoord[0], fieldCoord[1])
    if (ai_loop):
        mv = ms_ai.move(ms)
        if mv is not None:
            ms.click(mv[0],mv[1], ms_ai)
            print("=>"+str(mv))
    screen.fill(grey)
    drawMS(screen, font, ms)
    if (ms.gameOver) or (ms.gameWon):
        if (not waitForNG):
            if (ms.gameOver):
                lost += 1
            if (ms.gameWon):
                won += 1
                if first:
                    bestTime = time.perf_counter() - start_t
                    first = False
                else:
                    bestTime = min(bestTime,time.perf_counter() - start_t)
            waitForNG = True
        if (ai_loop):
            end_t = time.perf_counter()
            time_taken = end_t - start_t
            total_t += time_taken
            ms.resetField()
            ms_ai.knowledge = []
            waitForNG = False
            start_t = time.perf_counter()
                
    printText(ms, ms_ai, font_text, screen)
    pygame.display.update()
        
pygame.quit()