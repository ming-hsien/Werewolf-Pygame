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

def shuffle_roles_card(role_list):
    random.shuffle(role_list)
    return role_list

class Games:
    def __init__(self, game_type, role_path):
        self.game_type = game_type
        self.game_roles = []
        
        if game_type not in ROLES_CONFIG:
            print(f"[Error] Game type : {game_type} doesn't exist !")
        else:
            self.add_roles(role_path)
        
    def add_roles(self, role_path):
        buf = []
        for role in ROLES_CONFIG[self.game_type]:
            buf.append(role_path[role])
        buf = shuffle_roles_card(buf)
        for rp in buf:
            self.game_roles.append(pygame.image.load(rp))          

    def show_roles_page(self):
        screen.blit(background, (0,0))
        print(self.game_type, self.game_roles)

class Roles:
    def __init__(self, dir_path):
        self.role_path = {}
        self.load_roles_img(dir_path)

    def load_roles_img(self, dir_path):
        file_list = os.listdir(dir_path)
        for fn in file_list:
            if os.path.basename(fn)[0] == '.':
                continue
            self.role_path[os.path.basename(fn).split('.')[0]] = os.path.join(dir_path, fn)
            print(f"Load role Success: {os.path.join(dir_path, fn)}")
        

def main():
    current_page = "start" # start -> game_menu -> role_page
    roles_obj = Roles("./assets/role")
    games_obj = ""
    running = True
    menu_buttons_rect = []
    
    while running:
        for event in pygame.event.get():
            # 設定點擊關閉頁面
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            # 設定點擊遊戲開始的按鈕後，頁面狀態更新
            elif event.type == pygame.MOUSEBUTTONDOWN and game_start_rect.collidepoint(event.pos):
                current_page = "game_menu"
            
            # 設定點擊返回按鈕，頁面狀態更新
            elif event.type == pygame.MOUSEBUTTONDOWN and return_button_rect.collidepoint(event.pos):
                if current_page == "game_menu":
                    current_page = "start"
                elif current_page == "role_page":
                    current_page = "game_menu"
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and menu_buttons_rect[0].collidepoint(event.pos):
                games_obj = Games(list(ROLES_CONFIG.keys())[0], roles_obj.role_path)
                current_page = "role_page"
            elif event.type == pygame.MOUSEBUTTONDOWN and menu_buttons_rect[1].collidepoint(event.pos):
                games_obj = Games(list(ROLES_CONFIG.keys())[1], roles_obj.role_path)
                current_page = "role_page"
            elif event.type == pygame.MOUSEBUTTONDOWN and menu_buttons_rect[2].collidepoint(event.pos):
                games_obj = Games(list(ROLES_CONFIG.keys())[2], roles_obj.role_path)
                current_page = "role_page"
            
                
        if current_page == "start":
            show_start_page()
        
        elif current_page == "game_menu":
            menu_buttons_rect = show_game_menu_page()
        
        elif current_page == "role_page":
            games_obj.show_roles_page()

        pygame.display.flip()
        clock.tick(FPS)

    # 結束 Pygame
    pygame.quit()
    sys.exit()

# 執行主程式
if __name__ == "__main__":
    main()