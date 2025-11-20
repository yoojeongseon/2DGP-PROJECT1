# (파일: collisions.py)

import pygame


def handle_player_collisions(player1, player2):
    """
    두 플레이어 간의 타격 판정을 처리합니다.
    (각성 효과: 공격력 1.5배 적용)
    (Dizzy 상태: 무적 적용 - 데미지 입지 않음)
    """

    # 각성 시 데미지 배율
    AWAKEN_MULTIPLIER = 1.5

    # --- [1] P1이 P2를 때렸는지 검사 ---
    attack_name_p1 = player1.current_state
    current_attack_p1 = player1.attacks.get(attack_name_p1)

    # P1의 '주먹' hitbox를 가져옴
    absolute_hitbox_p1 = player1.get_absolute_hitbox()

    if (absolute_hitbox_p1 and
            player1.has_hit == False and
            player2.is_alive):

        # 충돌 검사
        if absolute_hitbox_p1.colliderect(player2.hurtbox_absolute):

            player1.has_hit = True  # 때렸음으로 표시

            # ▼▼▼ [핵심 수정] P2 상태 확인 ▼▼▼
            if player2.current_state == 'Blocking':
                print("P2 Blocked!")  # 방어 성공

            elif player2.current_state == 'Dizzy':
                print("P2 is Invincible! (Dizzy)")  # 무적 상태 (데미지 없음)

            else:
                # 방어도, 무적도 아닐 때만 데미지 적용
                if current_attack_p1.is_ko_move:
                    player2.take_damage(player2.max_hp)
                else:
                    damage = current_attack_p1.damage

                    # P1 각성 시 공격력 증가
                    if player1.is_awakened:
                        damage *= AWAKEN_MULTIPLIER
                        print("P1 Awakened Strike!")

                    player2.take_damage(damage)

    # --- [2] P2가 P1을 때렸는지 검사 ---
    attack_name_p2 = player2.current_state
    current_attack_p2 = player2.attacks.get(attack_name_p2)

    # P2의 '주먹' hitbox를 가져옴
    absolute_hitbox_p2 = player2.get_absolute_hitbox()

    if (absolute_hitbox_p2 and
            player2.has_hit == False and
            player1.is_alive):

        if absolute_hitbox_p2.colliderect(player1.hurtbox_absolute):

            player2.has_hit = True

            # ▼▼▼ [핵심 수정] P1 상태 확인 ▼▼▼
            if player1.current_state == 'Blocking':
                print("P1 Blocked!")  # 방어 성공

            elif player1.current_state == 'Dizzy':
                print("P1 is Invincible! (Dizzy)")  # 무적 상태 (데미지 없음)

            else:
                # 방어도, 무적도 아닐 때만 데미지 적용
                if current_attack_p2.is_ko_move:
                    player1.take_damage(player1.max_hp)
                else:
                    damage = current_attack_p2.damage

                    # P2 각성 시 공격력 증가
                    if player2.is_awakened:
                        damage *= AWAKEN_MULTIPLIER
                        print("P2 Awakened Strike!")

                    player1.take_damage(damage)