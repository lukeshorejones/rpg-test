import math, numpy, os, pygame as pg, random, shutil, time, yaml

from globals import *
from sprites import *
from map import *

def restore_all():
    restore_file('chars.yml')
    restore_file('weapons.yml')

    restore_dir('img')
    restore_dir('music')
    restore_dir('sounds')
    restore_dir('names')
    restore_dir('maps-singleplayer')
    restore_dir('maps-multiplayer')
    restore_dir('img/blue_male')
    restore_dir('img/blue_female')
    restore_dir('img/red_male')
    restore_dir('img/red_female')

    restore_file('img/titlescreen.png')
    restore_file('img/icon.png')

    restore_file('music/title_screen.ogg')
    restore_file('music/game.ogg')
    restore_file('music/win_intro.ogg')
    restore_file('music/win_loop.ogg')
    restore_file('music/lose_intro.ogg')
    restore_file('music/lose_loop.ogg')

    restore_file('sounds/step1.ogg')
    restore_file('sounds/step2.ogg')
    restore_file('sounds/step3.ogg')
    restore_file('sounds/step4.ogg')
    restore_file('sounds/hit.ogg')
    restore_file('sounds/miss.ogg')
    restore_file('sounds/crit.ogg')
    restore_file('sounds/click.ogg')

    restore_file('names/first_names_male.txt')
    restore_file('names/first_names_female.txt')
    restore_file('names/surnames.txt')

    if not os.path.exists('content/README.txt'):
        shutil.copy('basecontent/content_readme/README.txt', 'content')

    for file in os.listdir("basecontent/maps-singleplayer"):
        if file not in os.listdir("content/maps-singleplayer"):
            shutil.copy('basecontent/maps-singleplayer/' + file,'content/maps-singleplayer')

    for file in os.listdir("basecontent/maps-multiplayer"):
        if file not in os.listdir("content/maps-multiplayer"):
            shutil.copy('basecontent/maps-multiplayer/' + file,'content/maps-multiplayer')

    for file in os.listdir("basecontent/img/blue_male"):
        if file not in os.listdir("content/img/blue_male"):
            shutil.copy('basecontent/img/blue_male/' + file,'content/img/blue_male')

    for file in os.listdir("basecontent/img/blue_female"):
        if file not in os.listdir("content/img/blue_female"):
            shutil.copy('basecontent/img/blue_female/' + file,'content/img/blue_female')

    for file in os.listdir("basecontent/img/red_male"):
        if file not in os.listdir("content/img/red_male"):
            shutil.copy('basecontent/img/red_male/' + file,'content/img/red_male')

    for file in os.listdir("basecontent/img/red_female"):
        if file not in os.listdir("content/img/red_female"):
            shutil.copy('basecontent/img/red_female/' + file,'content/img/red_female')

def restore_file(path):
    if not os.path.exists('content/' + path):
        shutil.copy('basecontent/' + path, 'content/' + path)

def restore_dir(path):
    if not os.path.exists('content/' + path):
        os.makedirs('content/' + path)

def import_player_char(i, pos, playerColour):
    stats = []
    duplicatePositions = []

    name = g.charDict.get(i).get('name')
    gender = g.charDict.get(i).get('gender')
    img = str(g.charDict.get(i).get('img'))

    for j in range(len(STAT_NAMES)):
        stats.append(g.charDict.get(i).get('stats').get(STAT_NAMES[j].lower()))
    hp = MAX_HP

    weapon = g.charDict.get(i).get('weapon')
    weapon = g.weaponDict.get(weapon)

    charTextContent = "Name: " + name + " | Gender: " + gender
    for j in range(len(STAT_NAMES)):
        charTextContent += " | " + STAT_NAMES[j] + ": " + str(stats[j])
    charTextContent += " | Equipped: " + weapon.get('name')

    if playerColour == 'blue':
        g.blueCharList.append(BlueChar(name, gender, img, stats, hp, weapon, pos, charTextContent))
    elif playerColour == 'red':
        g.redCharList.append(RedChar(name, gender, img, stats, hp, weapon, pos, charTextContent))

def create_random_enemy(pos):
    stats = []
    duplicatePositions = []

    gender = random.choice(('Male', 'Female'))

    if gender == 'Male':
        name = random.choice(g.first_names_male)
    elif gender == 'Female':
        name = random.choice(g.first_names_female)
    name = name + " " + random.choice(g.surnames)

    stats = copy.copy(ENEMY_STAT_SPREAD)
    random.shuffle(stats)
    hp = MAX_HP

    weapon = random.randint(0,len(g.weaponDict)-1)
    while g.weaponDict.get(weapon).get('stat') != stats.index(max(stats[0], stats[2])):
        weapon = random.randint(0,len(g.weaponDict)-1)

    if weapon == 0:
        img = random.choice((1,2))
    elif weapon == 1 or weapon == 4:
        img = 3
    elif weapon == 2 or weapon == 5:
        img = 4
    elif weapon == 3:
        img = 0
    weapon = g.weaponDict.get(weapon)

    charTextContent = "Name: " + name + " | Gender: " + gender
    for j in range(len(STAT_NAMES)):
        charTextContent += " | " + STAT_NAMES[j] + ": " + str(stats[j])
    charTextContent += " | Equipped: " + weapon.get('name')
    g.redCharList.append(RedChar(name, gender, str(img), stats, hp, weapon, pos, charTextContent))

def animation_update():

    g.bg.mini_update(g)
    g.screen.blit(g.gameMapImg, (-g.camera.posx,-g.camera.posy))
    for j in range(len(g.blueCharList)):
        g.blueCharList[j].update(g)
    for j in range(len(g.redCharList)):
        g.redCharList[j].update(g)
    g.charText.update(g)
    g.turnText.update(g)
    pg.display.flip()

def check_turn_end():
    foundActive = 0

    if g.mode == 'sp':
        for i in range(len(g.blueCharList)):
            if g.blueCharList[i].active == True:
                foundActive = 1
        if foundActive == 0:
            enemy_turn()

    elif g.mode == 'mp':
        if g.turn//2 != g.turn/2:
            for i in range(len(g.blueCharList)):
                if g.blueCharList[i].active == True:
                    foundActive = 1
            if foundActive == 0:
                red_turn()
        elif g.turn//2 == g.turn/2:
            for i in range(len(g.redCharList)):
                if g.redCharList[i].active == True:
                    foundActive = 1
            if foundActive == 0:
                blue_turn()

def blue_turn():
    g.turn += 1
    g.turnText.content = "Turn " + str(g.turn) + " (Blue)"

    g.currentCharList = g.blueCharList
    g.enemyCharList = g.redCharList

    for i in range(len(g.blueCharList)):
        g.blueCharList[i].active = True
        g.blueCharList[i].get_range(g)

    g.camera = g.blueCamera
    turn_change_animation('BLUE')

def red_turn():
    g.turn += 1
    g.turnText.content = "Turn " + str(g.turn) + " (Red)"

    g.currentCharList = g.redCharList
    g.enemyCharList = g.blueCharList

    for i in range(len(g.redCharList)):
        g.redCharList[i].active = True
        g.redCharList[i].get_range(g)

    g.camera = g.redCamera
    turn_change_animation('RED')

def turn_change_animation(team):

    g.turnChangeText.content = team + ' TURN'

    g.bg.update(g)
    g.screen.blit(g.gameMapImg, (-g.camera.posx,-g.camera.posy))
    for j in range(len(g.blueCharList)):
        g.blueCharList[j].update(g)
    for j in range(len(g.redCharList)):
        g.redCharList[j].update(g)

    g.turnChangeText.update(g)
    pg.display.flip()

    time.sleep(1)

def player_turn():
    g.turn += 1
    g.turnText.content = "Turn " + str(g.turn) + " (Player)"

    for i in range(len(g.blueCharList)):
        g.blueCharList[i].active = True
        g.blueCharList[i].get_range(g)

    turn_change_animation('PLAYER')

def damage_calc(currentCharID, enemyCharID):
    dexRoll = random.randint(1,100)
    critRoll = random.randint(1,100)
    dmg = g.currentCharList[currentCharID].stats[g.currentCharList[currentCharID].weapon.get('stat')] * g.currentCharList[currentCharID].weapon.get('damage')
    defenceStat = g.currentCharList[currentCharID].weapon.get('stat') + 1

    g.baseCurrentDamage = max(math.floor(dmg / g.enemyCharList[enemyCharID].stats[defenceStat]), 1)
    g.currentDamage = random.randint(g.baseCurrentDamage-1, g.baseCurrentDamage+1)

    if dexRoll <= 1.5 * g.enemyCharList[enemyCharID].stats[4]:
        g.currentDamage = 0
        g.currentHit = 'miss'
    else:
        g.currentDamage = g.baseCurrentDamage
        g.currentHit = 'hit'
        if critRoll <= 1.5 * g.currentCharList[currentCharID].stats[5]:
            g.currentDamage *= 2
            g.currentHit = 'crit'

    dexRoll = random.randint(1,100)
    critRoll = random.randint(1,100)
    dmg = g.enemyCharList[enemyCharID].stats[g.enemyCharList[enemyCharID].weapon.get('stat')] * g.enemyCharList[enemyCharID].weapon.get('damage')
    defenceStat = g.enemyCharList[enemyCharID].weapon.get('stat') + 1

    g.baseEnemyDamage = max(math.floor(dmg / g.currentCharList[currentCharID].stats[defenceStat]),1)
    g.enemyDamage = random.randint(g.baseEnemyDamage-1, g.baseEnemyDamage+1)

    if dexRoll <= 1.5 * g.currentCharList[currentCharID].stats[4]:
        g.enemyDamage = 0
        g.enemyHit = 'miss'
    else:
        g.enemyDamage = g.baseEnemyDamage
        g.enemyHit = 'hit'
        if critRoll <= 1.5 * g.enemyCharList[enemyCharID].stats[5]:
            g.enemyDamage *= 2
            g.enemyHit = 'crit'

def player_combat(currentCharID, enemyCharID):
    damage_calc(currentCharID, enemyCharID)
    if g.currentCharList[currentCharID].pos[0] > g.enemyCharList[enemyCharID].pos[0]:
        dx = -8
    elif g.currentCharList[currentCharID].pos[0] < g.enemyCharList[enemyCharID].pos[0]:
        dx = 8
    else:
        dx = 0

    if g.currentCharList[currentCharID].pos[1] > g.enemyCharList[enemyCharID].pos[1]:
        dy = -8
    elif g.currentCharList[currentCharID].pos[1] < g.enemyCharList[enemyCharID].pos[1]:
        dy = 8
    else:
        dy = 0

    for i in range(4):
        g.currentCharList[currentCharID].pos = (g.currentCharList[currentCharID].pos[0]+dx, g.currentCharList[currentCharID].pos[1]+dy)
        animation_update()
        time.sleep(MOVE_TIME)

    if g.currentHit == 'hit':
        pg.mixer.Sound.play(g.hit)
    elif g.currentHit == 'crit':
        pg.mixer.Sound.play(g.crit)
    else:
        pg.mixer.Sound.play(g.miss)

    if g.enemyCharList[enemyCharID].hp <= g.currentDamage:
        g.enemyCharList[enemyCharID].hp = 0
        g.enemyCharList.remove(g.enemyCharList[enemyCharID])

        for i in range(4):
            g.currentCharList[currentCharID].pos = (g.currentCharList[currentCharID].pos[0]-dx, g.currentCharList[currentCharID].pos[1]-dy)
            animation_update()
            time.sleep(MOVE_TIME)

        g.currentCharList[currentCharID].active = False

    else:
        g.enemyCharList[enemyCharID].hp -= g.currentDamage

        for i in range(4):
            g.currentCharList[currentCharID].pos = (g.currentCharList[currentCharID].pos[0]-dx, g.currentCharList[currentCharID].pos[1]-dy)
            animation_update()
            time.sleep(MOVE_TIME)

        time.sleep(0.1)
        g.enemyCharList[enemyCharID].get_atk_range(g)

        if g.enemyCharList[enemyCharID].attackRange[g.currentCharList[currentCharID].gridPos[1]][g.currentCharList[currentCharID].gridPos[0]] == 1:
            for i in range(4):
                g.enemyCharList[enemyCharID].pos = (g.enemyCharList[enemyCharID].pos[0]-dx, g.enemyCharList[enemyCharID].pos[1]-dy)
                animation_update()
                time.sleep(MOVE_TIME)

            if g.enemyHit == 'hit':
                pg.mixer.Sound.play(g.hit)
            elif g.enemyHit == 'crit':
                pg.mixer.Sound.play(g.crit)
            else:
                pg.mixer.Sound.play(g.miss)

            if g.currentCharList[currentCharID].hp <= g.enemyDamage:
                g.currentCharList[currentCharID].hp = 0
                g.currentCharList.remove(g.currentCharList[currentCharID])
                for i in range(4):
                    g.enemyCharList[enemyCharID].pos = (g.enemyCharList[enemyCharID].pos[0]+dx, g.enemyCharList[enemyCharID].pos[1]+dy)
                    animation_update()
                    time.sleep(MOVE_TIME)
            else:
                g.currentCharList[currentCharID].hp -= g.enemyDamage
                for i in range(4):
                    g.enemyCharList[enemyCharID].pos = (g.enemyCharList[enemyCharID].pos[0]+dx, g.enemyCharList[enemyCharID].pos[1]+dy)
                    animation_update()
                    time.sleep(MOVE_TIME)
                g.currentCharList[currentCharID].active = False

        else:
            g.currentCharList[currentCharID].active = False

    end_player_combat()

def end_player_combat():
    g.attackTileList = []
    check_turn_end()

def get_pos_atk_range_loop(redCharID, posy, posx, adjacentSquares):
    weaponRange = g.redCharList[redCharID].weapon.get('range')
    for i in range(4):
        if g.distance < weaponRange and g.posAttackRange[adjacentSquares[i][0]][adjacentSquares[i][1]] != 2:
            g.distance += 1
            posx, posy = adjacentSquares[i][1], adjacentSquares[i][0]
            g.posAttackRange[posy][posx] = 1

            get_pos_atk_range_loop(redCharID, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

        elif g.distance == weaponRange:
            g.distance -= 1
            return

    g.distance -= 1

def get_pos_atk_range(redCharID, posy, posx):
    g.distance = 0
    g.posAttackRange = copy.deepcopy(g.gameMap.matrix)
    get_pos_atk_range_loop(redCharID, posy, posx, [[posy, posx+1], [posy-1, posx], [posy, posx-1], [posy+1, posx]])

def enemy_turn():
    g.turn += 1
    g.turnText.content = "Turn " + str(g.turn) + " (Enemy)"
    trueCameraPosx, trueCameraPosy = g.camera.posx, g.camera.posy

    for i in range(len(g.redCharList)):
        g.redCharList[i].active = True

    turn_change_animation('ENEMY')
    animation_update()
    time.sleep(0.5)

    for i in range(len(g.redCharList)):
        indices = []
        moveOptions = []
        attackMoveOptions = []
        rangedAttackMoveOptions = []
        attackOptions = []
        rangedAttackOptions = []

        g.redCharList[i].get_range(g)

        for y in range(len(g.redCharList[i].moveRange)):
            row = numpy.array(g.redCharList[i].moveRange[y])
            indices = numpy.where(row == 1)[0]
            for x in range(len(indices)):
                moveOptions.append((indices[x], y))

        for j in range(len(moveOptions)):
            get_pos_atk_range(i, moveOptions[j][1], moveOptions[j][0])

            for k in range(len(g.blueCharList)):
                if g.posAttackRange[g.blueCharList[k].gridPos[1]][g.blueCharList[k].gridPos[0]] == 1 and moveOptions[j] not in attackMoveOptions:
                    attackMoveOptions.append(moveOptions[j])

                    adjacentSquares = [(moveOptions[j][1], moveOptions[j][0]+1),
                                       (moveOptions[j][1]-1, moveOptions[j][0]),
                                       (moveOptions[j][1], moveOptions[j][0]-1),
                                       (moveOptions[j][1]+1, moveOptions[j][0])]

                    if (g.blueCharList[k].gridPos[1], g.blueCharList[k].gridPos[0]) not in adjacentSquares:
                        rangedAttackMoveOptions.append(moveOptions[j])

        if rangedAttackMoveOptions != []:
            chosenOption = random.choice(rangedAttackMoveOptions)
        elif attackMoveOptions != []:
            chosenOption = random.choice(attackMoveOptions)
        else:
            chosenOption = random.choice(moveOptions)

        startPos = (g.redCharList[i].pos[0],g.redCharList[i].pos[1])
        endPos = (chosenOption[0]*WIDTH,chosenOption[1]*HEIGHT)

        dy = (endPos[1]-startPos[1])/MOVE_STEPS
        dx = (endPos[0]-startPos[0])/MOVE_STEPS

        if dx > 0 and g.redCharList[i].pos[0] < endPos[0]:
            xMoveComplete = False
        elif dx >= 0 and g.redCharList[i].pos[0] >= endPos[0]:
            xMoveComplete = True
        elif dx < 0 and g.redCharList[i].pos[0] > endPos[0]:
            xMoveComplete = False
        elif dx <= 0 and g.redCharList[i].pos[0] <= endPos[0]:
            xMoveComplete = True

        if dy > 0 and g.redCharList[i].pos[1] < endPos[1]:
            yMoveComplete = False
        elif dy >= 0 and g.redCharList[i].pos[1] >= endPos[1]:
            yMoveComplete = True
        elif dy < 0 and g.redCharList[i].pos[1] > endPos[1]:
            yMoveComplete = False
        elif dy <= 0 and g.redCharList[i].pos[1] <= endPos[1]:
            yMoveComplete = True

        while startPos[0]-g.camera.posx < 0:
            g.camera.posx -= 64
        while startPos[0]-g.camera.posx >= DISPLAY_WIDTH:
            g.camera.posx += 64
        while startPos[1]-g.camera.posy < 0:
            g.camera.posy -= 64
        while startPos[1]-g.camera.posy >= DISPLAY_HEIGHT:
            g.camera.posy += 64

        while endPos[0]-g.camera.posx < 0:
            g.camera.posx -= 64
        while endPos[0]-g.camera.posx >= DISPLAY_WIDTH:
            g.camera.posx += 64
        while endPos[1]-g.camera.posy < 0:
            g.camera.posy -= 64
        while endPos[1]-g.camera.posy >= DISPLAY_HEIGHT:
            g.camera.posy += 64

        g.charText.content = g.redCharList[i].charTextContent
        animation_update()

        while xMoveComplete == False or yMoveComplete == False:
            g.redCharList[i].pos = (g.redCharList[i].pos[0]+dx, g.redCharList[i].pos[1]+dy)
            g.charText.content = g.redCharList[i].charTextContent
            animation_update()

            if pg.mixer.get_busy() == False:
                step = random.randint(0,3)
                pg.mixer.Sound.play(g.steps[step])

            if dx > 0 and g.redCharList[i].pos[0] < endPos[0]:
                    xMoveComplete = False
            elif dx >= 0 and g.redCharList[i].pos[0] >= endPos[0]:
                    xMoveComplete = True
            elif dx < 0 and g.redCharList[i].pos[0] > endPos[0]:
                    xMoveComplete = False
            elif dx <= 0 and g.redCharList[i].pos[0] <= endPos[0]:
                    xMoveComplete = True

            if dy > 0 and g.redCharList[i].pos[1] < endPos[1]:
                    yMoveComplete = False
            elif dy >= 0 and g.redCharList[i].pos[1] >= endPos[1]:
                    yMoveComplete = True
            elif dy < 0 and g.redCharList[i].pos[1] > endPos[1]:
                    yMoveComplete = False
            elif dy <= 0 and g.redCharList[i].pos[1] <= endPos[1]:
                    yMoveComplete = True

            time.sleep(MOVE_TIME)

        g.redCharList[i].pos = (chosenOption[0]*WIDTH,chosenOption[1]*HEIGHT)

        if attackMoveOptions != []:
            g.redCharList[i].get_atk_range(g)

            for j in range(len(g.blueCharList)):
                if g.redCharList[i].attackRange[g.blueCharList[j].gridPos[1]][g.blueCharList[j].gridPos[0]] == 1:
                    attackOptions.append(j)

                    adjacentSquares = [(g.redCharList[i].gridPos[1], g.redCharList[i].gridPos[0]+1),
                                       (g.redCharList[i].gridPos[1]-1, g.redCharList[i].gridPos[0]),
                                       (g.redCharList[i].gridPos[1], g.redCharList[i].gridPos[0]-1),
                                       (g.redCharList[i].gridPos[1]+1, g.redCharList[i].gridPos[0])]

                    if (g.blueCharList[j].gridPos[1], g.blueCharList[j].gridPos[0]) not in adjacentSquares:
                        rangedAttackOptions.append(j)

            if rangedAttackOptions != []:
                blueCharID = random.choice(rangedAttackOptions)
            else:
                blueCharID = random.choice(attackOptions)

            damage_calc(blueCharID, i)

            if g.blueCharList[blueCharID].pos[0] > g.redCharList[i].pos[0]:
                dx = -8
            elif g.blueCharList[blueCharID].pos[0] < g.redCharList[i].pos[0]:
                dx = 8
            else:
                dx = 0

            if g.blueCharList[blueCharID].pos[1] > g.redCharList[i].pos[1]:
                dy = -8
            elif g.blueCharList[blueCharID].pos[1] < g.redCharList[i].pos[1]:
                dy = 8
            else:
                dy = 0

            time.sleep(0.1)
            g.blueCharList[blueCharID].get_atk_range(g)
            if g.blueCharList[blueCharID].hp <= g.baseEnemyDamage or g.redCharList[i].hp > g.baseCurrentDamage or g.blueCharList[blueCharID].attackRange[g.redCharList[i].gridPos[1]][g.redCharList[i].gridPos[0]] == 0:

                for j in range(4):
                    g.redCharList[i].pos = (g.redCharList[i].pos[0]-dx, g.redCharList[i].pos[1]-dy)
                    animation_update()
                    time.sleep(MOVE_TIME)

                if g.enemyHit == 'hit':
                    pg.mixer.Sound.play(g.hit)
                elif g.enemyHit == 'crit':
                    pg.mixer.Sound.play(g.crit)
                else:
                    pg.mixer.Sound.play(g.miss)

                if g.blueCharList[blueCharID].hp <= g.enemyDamage:
                    g.blueCharList[blueCharID].hp = 0
                    g.blueCharList.remove(g.blueCharList[blueCharID])

                    for j in range(4):
                        g.redCharList[i].pos = (g.redCharList[i].pos[0]+dx, g.redCharList[i].pos[1]+dy)
                        animation_update()
                        time.sleep(MOVE_TIME)

                else:
                    g.blueCharList[blueCharID].hp -= g.enemyDamage

                    for j in range(4):
                        g.redCharList[i].pos = (g.redCharList[i].pos[0]+dx, g.redCharList[i].pos[1]+dy)
                        animation_update()
                        time.sleep(MOVE_TIME)

                    if g.blueCharList[blueCharID].attackRange[g.redCharList[i].gridPos[1]][g.redCharList[i].gridPos[0]] == 1:
                        time.sleep(0.1)

                        for j in range(4):
                            g.blueCharList[blueCharID].pos = (g.blueCharList[blueCharID].pos[0]+dx, g.blueCharList[blueCharID].pos[1]+dy)
                            animation_update()
                            time.sleep(MOVE_TIME)

                        if g.currentHit == 'hit':
                            pg.mixer.Sound.play(g.hit)
                        elif g.currentHit == 'crit':
                            pg.mixer.Sound.play(g.crit)
                        else:
                            pg.mixer.Sound.play(g.miss)

                        if g.redCharList[i].hp <= g.currentDamage:
                            g.redCharList[i].hp = 0
                            g.redCharList.remove(g.redCharList[i])
                        else:
                            g.redCharList[i].hp -= g.currentDamage

                        for j in range(4):
                            g.blueCharList[blueCharID].pos = (g.blueCharList[blueCharID].pos[0]-dx, g.blueCharList[blueCharID].pos[1]-dy)
                            animation_update()
                            time.sleep(MOVE_TIME)

        g.redCharList[i].active = False

        g.charText.content = g.redCharList[i].charTextContent
        animation_update()
        time.sleep(0.5)

    g.camera.posx, g.camera.posy = trueCameraPosx, trueCameraPosy
    animation_update()
    player_turn()

def mouse_hover():
    anySelected = False

    if g.attackTileList == []:
        for i in range(len(g.blueCharList)):
            if g.gridx == g.blueCharList[i].gridPos[0] and g.gridy == g.blueCharList[i].gridPos[1]:
                anySelected = True
                g.charText.content = g.blueCharList[i].charTextContent
                g.blueCharList[i].get_range(g)

                g.preMoveTileList = []
                for row in range(len(g.blueCharList[i].moveRange)):
                    for column in range(len(g.blueCharList[i].moveRange[row])):
                        if g.blueCharList[i].moveRange[row][column] == 1 and g.moveTileList == []:
                                g.preMoveTileList.append(PreMoveTile((column,row),'blue',g.blueCharList[i].active))

        for i in range(len(g.redCharList)):
            if g.gridx == g.redCharList[i].gridPos[0] and g.gridy == g.redCharList[i].gridPos[1]:
                anySelected = True
                g.charText.content = g.redCharList[i].charTextContent
                g.redCharList[i].get_range(g)

                g.preMoveTileList = []
                for row in range(len(g.redCharList[i].moveRange)):
                    for column in range(len(g.redCharList[i].moveRange[row])):
                        if g.redCharList[i].moveRange[row][column] == 1 and g.moveTileList == []:
                            g.preMoveTileList.append(PreMoveTile((column,row),'red',g.redCharList[i].active))

    if anySelected == False:
        g.charText.content = ""
        g.preMoveTileList = []

def mouse_down(button):
    if button == 1: #LEFT MOUSE BUTTON
        for i in range(len(g.attackTileList)):
            if g.gridx == g.attackTileList[i].gridPos[0] and g.gridy == g.attackTileList[i].gridPos[1]:
                click_attack_tile(i)
                return

        if g.attackTileList == []:
            for i in range(len(g.moveTileList)):
                if g.gridx == g.moveTileList[i].gridPos[0] and g.gridy == g.moveTileList[i].gridPos[1]:
                    click_move_tile(i)
                    return

            for i in range(len(g.blueCharList)):
                if g.turn//2 != g.turn/2 and g.gridx == g.blueCharList[i].gridPos[0] and g.gridy == g.blueCharList[i].gridPos[1] and g.blueCharList[i].active == True:
                    g.colour = 'blue'
                    click_char(i)
                    return

            for i in range(len(g.redCharList)):
                if g.turn//2 == g.turn/2 and g.gridx == g.redCharList[i].gridPos[0] and g.gridy == g.redCharList[i].gridPos[1] and g.redCharList[i].active == True:
                    g.colour = 'red'
                    click_char(i)
                    return

        g.moveTileList = []

    elif button == 3:
        g.moveTileList = []
        if g.attackTileList != []:
            g.attackTileList = []
            g.blueCharList[g.selectedCharID].active = False
            check_turn_end()

def click_char(i):

    g.selectedCharID = i
    g.moveTileList = []
    g.preMoveTileList = []
    pg.mixer.Sound.play(g.click)
    for row in range(len(g.currentCharList[i].moveRange)):
        for column in range(len(g.currentCharList[i].moveRange[row])):
            if g.currentCharList[i].moveRange[row][column] == 1:
                g.moveTileList.append(MoveTile((column,row),g.colour))

def click_move_tile(i):

    startPos = (g.currentCharList[g.selectedCharID].pos[0],g.currentCharList[g.selectedCharID].pos[1])
    endPos = (g.moveTileList[i].gridPos[0]*WIDTH,g.moveTileList[i].gridPos[1]*HEIGHT)

    dy = (endPos[1]-startPos[1])/MOVE_STEPS
    dx = (endPos[0]-startPos[0])/MOVE_STEPS

    if dx > 0 and g.currentCharList[g.selectedCharID].pos[0] < endPos[0]:
        xMoveComplete = False
    elif dx >= 0 and g.currentCharList[g.selectedCharID].pos[0] >= endPos[0]:
        xMoveComplete = True
    elif dx < 0 and g.currentCharList[g.selectedCharID].pos[0] > endPos[0]:
        xMoveComplete = False
    elif dx <= 0 and g.currentCharList[g.selectedCharID].pos[0] <= endPos[0]:
        xMoveComplete = True

    if dy > 0 and g.currentCharList[g.selectedCharID].pos[1] < endPos[1]:
        yMoveComplete = False
    elif dy >= 0 and g.currentCharList[g.selectedCharID].pos[1] >= endPos[1]:
        yMoveComplete = True
    elif dy < 0 and g.currentCharList[g.selectedCharID].pos[1] > endPos[1]:
        yMoveComplete = False
    elif dy <= 0 and g.currentCharList[g.selectedCharID].pos[1] <= endPos[1]:
        yMoveComplete = True

    while xMoveComplete == False or yMoveComplete == False:
        g.currentCharList[g.selectedCharID].pos = (g.currentCharList[g.selectedCharID].pos[0]+dx, g.currentCharList[g.selectedCharID].pos[1]+dy)
        animation_update()

        if pg.mixer.get_busy() == False:
            step = random.randint(0,3)
            pg.mixer.Sound.play(g.steps[step])

        if dx > 0 and g.currentCharList[g.selectedCharID].pos[0] < endPos[0]:
            xMoveComplete = False
        elif dx >= 0 and g.currentCharList[g.selectedCharID].pos[0] >= endPos[0]:
            xMoveComplete = True
        elif dx < 0 and g.currentCharList[g.selectedCharID].pos[0] > endPos[0]:
                xMoveComplete = False
        elif dx <= 0 and g.currentCharList[g.selectedCharID].pos[0] <= endPos[0]:
            xMoveComplete = True

        if dy > 0 and g.currentCharList[g.selectedCharID].pos[1] < endPos[1]:
            yMoveComplete = False
        elif dy >= 0 and g.currentCharList[g.selectedCharID].pos[1] >= endPos[1]:
            yMoveComplete = True
        elif dy < 0 and g.currentCharList[g.selectedCharID].pos[1] > endPos[1]:
            yMoveComplete = False
        elif dy <= 0 and g.currentCharList[g.selectedCharID].pos[1] <= endPos[1]:
            yMoveComplete = True
        time.sleep(MOVE_TIME)

    g.currentCharList[g.selectedCharID].pos = (g.moveTileList[i].gridPos[0]*WIDTH, g.moveTileList[i].gridPos[1]*HEIGHT)
    g.moveTileList = []

    g.currentCharList[g.selectedCharID].get_atk_range(g)

    for j in range(len(g.enemyCharList)):
        if g.currentCharList[g.selectedCharID].attackRange[g.enemyCharList[j].gridPos[1]][g.enemyCharList[j].gridPos[0]] == 1:
            g.attackTileList.append(AttackTile((g.enemyCharList[j].gridPos[0], g.enemyCharList[j].gridPos[1])))

    if g.attackTileList == []:
        g.currentCharList[g.selectedCharID].active = False
        check_turn_end()

def click_attack_tile(i):
    for charID in range(len(g.enemyCharList)):
        if g.enemyCharList[charID].gridPos[0] == g.attackTileList[i].gridPos[0] and g.enemyCharList[charID].gridPos[1] == g.attackTileList[i].gridPos[1]:
            player_combat(g.selectedCharID, charID)
            return

class Game:
    def __init__(self):
        # initialise game window
        pg.init()
        restore_all()

        self.charDict = yaml.load(open('content/chars.yml'))
        self.weaponDict = yaml.load(open('content/weapons.yml'))
        self.first_names_male = open("content/names/first_names_male.txt", "r").read().split(', ')
        self.first_names_female = open("content/names/first_names_female.txt", "r").read().split(', ')
        self.surnames = open("content/names/surnames.txt", "r").read().split(', ')

        iconSurface = pg.image.load("content/img/icon.png")

        pg.display.set_caption(TITLE)
        pg.display.set_icon(iconSurface)

        if FULLSCREEN == True:
            self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        self.clock = pg.time.Clock()

        self.steps = []
        for i in range(4):
            self.steps.append(pg.mixer.Sound('content/sounds/step' + str(i+1) + '.ogg'))
        self.hit = pg.mixer.Sound('content/sounds/hit.ogg')
        self.miss = pg.mixer.Sound('content/sounds/miss.ogg')
        self.crit = pg.mixer.Sound('content/sounds/crit.ogg')
        self.click = pg.mixer.Sound('content/sounds/click.ogg')

        for i in range(4):
            self.steps[i].set_volume(1.2*VOLUME)
        self.hit.set_volume(0.2*VOLUME)
        self.miss.set_volume(0.3*VOLUME)
        self.crit.set_volume(0.2*VOLUME)
        self.click.set_volume(0.5*VOLUME)

        self.fade = Fade()
        self.running = True

    def new(self):
        self.blueCharList = []
        self.redCharList = []
        self.preMoveTileList = []
        self.moveTileList = []
        self.attackTileList = []
        self.turn = 1

        self.bg = Background()

        g.currentCharList = g.blueCharList
        g.enemyCharList = g.redCharList

        if self.mode == 'sp':
            self.new_sp()
        elif self.mode == 'mp':
            self.new_mp()

    def new_sp(self):
        # start new game

        self.gameMap = Map(random.choice(self.maps_sp))
        self.gameMapImg = self.gameMap.make_map()

        self.cursor = Cursor()
        self.turnChangeText = CenterText("", (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2), 70, WHITE)
        self.turnText = Text("Turn " + str(self.turn) + " (Player)", (10,10), 20, WHITE)
        self.charText = Text("", (10,DISPLAY_HEIGHT-32), 20, WHITE)

        for i in range(len(self.gameMap.blueSpawns)):
            import_player_char(BLUE_PARTY[i], self.gameMap.blueSpawns[i], 'blue')
            self.blueCharList[i].moveRange = []

        for i in range(len(self.gameMap.redSpawns)):
            create_random_enemy(self.gameMap.redSpawns[i])
            self.redCharList[i].moveRange = []

        for i in range(len(self.blueCharList)):
            self.blueCharList[i].get_range(g)
        for i in range(len(self.redCharList)):
            self.redCharList[i].get_range(g)

        self.blueCamera = BlueCamera(g)
        self.camera = self.blueCamera

        pg.mixer.music.load('content/music/game.ogg')
        pg.mixer.music.play(-1)
        self.fade.start_fadein(g)
        self.run()

    def new_mp(self):
        # start new game

        self.gameMap = Map(random.choice(self.maps_mp))
        self.gameMapImg = self.gameMap.make_map()

        self.cursor = Cursor()
        self.turnChangeText = CenterText("", (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2), 70, WHITE)
        self.turnText = Text("Turn " + str(self.turn) + " (Blue)", (10,10), 20, WHITE)
        self.charText = Text("", (10,DISPLAY_HEIGHT-32), 20, WHITE)

        for i in range(len(self.gameMap.blueSpawns)):
            import_player_char(BLUE_PARTY[i], self.gameMap.blueSpawns[i], 'blue')
            self.blueCharList[i].moveRange = []

        for i in range(len(self.gameMap.redSpawns)):
            import_player_char(RED_PARTY[i], self.gameMap.redSpawns[i], 'red')
            self.redCharList[i].moveRange = []

        for i in range(len(self.blueCharList)):
            self.blueCharList[i].get_range(g)
        for i in range(len(self.redCharList)):
            self.redCharList[i].get_range(g)

        self.blueCamera = BlueCamera(g)
        self.redCamera = RedCamera(g)

        self.camera = self.blueCamera

        pg.mixer.music.load('content/music/game.ogg')
        pg.mixer.music.play(-1)
        self.fade.start_fadein(g)
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()

    def update(self):
        # game loop - update
        self.bg.update(g)
        self.screen.blit(self.gameMapImg, (-g.camera.posx,-g.camera.posy))

        for i in range(len(self.preMoveTileList)):
            self.preMoveTileList[i].update(g)
        for i in range(len(self.moveTileList)):
            self.moveTileList[i].update(g)
        for i in range(len(self.attackTileList)):
            self.attackTileList[i].update(g)
        for i in range(len(self.blueCharList)):
            self.blueCharList[i].update(g)
        for i in range(len(self.redCharList)):
            self.redCharList[i].update(g)

        self.cursor.update(g)
        self.charText.update(g)
        self.turnText.update(g)
        mouse_hover()

        pg.display.flip()

        if g.blueCharList == [] and g.redCharList == []:
            self.result = "tie"
            self.playing = False
        elif g.redCharList == []:
            self.result = "blue"
            self.playing = False
        elif g.blueCharList == []:
            self.result = "red"
            self.playing = False

    def events(self):
        # game loop - events
        self.x, self.y = pg.mouse.get_pos()
        self.gridx, self.gridy = self.x//(WIDTH) + g.camera.posx//(WIDTH), self.y//(HEIGHT) + g.camera.posy//(HEIGHT)

        pressed = pg.key.get_pressed()
        if (g.camera.posx > 0) and (pressed[pg.K_LEFT] or pressed[pg.K_a]):
            g.camera.posx -= WIDTH
        if (DISPLAY_WIDTH < g.gameMap.width-g.camera.posx) and (pressed[pg.K_RIGHT] or pressed[pg.K_d]):
            g.camera.posx += WIDTH
        if (g.camera.posy > 0) and (pressed[pg.K_UP] or pressed[pg.K_w]):
            g.camera.posy -= HEIGHT
        if (DISPLAY_HEIGHT < g.gameMap.height-g.camera.posy) and (pressed[pg.K_DOWN] or pressed[pg.K_s]):
            g.camera.posy += HEIGHT

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_down(event.button)

    def update_start_screen(self):
        self.x, self.y = pg.mouse.get_pos()

        self.screen.blit(self.startScreenMapImg, self.startScreenPos)
        self.screen.blit(self.startScreenImg, (0,0))
        self.titleText.update(g)

        for i in range(len(self.titleOptions)):
            if self.titleOptions[i].rect.collidepoint((self.x, self.y)):
                self.titleOptions[i].hover()
            else:
                self.titleOptions[i].no_hover()
            self.titleOptions[i].update(g)

        pg.display.flip()

        startScreenPos = list(self.startScreenPos)
        if startScreenPos[0] + self.startScreenVelX < self.startScreenMinX or startScreenPos[0] + self.startScreenVelX > 0:
            self.startScreenVelX *= -1
        if startScreenPos[1] + self.startScreenVelY < self.startScreenMinY or startScreenPos[1] + self.startScreenVelY > 0:
            self.startScreenVelY *= -1
        startScreenPos[0] += self.startScreenVelX
        startScreenPos[1] += self.startScreenVelY
        self.startScreenPos = tuple(startScreenPos)

    def start_screen(self):
        # show start screen
        self.maps_sp = []
        self.maps_mp = []
        self.titleOptions = []

        for file in os.listdir("content/maps-singleplayer"):
            if file.endswith(".tmx"):
                self.maps_sp.append(os.path.join("content/maps-singleplayer", file))
        for file in os.listdir("content/maps-multiplayer"):
            if file.endswith(".tmx"):
                self.maps_mp.append(os.path.join("content/maps-multiplayer", file))
        self.maps = self.maps_sp + self.maps_mp

        self.startScreenMap = Map(random.choice(self.maps))
        self.startScreenMapImg = self.startScreenMap.make_map()
        self.startScreenMapImg = pg.transform.scale(self.startScreenMapImg, (int(self.startScreenMap.width*2),int(self.startScreenMap.height*2)))

        self.startScreenImg = pg.image.load('content/img/titlescreen.png')
        self.titleText = Text(TITLE, (70,70), 50, WHITE)

        self.titleOptions.append(TitleOption(g, 'Single Player', 30, WHITE))
        self.titleOptions.append(TitleOption(g, 'Multiplayer', 30, WHITE))
        self.titleOptions.append(TitleOption(g, 'Configure Game', 30, WHITE))

        self.startScreenMinX = DISPLAY_WIDTH-self.startScreenMap.width*2
        self.startScreenMinY = DISPLAY_HEIGHT-self.startScreenMap.height*2
        self.startScreenPos = (random.randint(self.startScreenMinX,0),random.randint(self.startScreenMinY,0))
        self.startScreenVelX = random.randint(-int(START_SCREEN_SPEED),int(START_SCREEN_SPEED))/10
        self.startScreenVelY = random.choice((math.sqrt((int(START_SCREEN_SPEED)/10)**2 - self.startScreenVelX**2),  -math.sqrt((int(START_SCREEN_SPEED)/10)**2 - self.startScreenVelX**2)))

        self.fade.end_fadein(g)

        pg.mixer.music.load('content/music/title_screen.ogg')
        pg.mixer.music.set_volume(0.4*VOLUME)
        pg.mixer.music.play(-1)

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            g.update_start_screen()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(len(self.titleOptions)):

                        if self.titleOptions[i].rect.collidepoint((self.x, self.y)):
                            if i == 0:
                                self.mode = 'sp'
                                pg.mixer.music.stop()
                                pg.mixer.Sound.play(g.click)
                                pg.mouse.set_visible(False)
                                self.fade.start_fadeout(g)
                                waiting = False
                            if i == 1:
                                self.mode = 'mp'
                                pg.mixer.music.stop()
                                pg.mixer.Sound.play(g.click)
                                pg.mouse.set_visible(False)
                                self.fade.start_fadeout(g)
                                waiting = False
                            if i == 2:
                                pg.mixer.Sound.play(g.click)
                                os.startfile('content')

    def end_screen(self):
        # show end screen (game over)
        if not self.running:
            return

        pg.mouse.set_visible(True)
        self.endScreenDialogue = EndScreenDialogue()

        if self.result == 'blue':
            if self.mode == 'sp':
                self.endText = CenterText(WIN_TEXT, (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2-15), 40, WHITE)
            else:
                self.endText = CenterText("Blue Wins", (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2-15), 40, WHITE)

        elif self.result == 'red':
            if self.mode == 'sp':
                self.endText = CenterText(LOSE_TEXT, (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2-15), 40, WHITE)
            else:
                self.endText = CenterText("Red Wins", (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2-15), 40, WHITE)

        elif self.result == 'tie':
            self.endText = CenterText(TIE_TEXT, (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2-15), 40, WHITE)
        self.endSubText = CenterText("Press any key", (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2+25 ), 20, WHITE)

        self.screen.blit(self.gameMapImg, (-g.camera.posx,-g.camera.posy))
        for i in range(len(self.blueCharList)):
            self.blueCharList[i].update(g)
        for i in range(len(self.redCharList)):
            self.redCharList[i].update(g)

        self.endScreenDialogue.update(g)
        self.endText.update(g)
        self.endSubText.update(g)

        pg.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    pg.mixer.music.stop()
                    self.fade.end_fadeout(g)
                    waiting = False
                    g.start_screen()

g = Game()
g.start_screen()

while g.running:
    g.new()
    g.end_screen()

pg.quit()
quit()
