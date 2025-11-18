# (파일: collisions.py - KO 펀치 로직 적용)

import pygame


def handle_player_collisions(player1, player2):
    """
    플레이어 간의 타격 판정(Hitbox/Hurtbox)을 처리합니다.
    [수정] KO 펀치(is_ko_move)를 확인합니다.
    """

    # --- 1. P1이 P2를 공격하는 판정 ---
    p1_hitbox = player1.get_absolute_hitbox()

    if p1_hitbox:
        if not player1.has_hit:
            if player2.current_state != 'Blocking':
                if p1_hitbox.colliderect(player2.hurtbox_absolute):

                    attack = player1.attacks[player1.current_state]

                    # --- [수정] KO 펀치인지, 일반 공격인지 확인 ---
                    if attack.is_ko_move:
                        player2.force_ko()  # 즉시 KO 메서드 호출
                    else:
                        player2.take_damage(attack.damage)  # 일반 데미지
                    # --- [수정 끝] ---

                    player1.has_hit = True

                    # (디버그 프린트)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!! DEBUG: P1 -> P2 HIT SUCCESS !!!!!!!!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                else:
                    # (디버그 프린트 - Miss)
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

                    attack = player2.attacks[player2.current_state]

                    # --- [수정] KO 펀치인지, 일반 공격인지 확인 ---
                    if attack.is_ko_move:
                        player1.force_ko()  # 즉시 KO 메서드 호출
                    else:
                        player1.take_damage(attack.damage)  # 일반 데미지
                    # --- [수정 끝] ---

                    player2.has_hit = True

                    # (디버그 프린트)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!! DEBUG: P2 -> P1 HIT SUCCESS !!!!!!!!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                else:
                    # (디버그 프린트 - Miss)
                    print("--- DEBUG: MISS! (P2 Attack) ---")
                    print(f"   P2 Hitbox: {p2_hitbox}")
                    print(f"   P1 Hurtbox: {player1.hurtbox_absolute}")
                    print("--------------------------------")

            else:
                print("DEBUG: P1 IS BLOCKING!")

        else:
            print("DEBUG: P2 'has_hit' is True. (Preventing multi-hit)")