import pygame

class SkinsMenu:
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 40)
        self.active = False
        
        self.color_names = ["Default", "Red", "Green", "Blue", "Yellow"]
        self.colors = [(255, 255, 255), (255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        self.bg_names = ["Default (Space)", "Custom (fon.png)", "Animated Stars"]
        
    def draw(self):
        self.screen.fill((30, 20, 50))
        
        title = self.font.render("Skins Menu (Press ESC to return)", True, (255, 255, 255))
        self.screen.blit(title, (50, 50))
        
        gun_color_name = self.color_names[self.stats.gun_skin_index % len(self.color_names)]
        gun_color_val = self.colors[self.stats.gun_skin_index % len(self.colors)]
        
        enemy_color_name = self.color_names[self.stats.enemy_skin_index % len(self.color_names)]
        enemy_color_val = self.colors[self.stats.enemy_skin_index % len(self.colors)]
        
        # Gun skin option
        t1 = self.small_font.render(f"[1] Change Player Skin: {gun_color_name}", True, gun_color_val)
        self.screen.blit(t1, (50, 200))
        
        # Enemy skin option
        t2 = self.small_font.render(f"[2] Change Enemy Skin: {enemy_color_name}", True, enemy_color_val)
        self.screen.blit(t2, (50, 280))
        
        # BG skin option
        bg_name = self.bg_names[getattr(self.stats, 'bg_skin_index', 0) % len(self.bg_names)]
        t3 = self.small_font.render(f"[3] Change Background: {bg_name}", True, (200, 200, 200))
        self.screen.blit(t3, (50, 360))
        
        pygame.display.flip()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.stats.gun_skin_index = (self.stats.gun_skin_index + 1) % len(self.color_names)
                self.stats.save_upgrades()
            elif event.key == pygame.K_2:
                self.stats.enemy_skin_index = (self.stats.enemy_skin_index + 1) % len(self.color_names)
                self.stats.save_upgrades()
            elif event.key == pygame.K_3:
                self.stats.bg_skin_index = (getattr(self.stats, 'bg_skin_index', 0) + 1) % len(self.bg_names)
                self.stats.save_upgrades()
