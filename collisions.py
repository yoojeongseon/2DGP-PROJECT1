# (파일: collisions.py - 최종 디버그: 좌표 출력)

import pygame


def handle_player_collisions(player1, player2):
    """
    플레이어 간의 타격 판정(Hitbox/Hurtbox)을 처리합니다.
    [수정] 충돌 실패 시(Miss) 실제 좌표를 출력합니다.
    """

    # --- 1. P1이 P2를 공격하는 판정 ---
    p1_hitbox = player1.get_absolute_hitbox()

    if p1_hitbox:
        # print(f"DEBUG: P1 Hitbox Active! (State: {player1.current_state}, Frame: {player1.current_frame})") # (너무 많으니 잠시 주석 처리)

        if not player1.has_hit:
            # print(f"DEBUG: P1 'has_hit' is False. (Can Damage)") # (너무 많으니 잠시 주석 처리)

            if player2.current_state != 'Blocking':
                # print(f"DEBUG: P2 is NOT Blocking. (State: {player2.current_state})") # (너무 많으니 잠시 주석 처리)

                if p1_hitbox.colliderect(player2.hurtbox_absolute):

                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!! DEBUG: P1 -> P2 HIT SUCCESS !!!!!!!!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    attack = player1.attacks[player1.current_state]
                    player2.take_damage(attack.damage)
                    player1.has_hit = True

                else:
                    # [수정] P1 Hitbox와 P2 Hurtbox의 실제 좌표를 출력
                    print("--- DEBUG: MISS! ---")
                    print(f"   P1 Hitbox: {p1_hitbox}")
                    print(f"   P2 Hurtbox: {player2.hurtbox_absolute}")
                    print("--------------------")

            else:
                print("DEBUG: P2 IS BLOCKING!")

        else:
            print("DEBUG: P1 'has_hit' is True. (Preventing multi-hit)")

    # --- 2. P2가 P1을 공격하는 판정 (P2도 동일하게 수정) ---
    p2_hitbox = player2.get_absolute_hitbox()

    if p2_hitbox:
        if not player2.has_hit:
            if player1.current_state != 'Blocking':
                if p2_hitbox.colliderect(player1.hurtbox_absolute):

                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!! DEBUG: P2 -> P1 HIT SUCCESS !!!!!!!!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                    attack = player2.attacks[player2.current_state]
                    player1.take_damage(attack.damage)
                    player2.has_hit = True

                else:
                    # [수정] P2 Hitbox와 P1 Hurtbox의 실제 좌표를 출력
                    print("--- DEBUG: MISS! (P2 Attack) ---")
                    print(f"   P2 Hitbox: {p2_hitbox}")
                    print(f"   P1 Hurtbox: {player1.hurtbox_absolute}")
                    print("--------------------------------")

            else:
                print("DEBUG: P1 IS BLOCKING!")

        else:
            print("DEBUG: P2 'has_hit' is True. (Preventing multi-hit)")