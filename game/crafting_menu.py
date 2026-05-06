import pygame

class CraftingMenu:
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.active = False
        
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 30)
        
        self.recipes = {
            'wave_clear': {'name': 'Instant Wave Clear (Z)', 'iron': 10, 'crystal': 5, 'core': 0},
            'invincibility': {'name': 'Invincibility for Wave (X)', 'iron': 0, 'crystal': 5, 'core': 2},
            'boss_half_hp': {'name': 'Boss 50% HP Damage (C)', 'iron': 10, 'crystal': 10, 'core': 3}
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_1:
                self.craft('wave_clear')
            elif event.key == pygame.K_2:
                self.craft('invincibility')
            elif event.key == pygame.K_3:
                self.craft('boss_half_hp')

    def craft(self, item_id):
        recipe = self.recipes[item_id]
        mats = getattr(self.stats, 'materials', {'iron': 0, 'crystal': 0, 'core': 0})
        
        if mats.get('iron', 0) >= recipe['iron'] and \
           mats.get('crystal', 0) >= recipe['crystal'] and \
           mats.get('core', 0) >= recipe['core']:
            
            mats['iron'] -= recipe['iron']
            mats['crystal'] -= recipe['crystal']
            mats['core'] -= recipe['core']
            
            self.stats.materials = mats
            actives = getattr(self.stats, 'actives', {})
            actives[item_id] = actives.get(item_id, 0) + 1
            self.stats.actives = actives
            self.stats.save_upgrades()

    def draw(self):
        self.screen.fill((30, 20, 40))
        
        title = self.font.render("Crafting Menu (ESC to exit)", True, (255, 255, 255))
        self.screen.blit(title, (50, 20))
        
        mats = getattr(self.stats, 'materials', {'iron': 0, 'crystal': 0, 'core': 0})
        actives = getattr(self.stats, 'actives', {})
        
        inventory_text = self.small_font.render(f"Inventory: {mats.get('iron', 0)} Iron | {mats.get('crystal', 0)} Crystal | {mats.get('core', 0)} Core", True, (200, 255, 200))
        self.screen.blit(inventory_text, (50, 80))
        
        y = 150
        idx = 1
        for key, recipe in self.recipes.items():
            cost_str = []
            if recipe['iron'] > 0: cost_str.append(f"{recipe['iron']} Iron")
            if recipe['crystal'] > 0: cost_str.append(f"{recipe['crystal']} Crystal")
            if recipe['core'] > 0: cost_str.append(f"{recipe['core']} Core")
            cost_text = " + ".join(cost_str)
            
            owned = actives.get(key, 0)
            
            text = self.small_font.render(f"[{idx}] Craft {recipe['name']} | Cost: {cost_text} | Owned: {owned}", True, (255, 255, 255))
            self.screen.blit(text, (50, y))
            y += 60
            idx += 1
