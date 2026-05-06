import pygame

class MapMenu:
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        
        self.active = False
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)
        
        self.selected_level = getattr(self.stats, 'max_wave_unlocked', 1)
        self.max_levels = 20
        
        # Calculate level positions (zig-zag pattern)
        self.level_positions = []
        start_x, start_y = 100, self.screen_rect.bottom - 100
        x_step = (self.screen_rect.width - 200) / 4
        y_step = (self.screen_rect.height - 200) / 5
        
        for i in range(self.max_levels):
            row = i // 5
            col = i % 5
            if row % 2 != 0:
                col = 4 - col # Reverse direction for zig-zag
            
            x = start_x + col * x_step
            y = start_y - row * y_step
            self.level_positions.append((int(x), int(y)))

    def handle_event(self, event, start_game_callback):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_LEFT:
                if self.selected_level > 1:
                    self.selected_level -= 1
            elif event.key == pygame.K_RIGHT:
                if self.selected_level < getattr(self.stats, 'max_wave_unlocked', 1) and self.selected_level < self.max_levels:
                    self.selected_level += 1
            elif event.key == pygame.K_RETURN:
                self.stats.wave = self.selected_level
                self.active = False
                start_game_callback()

    def draw(self):
        self.screen.fill((20, 20, 50))
        
        title = self.font.render("Adventure Map", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_rect.centerx - title.get_width() // 2, 20))
        
        instructions = self.small_font.render("Use LEFT/RIGHT to select level. Press ENTER to start. ESC to back.", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen_rect.centerx - instructions.get_width() // 2, 60))
        
        # Draw lines between nodes
        for i in range(self.max_levels - 1):
            color = (100, 255, 100) if i + 1 < getattr(self.stats, 'max_wave_unlocked', 1) else (100, 100, 100)
            pygame.draw.line(self.screen, color, self.level_positions[i], self.level_positions[i+1], 4)
            
        # Draw nodes
        for i in range(self.max_levels):
            pos = self.level_positions[i]
            level_num = i + 1
            is_unlocked = level_num <= getattr(self.stats, 'max_wave_unlocked', 1)
            is_selected = level_num == self.selected_level
            
            color = (50, 50, 50) # Locked
            if is_unlocked:
                color = (0, 200, 0) # Unlocked
            if is_selected:
                color = (255, 255, 0) # Selected
                
            radius = 20 if is_selected else 15
            pygame.draw.circle(self.screen, color, pos, radius)
            pygame.draw.circle(self.screen, (255, 255, 255), pos, radius, 2)
            
            num_text = self.small_font.render(str(level_num), True, (255, 255, 255))
            self.screen.blit(num_text, (pos[0] - num_text.get_width() // 2, pos[1] - num_text.get_height() // 2))
