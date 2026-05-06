import pygame
import sys
import time
import random
from bullet import Bullet
from emp import Ino
from boss import Boss
from boss2 import Boss2
from boss3 import Boss3
from boss_tck import BossTck
from mmp8 import Mmp8

# Р”РѕРґР°С”РјРѕ РіР»РѕР±Р°Р»СЊРЅСѓ Р·РјС–РЅРЅСѓ РґР»СЏ РєРѕРЅС‚СЂРѕР»СЋ С‡Р°СЃС‚РѕС‚Рё СЃС‚СЂС–Р»СЊР±Рё
last_shot_time = 0
SHOT_DELAY = 150  # Р—РјРµРЅС€СѓС”РјРѕ Р·Р°С‚СЂРёРјРєСѓ РјС–Р¶ РїРѕСЃС‚СЂС–Р»Р°РјРё РґРѕ 150РјСЃ (Р±СѓР»Рѕ 250РјСЃ)

def events(screen, gun, bullets, stats, boss=None, inos=None):
    """РћР±СЂРѕР±РєР° РїРѕРґС–Р№"""
    global last_shot_time
    
    # РџРµСЂРµРІС–СЂСЏС”РјРѕ РЅР°С‚РёСЃРєР°РЅРЅСЏ РєРЅРѕРїРєРё РјРёС€С–
    current_time = pygame.time.get_ticks()
    
    current_shot_delay = max(50, SHOT_DELAY - getattr(stats, 'fire_rate_level', 0) * 10)
    
    if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_SPACE]:
        if current_time - last_shot_time > current_shot_delay:
            has_db = getattr(stats, 'double_bullet_timer', 0) > current_time
            if getattr(stats, 'has_extra_bullet', False) or has_db:
                b1 = Bullet(screen, gun, stats)
                b1.rect.centerx -= 20
                b1.x -= 20
                b2 = Bullet(screen, gun, stats)
                b2.rect.centerx += 20
                b2.x += 20
                bullets.add(b1)
                bullets.add(b2)
            else:
                new_bullet = Bullet(screen, gun, stats)
                bullets.add(new_bullet)
            last_shot_time = current_time

    # РћР±СЂРѕР±РєР° РєР»Р°РІС–С€
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_d:
                gun.mright = True
            elif event.key == pygame.K_a:
                gun.mleft = True
            elif event.key == pygame.K_w:
                gun.mup = True
            elif event.key == pygame.K_s:
                gun.mdown = True
            # Active Abilities
            elif event.key == pygame.K_z:
                actives = getattr(stats, 'actives', {})
                if actives.get('wave_clear', 0) > 0 and boss is None and inos is not None:
                    actives['wave_clear'] -= 1
                    for ino in inos:
                        ino.take_damage(999999)
            elif event.key == pygame.K_x:
                actives = getattr(stats, 'actives', {})
                if actives.get('invincibility', 0) > 0:
                    actives['invincibility'] -= 1
                    stats.invincible_wave = getattr(stats, 'wave', 1)
            elif event.key == pygame.K_c:
                actives = getattr(stats, 'actives', {})
                if actives.get('boss_half_hp', 0) > 0 and boss is not None:
                    actives['boss_half_hp'] -= 1
                    if hasattr(boss, 'health'):
                        boss.health //= 2
            elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_q and getattr(stats, 'has_super_mode', False):
                if current_time > getattr(stats, 'super_mode_cooldown', 0):
                    stats.super_mode_active = True
                    stats.super_mode_end_time = current_time + 10000
                    stats.super_mode_cooldown = current_time + 40000
            elif event.key == pygame.K_e and getattr(stats, 'has_money_mode', False):
                if current_time > getattr(stats, 'money_mode_cooldown', 0):
                    stats.money_mode_active = True
                    stats.money_mode_end_time = current_time + 30000
                    stats.money_mode_cooldown = current_time + 60000
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                gun.mright = False
            elif event.key == pygame.K_a:
                gun.mleft = False
            elif event.key == pygame.K_w:
                gun.mup = False
            elif event.key == pygame.K_s:
                gun.mdown = False

def update(bg_color, screen, stats, sc, gun, inos, bullets, boss, bunkers=None, drops=None):
    """РћРЅРѕРІР»РµРЅРЅСЏ РµРєСЂР°РЅСѓ"""
    sc.show_score()

    # РњР°Р»СЋС”РјРѕ РїСЂРµРіСЂР°РґРё
    if bunkers:
        for bunker in bunkers.sprites():
            bunker.draw()

    # РњР°Р»СЋС”РјРѕ РІСЃС– РєСѓР»С–
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    if drops is not None:
        drops.draw(screen)

    gun.output()
    inos.draw(screen)

    # РћРЅРѕРІР»СЋС”РјРѕ С‚Р° РјР°Р»СЋС”РјРѕ Р±РѕСЃР°
    if boss:
        boss.update()
        boss.draw()
        # РњР°Р»СЋС”РјРѕ РєСѓР»С– Р±РѕСЃР°
        for bullet in boss.bullets:
            bullet.draw_bullet()

    pygame.display.flip()

def update_bullets(screen, stats, sc, inos, bullets, boss, bunkers=None, drops=None):
    """РћРЅРѕРІР»РµРЅРЅСЏ РїРѕР·РёС†С–С— РєСѓР»СЊ"""
    current_time = pygame.time.get_ticks()
    
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    if bunkers:
        collisions_b = pygame.sprite.groupcollide(bullets, bunkers, True, False)
        for bullet, hit_bunkers in collisions_b.items():
            for bunker in hit_bunkers:
                bunker.take_damage(bullet.damage)
                
        if boss:
            collisions_boss_b = pygame.sprite.groupcollide(boss.bullets, bunkers, True, False)
            for boss_bullet, hit_bunkers in collisions_boss_b.items():
                for bunker in hit_bunkers:
                    damage = getattr(boss_bullet, 'damage', 10)
                    bunker.take_damage(damage)
            
    collisions = pygame.sprite.groupcollide(bullets, inos, True, False)
    if collisions:
        from drops import Drop
        for bullet, hit_inos in collisions.items():
            for ino in hit_inos:
                ino.take_damage(bullet.damage)
                if getattr(ino, 'health', 0) <= 0:
                    if drops is not None and random.random() < 0.2:
                        drops.add(Drop(screen, ino.rect.centerx, ino.rect.centery))
                    ino.kill()
                    points = 10
                    stats.score += points
                    stats.current_life_score += points
                    stats.money += int(1 * stats.get_money_multiplier())
                    stats.save_upgrades()
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    
    if len(inos) == 0 and boss is None:
        stats.wave = getattr(stats, 'wave', 1) + 1
        stats.max_wave_unlocked = max(getattr(stats, 'max_wave_unlocked', 1), stats.wave)
        stats.save_upgrades()
        if hasattr(sc, 'image_wave'):
            sc.image_wave()
        bullets.empty()
        
        extra_rows = getattr(stats, 'wave', 1) // 3
        create_army(screen, inos, bunkers, extra_rows, stats)
        
        def scale_boss(boss_inst):
            multiplier = 1 + (stats.wave - 1) * 0.25
            if hasattr(boss_inst, 'health'):
                boss_inst.health = int(boss_inst.health * multiplier)
            if hasattr(boss_inst, 'speed'):
                boss_inst.speed *= (1 + (stats.wave - 1) * 0.05)
            if hasattr(boss_inst, 'speed_x'):
                boss_inst.speed_x *= (1 + (stats.wave - 1) * 0.05)
            return boss_inst
            
        if stats.wave >= 15:
            boss_choice = random.choice([Boss, Boss2, Boss3, BossTck])
            boss = boss_choice(screen)
            return scale_boss(boss)
        else:
            if stats.wave % 2 == 0:
                inos.empty()
                boss_choice = random.choice([Boss, Boss2, Boss3, BossTck])
                boss = boss_choice(screen)
                return scale_boss(boss)
    
    if boss:
        boss_hit = pygame.sprite.spritecollide(boss, bullets, True)
        if boss_hit:
            points = 50
            stats.score += points
            stats.current_life_score += points
            sc.image_score()
            check_high_score(stats, sc)
            for bullet in boss_hit:
                boss.take_damage(bullet.damage)
            if boss.health <= 0:
                points = 500
                stats.score += points
                stats.current_life_score += points
                stats.money += int(100 * stats.get_money_multiplier())
                stats.save_upgrades()
                sc.image_score()
                check_high_score(stats, sc)
                stats.armies_defeated = 0
                return None
    return boss

def gun_kill(stats, screen, sc, gun, inos, bullets, bunkers=None, boss=None):
    """Р—С–С‚РєРЅРµРЅРЅСЏ РіР°СЂРјР°С‚Рё С‚Р° Р°СЂРјС–С—"""
    if stats.guns_left > 0:
        stats.update_life_score()  # Р—Р±РµСЂС–РіР°С”РјРѕ РѕС‡РєРё Р·Р° РїРѕС‚РѕС‡РЅРµ Р¶РёС‚С‚СЏ
        stats.current_life_score = 0  # РЎРєРёРґР°С”РјРѕ РѕС‡РєРё РґР»СЏ РЅРѕРІРѕРіРѕ Р¶РёС‚С‚СЏ
        stats.guns_left -= 1
        inos.empty()
        bullets.empty()
        if boss:
            boss.bullets.empty()
        extra_rows = 0
        if getattr(stats, 'wave', 1) >= 15:
            extra_rows = getattr(stats, 'wave', 1) // 15
        create_army(screen, inos, bunkers, extra_rows, stats)
        gun.create_gun()
        import time
        time.sleep(1)
    else:
        stats.run_game = False
        # Р¤С–РЅР°Р»СЊРЅРµ РѕРЅРѕРІР»РµРЅРЅСЏ РѕС‡РєС–РІ Р·Р° РѕСЃС‚Р°РЅРЅС” Р¶РёС‚С‚СЏ
        stats.update_life_score()

def inos_check(stats, screen, sc, gun, inos, bullets, bunkers=None, boss=None):
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets, bunkers, boss)
            return True
    return False

def update_inos(stats, screen, sc, gun, inos, bullets, boss, bunkers=None):
    """РћРЅРѕРІР»РµРЅРЅСЏ РїРѕР·РёС†С–С— РІРѕСЂРѕРіС–РІ"""
    inos.update(getattr(stats, 'wave', 1))
    
    current_time = pygame.time.get_ticks()
    new_inos = []
    for ino in inos.sprites():
        if getattr(ino, 'is_mmp8', False):
            if current_time - getattr(ino, 'last_spawn_time', 0) > 1000: # РЎРїР°РІРЅ РєРѕР¶РЅСѓ СЃРµРєСѓРЅРґСѓ (С‡Р°СЃС‚С–С€Рµ)
                from emp import Ino
                evader = Ino(screen)
                if stats:
                    evader.apply_skin(stats.get_enemy_color())
                evader.rect.centerx = ino.rect.centerx
                evader.rect.top = ino.rect.bottom
                evader.y = float(evader.rect.y)
                new_inos.append(evader)
                ino.last_spawn_time = current_time
    
    # РЎРїР°РІРЅ С€РІРёРґРєРёС… РІРѕСЂРѕРіС–РІ (Р»РёС€Рµ СЏРєС‰Рѕ РЅРµРјР°С” Р±РѕСЃР°)
    if not boss and hasattr(stats, 'wave_start_time'):
        time_in_wave = current_time - stats.wave_start_time
        # РџРµСЂС€Р° С…РІРёР»СЏ С€РІРёРґРєРёС… РІРѕСЂРѕРіС–РІ (С‡РµСЂРµР· 3 СЃРµРє)
        if time_in_wave > 3000 and getattr(stats, 'fast_enemies_spawned', 0) == 0:
            spawn_fast_enemies(screen, new_inos, stats)
            stats.fast_enemies_spawned = 1
        # Р”СЂСѓРіР° С…РІРёР»СЏ С€РІРёРґРєРёС… РІРѕСЂРѕРіС–РІ (С‡РµСЂРµР· 10 СЃРµРє)
        elif time_in_wave > 10000 and getattr(stats, 'fast_enemies_spawned', 0) == 1:
            spawn_fast_enemies(screen, new_inos, stats)
            stats.fast_enemies_spawned = 2
            
    for ev in new_inos:
        inos.add(ev)

    died = False
    is_invincible = getattr(stats, 'invincible_wave', -1) == getattr(stats, 'wave', 1)
    
    if not is_invincible:
        if pygame.sprite.spritecollideany(gun, inos):
            gun_kill(stats, screen, sc, gun, inos, bullets, bunkers, boss)
            died = True
            
        if not died:
            if inos_check(stats, screen, sc, gun, inos, bullets, bunkers, boss):
                died = True

    if died:
        stats.armies_defeated = 0
        return None

    if boss:
        # Р’СЃС‚Р°РЅРѕРІР»СЋС”РјРѕ РїРѕСЃРёР»Р°РЅРЅСЏ РЅР° РіСЂР°РІС†СЏ РґР»СЏ Р±РѕСЃР°
        if hasattr(boss, 'set_player'):
            boss.set_player(gun)
            
        # РћРЅРѕРІР»РµРЅРЅСЏ С‚Р° РјР°Р»СЋРІР°РЅРЅСЏ РєСѓР»СЊ Р±РѕСЃР°
        boss.update_bullets()

        # Р‘РѕСЃ СЃС‚СЂС–Р»СЏС” РєРѕР¶РЅС– 1.5 СЃРµРєСѓРЅРґРё
        now = pygame.time.get_ticks()
        if now - boss.last_shot_time > 1500:
            boss.shoot()
            boss.last_shot_time = now

        # РџРµСЂРµРІС–СЂРєР° РєРѕР»С–Р·С–Р№ Р· РіСЂР°РІС†РµРј
        if pygame.sprite.collide_rect(boss, gun):
            boss.bullets.empty()
            stats.armies_defeated = 0
            gun_kill(stats, screen, sc, gun, inos, bullets, bunkers, boss)
            return None
        else:
            # РџРµСЂРµРІС–СЂРєР° РєСѓР»СЊ Р±РѕСЃР° Р· РіСЂР°РІС†РµРј
            for bullet in boss.bullets:
                if pygame.sprite.collide_rect(bullet, gun):
                    if getattr(stats, 'current_armor', 0) > 0:
                        stats.current_armor -= 1
                        boss.bullets.remove(bullet)
                        continue
                    # РћС‡РёС‰Р°С”РјРѕ РєСѓР»С– С‚Р° СЃРєРёРґР°С”РјРѕ Р»С–С‡РёР»СЊРЅРёРє Р°СЂРјС–Р№
                    boss.bullets.empty()
                    stats.armies_defeated = 0
                    gun_kill(stats, screen, sc, gun, inos, bullets, bunkers, boss)
                    return None

    return boss

def create_army(screen, inos, bunkers=None, extra_rows=0, stats=None):
    if stats:
        stats.wave_start_time = pygame.time.get_ticks()
        stats.fast_enemies_spawned = 0
        
    if bunkers is not None:
        bunkers.empty()
        from bunker import Bunker
        # РЎС‚РІРѕСЂСЋС”РјРѕ 4 РїСЂРµРіСЂР°РґРё, СЂРѕР·РїРѕРґС–Р»СЏС”РјРѕ СЂС–РІРЅРѕРјС–СЂРЅРѕ
        gap = screen.get_rect().width // 5
        for i in range(4):
            bunker = Bunker(screen, gap + i * gap - 40, 350)
            bunkers.add(bunker)
    ino = Ino(screen)
    ino_width = ino.rect.width
    numbers_ino_x = int((screen.get_rect().width - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    numbers_ino_y = 3 + extra_rows

    for row_number in range(numbers_ino_y):
        image_type = row_number % 4 + 1
        for ino_number in range(numbers_ino_x):
            ino = Ino(screen, image_type=image_type)
            if stats:
                ino.apply_skin(stats.get_enemy_color())
            ino.x = ino_width + ino_width * ino_number
            ino.y = ino_height + ino_height * row_number
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + ino_height * row_number
            # Scale regular enemy health
            wave_val = getattr(stats, 'wave', 1) if stats else 1
            ino.health = int(ino.health * (1 + (wave_val - 1) * 0.3))
            inos.add(ino)
            
    if getattr(stats, 'wave', 1) >= 2 and random.random() < 0.7:
        from mmp8 import Mmp8
        mmp8 = Mmp8(screen)
        wave_val = getattr(stats, 'wave', 1) if stats else 1
        mmp8.health = int(mmp8.health * (1 + (wave_val - 1) * 0.3))
        inos.add(mmp8)

def spawn_fast_enemies(screen, inos_list, stats):
    from fast_enemy import FastEnemy
    import random
    wave = getattr(stats, 'wave', 1)
    
    if wave < 2:
        return
        
    count = 1 + (wave // 3)  # Р§РёРј РґР°Р»С–, С‚РёРј Р±С–Р»СЊС€Рµ РІРѕСЂРѕРіС–РІ
    for i in range(count):
        fe = FastEnemy(screen)
        fe.rect.x = random.randint(0, screen.get_rect().width - 30)
        fe.rect.y = -random.randint(0, 50)
        fe.x = float(fe.rect.x)
        fe.y = float(fe.rect.y)
        fe.health = int(fe.health * (1 + (wave - 1) * 0.3))
        inos_list.append(fe)

def check_high_score(stats, sc):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))
    def update_drops(stats, screen, gun, drops):

        drops.update()

        for drop in drops.copy():

            if drop.rect.top >= screen.get_rect().bottom:

                drops.remove(drop)

                

        collisions = pygame.sprite.spritecollide(gun, drops, True)

        for drop in collisions:

            if drop.type == 'armor':

                stats.current_armor = getattr(stats, 'current_armor', 0) + 1


def update_drops(stats, screen, gun, drops):
    drops.update()
    for drop in drops.copy():
        if drop.rect.top >= screen.get_rect().bottom:
            drops.remove(drop)
            
    collisions = pygame.sprite.spritecollide(gun, drops, True)
    for drop in collisions:
        if drop.type == 'armor':
            stats.current_armor = getattr(stats, 'current_armor', 0) + 1
        elif drop.type == 'double_bullet':
            stats.double_bullet_timer = pygame.time.get_ticks() + 10000
        else:
            mats = getattr(stats, 'materials', {'iron': 0, 'crystal': 0, 'core': 0})
            mats[drop.type] = mats.get(drop.type, 0) + 1
            stats.materials = mats
            stats.save_upgrades()
