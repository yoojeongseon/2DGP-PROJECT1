# (파일: collisions.py)

import pygame


def handle_player_collisions(player1, player2):
    """
    두 플레이어 간의 타격 판정을 처리합니다.
    player1, player2 객체를 받아와 상태를 확인하고 데미지를 적용합니다.
    """

    # --- P1이 P2를 때렸는지 검사 ---
    attack_name_p1 = player1.current_state
    # player1.attacks 딕셔너리에서 현재 공격(Attack 객체)을 가져옴
    current_attack_p1 = player1.attacks.get(attack_name_p1)

    # 1. P1이 공격 상태인가?
    # 2. P1의 현재 프레임이 P1 공격의 '타격 프레임'인가?
    # 3. P1과 P2가 충돌했는가?
    # 4. P1이 이번 공격으로 "아직 안 때렸는가"? (중복 히트 방지)
    # 5. P2가 살아있는가?
    if (current_attack_p1 and
            player1.current_frame == current_attack_p1.hit_frame and
            pygame.sprite.collide_rect(player1, player2) and
            player1.has_hit == False and
            player2.is_alive):

        # "때렸음"으로 표시
        player1.has_hit = True

        # P2가 방어 중인지 확인
        if player2.current_state == 'Blocking':
            print("P2 Blocked!")
        else:
            # 방어 중이 아니면 데미지 처리
            if current_attack_p1.is_ko_move:
                player2.take_damage(player2.max_hp)  # KO 데미지
            else:
                damage = current_attack_p1.damage
                player2.take_damage(damage)

    # --- P2가 P1을 때렸는지 검사 ---
    attack_name_p2 = player2.current_state
    current_attack_p2 = player2.attacks.get(attack_name_p2)

    if (current_attack_p2 and
            player2.current_frame == current_attack_p2.hit_frame and
            pygame.sprite.collide_rect(player2, player1) and
            player2.has_hit == False and
            player1.is_alive):

        player2.has_hit = True

        if player1.current_state == 'Blocking':
            print("P1 Blocked!")
        else:
            if current_attack_p2.is_ko_move:
                player1.take_damage(player1.max_hp)  # KO 데미지
            else:
                damage = current_attack_p2.damage
                player1.take_damage(damage)