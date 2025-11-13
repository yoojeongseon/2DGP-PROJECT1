# (파일: collisions.py)

import pygame


def handle_player_collisions(player1, player2):
    """
    두 플레이어 간의 타격 판정을 처리합니다.
    (각성 효과: 공격력 1.5배 적용)
    (Dizzy 상태: 무적 적용)
    """

    # 각성 시 데미지 배율
    AWAKEN_MULTIPLIER = 1.5

    # --- P1이 P2를 때렸는지 검사 ---
    attack_name_p1 = player1.current_state
    current_attack_p1 = player1.attacks.get(attack_name_p1)

    if (current_attack_p1 and
            player1.current_frame == current_attack_p1.hit_frame and
            pygame.sprite.collide_rect(player1, player2) and
            player1.has_hit == False and
            player2.is_alive):

        player1.has_hit = True

        # [수정] P2가 방어 중이거나 'Dizzy' (무적) 상태인지 확인
        if player2.current_state == 'Blocking':
            print("P2 Blocked!")
        elif player2.current_state == 'Dizzy':
            print("P2 is Dizzy! (Invulnerable)")
            # 무적이므로 아무것도 하지 않음
        else:
            # 방어/무적이 아니면 데미지 처리
            if current_attack_p1.is_ko_move:
                player2.take_damage(player2.max_hp)
            else:
                damage = current_attack_p1.damage

                if player1.is_awakened:
                    damage *= AWAKEN_MULTIPLIER
                    print("P1 Awakened Strike!")

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

        # [수정] P1이 방어 중이거나 'Dizzy' (무적) 상태인지 확인
        if player1.current_state == 'Blocking':
            print("P1 Blocked!")
        elif player1.current_state == 'Dizzy':
            print("P1 is Dizzy! (Invulnerable)")
            # 무적이므로 아무것도 하지 않음
        else:
            # 방어/무적이 아니면 데미지 처리
            if current_attack_p2.is_ko_move:
                player1.take_damage(player1.max_hp)
            else:
                damage = current_attack_p2.damage

                if player2.is_awakened:
                    damage *= AWAKEN_MULTIPLIER
                    print("P2 Awakened Strike!")

                player1.take_damage(damage)