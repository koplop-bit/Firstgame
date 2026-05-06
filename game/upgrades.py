import pygame

class UpgradesMenu:
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 30)
        
        self.damage_cost_base = 10
        self.size_cost_base = 10
        self.damage_2_cost_base = 500
        self.size_2_cost_base = 500
        self.money_mult_cost_base = 1000
        self.fire_rate_cost_base = 200
        self.bullet_speed_cost_base = 150
        self.player_speed_cost_base = 300
        
    def get_damage_cost(self):
        return self.damage_cost_base * (2 ** self.stats.damage_level)
        
    def get_size_cost(self):
        return self.size_cost_base * (2 ** self.stats.size_level)
        
    def get_damage_2_cost(self):
        return self.damage_2_cost_base * (2 ** getattr(self.stats, 'damage_level_2', 0))
        
    def get_size_2_cost(self):
        return self.size_2_cost_base * (2 ** getattr(self.stats, 'size_level_2', 0))
        
    def get_money_mult_cost(self):
        return self.money_mult_cost_base * (2 ** getattr(self.stats, 'money_mult_level', 0))
        
    def get_total_levels(self):
        return (self.stats.damage_level + self.stats.size_level + 
                getattr(self.stats, 'damage_level_2', 0) + 
                getattr(self.stats, 'size_level_2', 0) + 
                getattr(self.stats, 'money_mult_level', 0))
        
    def draw(self):
        self.screen.fill((20, 20, 50))
        
        # Заголовок
        title = self.font.render("Upgrades Menu (Press ESC to return)", True, (255, 255, 255))
        self.screen.blit(title, (50, 30))
        
        # Гроші
        money_text = self.font.render(f"Money: {self.stats.money} $", True, (255, 255, 0))
        self.screen.blit(money_text, (50, 80))
        
        total_levels = self.get_total_levels()
        level_text = self.small_font.render(f"Total Upgrades: {total_levels}", True, (200, 200, 200))
        self.screen.blit(level_text, (50, 120))
        
        y = 170
        
        # 1. Урон
        dmg_cost = self.get_damage_cost()
        dmg_text = self.small_font.render(f"[1] Upgrade Damage (+10%) | Level: {self.stats.damage_level} | Cost: {dmg_cost} $", True, (255, 255, 255))
        self.screen.blit(dmg_text, (50, y))
        y += 40
        
        # 2. Розмір куль
        size_cost = self.get_size_cost()
        size_text = self.small_font.render(f"[2] Upgrade Bullet Size | Level: {self.stats.size_level} | Cost: {size_cost} $", True, (255, 255, 255))
        self.screen.blit(size_text, (50, y))
        y += 50
        
        # 3. Урон 2
        if self.stats.damage_level >= 10:
            dmg2_cost = self.get_damage_2_cost()
            dmg2_text = self.small_font.render(f"[3] Damage Tier 2 (+25%) | Level: {getattr(self.stats, 'damage_level_2', 0)} | Cost: {dmg2_cost} $", True, (255, 150, 150))
            self.screen.blit(dmg2_text, (50, y))
        y += 40
        
        # 4. Розмір 2
        if self.stats.size_level >= 10:
            sz2_cost = self.get_size_2_cost()
            sz2_text = self.small_font.render(f"[4] Size Tier 2 (+20px) | Level: {getattr(self.stats, 'size_level_2', 0)} | Cost: {sz2_cost} $", True, (150, 255, 150))
            self.screen.blit(sz2_text, (50, y))
        y += 40
        
        # Q. Швидкість стрільби
        fr_cost = self.fire_rate_cost_base * (2 ** getattr(self.stats, 'fire_rate_level', 0))
        fr_text = self.small_font.render(f"[Q] Upgrade Fire Rate | Level: {getattr(self.stats, 'fire_rate_level', 0)} | Cost: {fr_cost} $", True, (255, 200, 200))
        self.screen.blit(fr_text, (50, y))
        y += 40
        
        # W. Швидкість кулі
        bs_cost = self.bullet_speed_cost_base * (2 ** getattr(self.stats, 'bullet_speed_level', 0))
        bs_text = self.small_font.render(f"[W] Upgrade Bullet Speed | Level: {getattr(self.stats, 'bullet_speed_level', 0)} | Cost: {bs_cost} $", True, (200, 255, 200))
        self.screen.blit(bs_text, (50, y))
        y += 40
        
        # E. Швидкість гравця
        ps_cost = self.player_speed_cost_base * (2 ** getattr(self.stats, 'player_speed_level', 0))
        ps_text = self.small_font.render(f"[E] Upgrade Player Speed | Level: {getattr(self.stats, 'player_speed_level', 0)} | Cost: {ps_cost} $", True, (200, 200, 255))
        self.screen.blit(ps_text, (50, y))
        y += 40
        
        # 5. Гроші
        if self.stats.damage_level >= 10 or self.stats.size_level >= 10:
            m_cost = self.get_money_mult_cost()
            m_text = self.small_font.render(f"[5] Money Multiplier (+0.5x) | Level: {getattr(self.stats, 'money_mult_level', 0)} | Cost: {m_cost} $", True, (255, 255, 100))
            self.screen.blit(m_text, (50, y))
        y += 60
        
        # Унікальні прокачки
        if total_levels >= 15:
            has_extra = getattr(self.stats, 'has_extra_bullet', False)
            if not has_extra:
                t = self.small_font.render(f"[6] Buy Extra Bullet (Passive) | Cost: 5000 $", True, (100, 255, 255))
            else:
                t = self.small_font.render(f"Extra Bullet (Passive): UNLOCKED", True, (100, 255, 255))
            self.screen.blit(t, (50, y))
        y += 40
        
        if total_levels >= 30:
            has_super = getattr(self.stats, 'has_super_mode', False)
            if not has_super:
                t = self.small_font.render(f"[7] Buy Super Mode (Press Q) | Cost: 15000 $", True, (255, 100, 255))
            else:
                t = self.small_font.render(f"Super Mode (Press Q): UNLOCKED", True, (255, 100, 255))
            self.screen.blit(t, (50, y))
        y += 40
        
        if total_levels >= 45:
            has_money = getattr(self.stats, 'has_money_mode', False)
            if not has_money:
                t = self.small_font.render(f"[8] Buy Money Mode (Press E) | Cost: 30000 $", True, (255, 200, 100))
            else:
                t = self.small_font.render(f"Money Mode (Press E): UNLOCKED", True, (255, 200, 100))
            self.screen.blit(t, (50, y))
            y += 40
            
        # Extra Life
        t = self.small_font.render(f"[9] Buy Extra Life (+1 Heart) | Owned: {getattr(self.stats, 'extra_lives', 0)} | Cost: 1000 $", True, (255, 50, 50))
        self.screen.blit(t, (50, y))
        y += 40
            
        # Armor
        armor_text = self.small_font.render(f"[0] Buy Armor (+1 Hit) | Owned: {getattr(self.stats, 'armor_level', 0)} | Cost: 2000 $", True, (100, 255, 100))
        self.screen.blit(armor_text, (50, y))
        y += 40
            
        pygame.display.flip()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                cost = self.get_damage_cost()
                if self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.damage_level += 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_2:
                cost = self.get_size_cost()
                if self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.size_level += 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_3 and self.stats.damage_level >= 10:
                cost = self.get_damage_2_cost()
                if self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.damage_level_2 = getattr(self.stats, 'damage_level_2', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_4 and self.stats.size_level >= 10:
                cost = self.get_size_2_cost()
                if self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.size_level_2 = getattr(self.stats, 'size_level_2', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_5 and (self.stats.damage_level >= 10 or self.stats.size_level >= 10):
                cost = self.get_money_mult_cost()
                if self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.money_mult_level = getattr(self.stats, 'money_mult_level', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_q:
                cost = self.fire_rate_cost_base * (2 ** getattr(self.stats, 'fire_rate_level', 0))
                if getattr(self.stats, 'fire_rate_level', 0) < 10 and self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.fire_rate_level = getattr(self.stats, 'fire_rate_level', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_w:
                cost = self.bullet_speed_cost_base * (2 ** getattr(self.stats, 'bullet_speed_level', 0))
                if getattr(self.stats, 'bullet_speed_level', 0) < 15 and self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.bullet_speed_level = getattr(self.stats, 'bullet_speed_level', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_e:
                cost = self.player_speed_cost_base * (2 ** getattr(self.stats, 'player_speed_level', 0))
                if getattr(self.stats, 'player_speed_level', 0) < 10 and self.stats.money >= cost:
                    self.stats.money -= cost
                    self.stats.player_speed_level = getattr(self.stats, 'player_speed_level', 0) + 1
                    self.stats.save_upgrades()
            elif event.key == pygame.K_6 and self.get_total_levels() >= 15 and not getattr(self.stats, 'has_extra_bullet', False):
                if self.stats.money >= 5000:
                    self.stats.money -= 5000
                    self.stats.has_extra_bullet = True
                    self.stats.save_upgrades()
            elif event.key == pygame.K_7 and self.get_total_levels() >= 30 and not getattr(self.stats, 'has_super_mode', False):
                if self.stats.money >= 15000:
                    self.stats.money -= 15000
                    self.stats.has_super_mode = True
                    self.stats.save_upgrades()
            elif event.key == pygame.K_8 and self.get_total_levels() >= 45 and not getattr(self.stats, 'has_money_mode', False):
                if self.stats.money >= 30000:
                    self.stats.money -= 30000
                    self.stats.has_money_mode = True
                    self.stats.save_upgrades()
            elif event.key == pygame.K_9:
                if self.stats.money >= 1000:
                    self.stats.money -= 1000
                    self.stats.extra_lives = getattr(self.stats, 'extra_lives', 0) + 1
                    self.stats.guns_left += 1  # Add immediately to current run
                    self.stats.save_upgrades()
            elif event.key == pygame.K_0:
                if self.stats.money >= 2000:
                    self.stats.money -= 2000
                    self.stats.armor_level = getattr(self.stats, 'armor_level', 0) + 1
                    self.stats.current_armor = self.stats.armor_level
                    self.stats.save_upgrades()
