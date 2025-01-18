import pygame
import os
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WereWolf")
background = pygame.image.load("./assets/background.jpg")
# 設定開始按鈕
game_start = pygame.image.load("./assets/GameStart.png")
game_start_rect = game_start.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5 ))

# 設定返回按鈕
return_button = pygame.transform.scale(pygame.image.load("./assets/returnbutton.png"), (100, 100))
return_button_rect = game_start.get_rect(center=(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 60))

pygame.mouse.set_visible(1)
clock = pygame.time.Clock()
FPS = 60

ROLES_CONFIG = {"9人速推局" : ["狼人", "狼人", "狼人", "預言家", "女巫", "獵人", "平民", "平民", "平民"],
                "10人速推局" : ["狼人", "狼人", "狼人" ,"預言家" ,"女巫" , "獵人" , "平民", "平民" , "平民", "平民"],
                "12人標準場" : ["狼人", "狼人", "狼人", "狼人", "預言家" ,"女巫" , "獵人", "白痴", "平民", "平民", "平民", "平民"]}

GAMES_DESCRIPTION = {"9人速推局" : "3狼人、預言家、女巫、獵人、3平民",
                "10人速推局" : "3狼人、預言家、女巫、獵人、4平民",
                "12人標準場" : "4狼人、預言家、女巫、獵人、守衛、3平民"}


def show_return_button():
    screen.blit(return_button, return_button_rect)

def show_start_page():
    screen.blit(background, (0,0))
    screen.blit(game_start, game_start_rect)
    
def show_game_menu_page():
    # menu_buttons = []
    menu_buttons_rect = []
    screen.blit(background, (0,0))
    # 設定遊戲模式的選項及按鈕
    rect_start = (SCREEN_WIDTH // 2, 120)
    for role_config in ROLES_CONFIG.keys():
        menu_button = pygame.transform.scale(pygame.image.load("./assets/{}.png".format(role_config)), (400, 150))
        menu_button_rect = menu_button.get_rect(center=(rect_start))
        screen.blit(menu_button, menu_button_rect)
        # menu_buttons.append(menu_button)
        menu_buttons_rect.append(menu_button_rect)
        rect_start = (rect_start[0], rect_start[1] + 160)
    show_return_button()
    
    return menu_buttons_rect

class Game:
    def __init__(self, game_type, role_path):
        self.game_type = game_type
        self.game_roles = []
        self.current_role = 0
        
         # 設定卡牌背面
        self.card_back = pygame.transform.scale(pygame.image.load("./assets/卡牌背面.jpg"), (300, 450)) 
        self.card_back_rect = self.card_back.get_rect(center=(SCREEN_WIDTH // 2, 300))
        
        # next card button
        self.next_card_button = pygame.transform.scale(pygame.image.load("./assets/next.png"), (150, 150)) 
        self.next_card_button_rect = self.next_card_button.get_rect(center=(SCREEN_WIDTH - 85, SCREEN_HEIGHT // 2))
        
        if game_type not in ROLES_CONFIG:
            print(f"[Error] Game type : {game_type} doesn't exist !")
        else:
            self.add_roles(role_path)

    def shuffle_roles_card(self, role_list):
        random.shuffle(role_list)
        return role_list
        
    def add_roles(self, role_path):
        buf = []
        for role in ROLES_CONFIG[self.game_type]:
            buf.append(role_path[role])
        buf = self.shuffle_roles_card(buf)
        self.game_roles = buf
        # for rp in buf:
        #     self.game_roles.append(pygame.transform.scale(pygame.image.load(rp), (300, 450)))
    def show_next_card_button(self):
        screen.blit(self.next_card_button, self.next_card_button_rect)
        
    def show_next_card_page(self):
        if self.current_role >= len(self.game_roles):
            show_start_page()
            return

        screen.blit(background, (0,0))
        screen.blit(pygame.transform.scale(pygame.image.load(self.game_roles[self.current_role]), (300, 450)), (250, 75))
        show_return_button()
        self.current_role += 1
        
        if self.current_role < len(self.game_roles):
            self.show_next_card_button()

    def show_card_back_page(self):
        screen.blit(background, (0,0))
        screen.blit(self.card_back, self.card_back_rect)
        show_return_button()

class RoleLoader:
    def __init__(self, dir_path):
        self.role_path = {}
        self.load_roles_img(dir_path)

    def load_roles_img(self, dir_path):
        file_list = os.listdir(dir_path)
        for fn in file_list:
            if os.path.basename(fn)[0] == '.':
                continue
            self.role_path[os.path.basename(fn).split('.')[0]] = os.path.join(dir_path, fn)
            # print(f"Load role Success: {os.path.join(dir_path, fn)}")
        

def main():
    current_page = "start"
    role_loader = RoleLoader("./assets/role")
    game = None
    menu_buttons_rect = []
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_page == "start" and game_start_rect.collidepoint(event.pos):
                    current_page = "menu"
                    menu_buttons_rect = show_game_menu_page()
                elif current_page == "menu":
                    for i, rect in enumerate(menu_buttons_rect):
                        if rect.collidepoint(event.pos):
                            game_type = list(ROLES_CONFIG.keys())[i]
                            game = Game(game_type, role_loader.role_path)
                            current_page = "card_back"
                            game.show_card_back_page()
                            break
                    if return_button_rect.collidepoint(event.pos):
                        current_page = "start"
                        show_start_page()
                elif current_page == "card_back" and game.card_back_rect.collidepoint(event.pos):
                    current_page = "card_page"
                    game.show_next_card_page()
                elif current_page == "card_page" and return_button_rect.collidepoint(event.pos):
                    current_page = "start"
                    show_start_page()
                elif current_page == "card_page" and game.next_card_button_rect.collidepoint(event.pos):
                    current_page = "card_back"
                    game.show_card_back_page()

        if current_page == "start":
            show_start_page()

        pygame.display.flip()
        clock.tick(FPS)

    # 結束 Pygame
    pygame.quit()
    sys.exit()

# 執行主程式
if __name__ == "__main__":
    main()