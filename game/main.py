import pygame
import controls
from weapon import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
from boss import Boss
from menu import Menu
from analytics import Analytics
from upgrades import UpgradesMenu
from map_menu import MapMenu
from crafting_menu import CraftingMenu

def run():
    pygame.init()
    try:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    except:
        screen = pygame.display.set_mode((800, 700))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Space Invaders")
    
    # Завантаження фону
    import os
    import glob
    bg_images = [None, None]
    
    # 0: Default (space_bd)
    try:
        if os.path.exists('images/space_bd.png'):
            bg_default = pygame.image.load('images/space_bd.png')
        elif os.path.exists('../images/space_bd.png'):
            bg_default = pygame.image.load('../images/space_bd.png')
        else:
            bg_default = None
            
        if bg_default:
            bg_images[0] = pygame.transform.scale(bg_default, (screen_rect.width, screen_rect.height)).convert()
    except:
        bg_images[0] = None
        
    # 1: Custom (fon.png)
    try:
        if os.path.exists('images/fon.png'):
            bg_custom = pygame.image.load('images/fon.png')
        elif os.path.exists('../images/fon.png'):
            bg_custom = pygame.image.load('../images/fon.png')
        else:
            bg_custom = None
            
        if bg_custom:
            bg_images[1] = pygame.transform.scale(bg_custom, (screen_rect.width, screen_rect.height)).convert()
        else:
            bg_images[1] = bg_images[0]
    except Exception as e:
        print("Bg error:", e)
        bg_images[1] = bg_images[0]
        
    bg_color = (0, 0, 0)
    
    # Завантаження музики
    import glob
    music_files = glob.glob('Music*.*') + glob.glob('images/Music*.*')
    valid_exts = ['.mp3', '.ogg', '.wav']
    playlist = [f for f in music_files if any(f.lower().endswith(ext) for ext in valid_exts)]
    import random
    current_track = 0
    if playlist:
        random.shuffle(playlist)
        try:
            pygame.mixer.music.load(playlist[current_track])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print("Music load error:", e)

    # Створюємо меню та аналітику
    menu = Menu(screen)
    analytics = Analytics(screen)
    game_started = False
    show_analytics = False
    show_upgrades = False

    from skins import SkinsMenu
    # Ініціалізуємо об'єкти гри
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    bunkers = Group()
    drops = Group()
    stats = Stats()
    sc = Scores(screen, stats)
    upgrades_menu = UpgradesMenu(screen, stats)
    skins_menu = SkinsMenu(screen, stats)
    map_menu = MapMenu(screen, stats)
    crafting_menu = CraftingMenu(screen, stats)
    boss = None
    
    import random
    stars = []
    for _ in range(100):
        x = random.randint(0, screen_rect.width)
        y = random.randint(0, screen_rect.height)
        speed = random.randint(1, 4)
        brightness = random.randint(100, 255)
        size = random.randint(1, 3)
        stars.append({'pos': [x, y], 'speed': speed, 'brightness': brightness, 'size': size})
    
    gun.apply_skin(stats.get_gun_color())

    while True:
        if playlist and not pygame.mixer.music.get_busy():
            current_track = (current_track + 1) % len(playlist)
            if current_track == 0:
                random.shuffle(playlist)
            try:
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
            except:
                pass

        if not game_started and not show_analytics and not show_upgrades and not getattr(skins_menu, 'active', False) and not getattr(map_menu, 'active', False) and not getattr(crafting_menu, 'active', False):
            # Показуємо меню
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_RETURN:  # Натиснуто Enter
                        game_started = True
                        gun = Gun(screen)
                        gun.apply_skin(stats.get_gun_color())
                        bullets = Group()
                        inos = Group()
                        bunkers = Group()
                        drops = Group()
                        controls.create_army(screen, inos, bunkers, 0, stats)
                        stats.reset_stats()
                        stats.run_game = True
                        boss = None
                    elif event.key == pygame.K_a:  # Натиснуто A
                        show_analytics = True
                    elif event.key == pygame.K_u:  # Натиснуто U
                        show_upgrades = True
                    elif event.key == pygame.K_s:
                        skins_menu.active = True
                    elif event.key == pygame.K_m:
                        map_menu.selected_level = getattr(stats, 'max_wave_unlocked', 1)
                        map_menu.active = True
                    elif event.key == pygame.K_c:
                        crafting_menu.active = True
                    elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        pygame.display.toggle_fullscreen()
            
            # Оновлюємо та малюємо меню
            menu.update_stars()
            menu.draw()
            
        elif show_analytics:
            # Показуємо аналітику
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Натиснуто ESC
                        show_analytics = False
                        analytics = Analytics(screen)  # Оновлюємо аналітику
            
            # Малюємо аналітику
            analytics.draw()
            
        elif getattr(skins_menu, 'active', False):
            # Показуємо скіни
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    skins_menu.active = False
                    gun.apply_skin(stats.get_gun_color())
                else:
                    skins_menu.handle_event(event)
            skins_menu.draw()
            
        elif show_upgrades:
            # Показуємо покращення
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    show_upgrades = False
                else:
                    upgrades_menu.handle_event(event)
            upgrades_menu.draw()
            
        elif getattr(map_menu, 'active', False):
            # Показуємо карту
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                else:
                    def start_game_from_map():
                        nonlocal game_started, gun, bullets, inos, bunkers, boss
                        game_started = True
                        gun = Gun(screen)
                        gun.apply_skin(stats.get_gun_color())
                        bullets = Group()
                        inos = Group()
                        bunkers = Group()
                        drops = Group()
                        controls.create_army(screen, inos, bunkers, 0, stats)
                        
                        # Preserve the wave we selected in the map menu
                        selected_wave = stats.wave
                        stats.reset_stats()
                        stats.wave = selected_wave
                        stats.run_game = True
                        boss = None
                        
                    map_menu.handle_event(event, start_game_from_map)
            if getattr(map_menu, 'active', False):
                map_menu.draw()
            pygame.display.flip()
            
        elif getattr(crafting_menu, 'active', False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                else:
                    crafting_menu.handle_event(event)
            if getattr(crafting_menu, 'active', False):
                crafting_menu.draw()
            pygame.display.flip()
            
        else:
            # Гра почалась
            # Обробка подій (стрільба та рух)
            controls.events(screen, gun, bullets, stats, boss, inos)

            if stats.run_game:
                # Оновлення гравця
                gun.update(stats)
                
                # Оновлення куль і дропу
                bullets.update()
                if 'drops' in locals():
                    drops.update()
                
                # Оновлення боса через update_bullets
                if boss is None:
                    new_boss = controls.update_bullets(screen, stats, sc, inos, bullets, boss, bunkers, drops if 'drops' in locals() else None)
                    if new_boss is not None:
                        boss = new_boss
                else:
                    boss = controls.update_bullets(screen, stats, sc, inos, bullets, boss, bunkers, drops if 'drops' in locals() else None)
                
                # Оновлення боса та ворогів
                boss = controls.update_inos(stats, screen, sc, gun, inos, bullets, boss)
                
                if 'drops' in locals():
                    controls.update_drops(stats, screen, gun, drops)
                
                # Малюємо фон
                bg_index = getattr(stats, 'bg_skin_index', 0) % 3
                if bg_index == 2:
                    # Режим анімованих зірок
                    screen.fill(bg_color)
                    for star in stars:
                        star['pos'][1] += star['speed']
                        if star['pos'][1] > screen_rect.height:
                            star['pos'][1] = 0
                            star['pos'][0] = random.randint(0, screen_rect.width)
                        pygame.draw.circle(
                            screen,
                            (star['brightness'], star['brightness'], star['brightness']),
                            star['pos'],
                            star['size']
                        )
                else:
                    current_bg = bg_images[bg_index]
                    if current_bg:
                        screen.blit(current_bg, (0, 0))
                    else:
                        screen.fill(bg_color)
                
                # Оновлення екрану
                controls.update(bg_color, screen, stats, sc, gun, inos, bullets, boss, bunkers)
            else:
                # Гра закінчена - зберігаємо очки за життя і повертаємось до меню
                stats.update_life_score()
                game_started = False
                # Оновлюємо аналітику для відображення нових даних
                analytics = Analytics(screen)

run()
