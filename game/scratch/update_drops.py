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
