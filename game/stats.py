class Stats:
    def __init__(self):
        """Ініціалізація статистики гри"""
        self.run_game = True
        self.life_scores = []  # Список для зберігання очків за кожне життя
        self.current_life_score = 0  # Очки за поточне життя

        # Завантаження найвищого результату з файлу
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.readline())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

        # Завантаження статистики очок за життя
        try:
            with open('life_scores.txt', 'r') as f:
                self.life_scores = [int(line.strip()) for line in f.readlines()]
                if len(self.life_scores) != 3:
                    self.life_scores = [0, 0, 0]
        except (FileNotFoundError, ValueError):
            self.life_scores = [0, 0, 0]

        self.current_boss_type = None  # Додаємо відслідковування типу поточного боса
        
        # Завантаження грошей та прокачки
        self.money = 0
        self.damage_level = 0
        self.size_level = 0
        
        # Нові прокачки
        self.damage_level_2 = 0
        self.size_level_2 = 0
        self.money_mult_level = 0
        self.fire_rate_level = 0
        self.bullet_speed_level = 0
        self.player_speed_level = 0
        self.max_wave_unlocked = 1
        
        self.has_extra_bullet = False
        self.has_super_mode = False
        self.has_money_mode = False
        
        self.materials = {'iron': 0, 'crystal': 0, 'core': 0}
        self.actives = {'wave_clear': 0, 'invincibility': 0, 'boss_half_hp': 0}
        self.invincible_wave = -1
        
        # Активні режими
        self.super_mode_active = False
        self.super_mode_end_time = 0
        self.super_mode_cooldown = 0
        
        self.money_mode_active = False
        self.money_mode_end_time = 0
        self.money_mode_cooldown = 0
        
        self.gun_skin_index = 0
        self.enemy_skin_index = 0
        self.bg_skin_index = 0
        self.extra_lives = 0
        self.armor_level = 0
        self.current_armor = 0

        self.load_upgrades()
        self.reset_stats()

    def load_upgrades(self):
        try:
            import json
            with open('upgrades.json', 'r') as f:
                data = json.load(f)
                self.money = data.get('money', 0)
                self.damage_level = data.get('damage_level', 0)
                self.size_level = data.get('size_level', 0)
                
                self.damage_level_2 = data.get('damage_level_2', 0)
                self.size_level_2 = data.get('size_level_2', 0)
                self.money_mult_level = data.get('money_mult_level', 0)
                self.fire_rate_level = data.get('fire_rate_level', 0)
                self.bullet_speed_level = data.get('bullet_speed_level', 0)
                self.player_speed_level = data.get('player_speed_level', 0)
                self.max_wave_unlocked = data.get('max_wave_unlocked', 1)
                self.has_extra_bullet = data.get('has_extra_bullet', False)
                self.has_super_mode = data.get('has_super_mode', False)
                self.has_money_mode = data.get('has_money_mode', False)
                
                self.materials = data.get('materials', {'iron': 0, 'crystal': 0, 'core': 0})
                self.actives = data.get('actives', {'wave_clear': 0, 'invincibility': 0, 'boss_half_hp': 0})
                self.gun_skin_index = data.get('gun_skin_index', 0)
                self.enemy_skin_index = data.get('enemy_skin_index', 0)
                self.bg_skin_index = data.get('bg_skin_index', 0)
                self.extra_lives = data.get('extra_lives', 0)
                self.armor_level = data.get('armor_level', 0)
        except:
            pass

    def save_upgrades(self):
        import json
        with open('upgrades.json', 'w') as f:
            json.dump({
                'money': self.money,
                'damage_level': self.damage_level,
                'size_level': self.size_level,
                'damage_level_2': self.damage_level_2,
                'size_level_2': self.size_level_2,
                'money_mult_level': self.money_mult_level,
                'fire_rate_level': self.fire_rate_level,
                'bullet_speed_level': self.bullet_speed_level,
                'player_speed_level': self.player_speed_level,
                'max_wave_unlocked': getattr(self, 'max_wave_unlocked', 1),
                'has_extra_bullet': self.has_extra_bullet,
                'has_super_mode': self.has_super_mode,
                'has_money_mode': self.has_money_mode,
                'materials': getattr(self, 'materials', {'iron': 0, 'crystal': 0, 'core': 0}),
                'actives': getattr(self, 'actives', {'wave_clear': 0, 'invincibility': 0, 'boss_half_hp': 0}),
                'gun_skin_index': self.gun_skin_index,
                'enemy_skin_index': self.enemy_skin_index,
                'bg_skin_index': self.bg_skin_index,
                'extra_lives': self.extra_lives,
                'armor_level': self.armor_level
            }, f, indent=4)
            
    def get_gun_color(self):
        colors = [(255, 255, 255), (255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        return colors[self.gun_skin_index % len(colors)]
        
    def get_enemy_color(self):
        colors = [(255, 255, 255), (255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        return colors[self.enemy_skin_index % len(colors)]
            
    def get_money_multiplier(self):
        import pygame
        mult = 1.0 + (0.5 * self.money_mult_level)
        if self.money_mode_active:
            if pygame.time.get_ticks() < self.money_mode_end_time:
                mult *= 3.0  # мультиплеєр на час дії
            else:
                self.money_mode_active = False
        return mult

    def reset_stats(self):
        """Скидає статистику, яка змінюється протягом гри"""
        self.guns_left = 2 + self.extra_lives  # Починаємо з життів (2 запасних + додаткові)
        self.score = 0
        self.armies_defeated = 0
        self.current_life_score = 0  # Очки для поточного життя
        self.current_boss_type = None
        self.super_mode_active = False
        self.money_mode_active = False
        self.wave = 1
        self.current_armor = self.armor_level

    def update_life_score(self):
        """Оновлює очки для поточного життя"""
        total_lives = 3 + self.extra_lives
        while len(self.life_scores) < total_lives:
            self.life_scores.append(0)
            
        life_index = (total_lives - 1) - self.guns_left
        if life_index < 0: life_index = 0
        if life_index >= len(self.life_scores): life_index = len(self.life_scores) - 1
            
        self.life_scores[life_index] = max(self.life_scores[life_index], self.current_life_score)
        
        # Зберігаємо статистику в файл
        with open('life_scores.txt', 'w') as f:
            for score in self.life_scores:
                f.write(f"{score}\n")

    def add_points(self, points):
        """Додає очки до загального рахунку та поточного життя"""
        self.score += points
        self.current_life_score += points
