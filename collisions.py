# (파일: collisions.py)

import pygame
from visual_effects import VisualEffect  # <-- 방금 만든 클래스 가져오기


def handle_player_collisions(player1, player2, effect_group, effect_frames):
    """
    타격 판정 및 이펙트 생성 함수
    - effect_group: 이펙트 스프라이트를 담을 그룹
    - effect_frames: 이펙트 이미지들이 담긴 딕셔너리
    """

    AWAKEN_MULTIPLIER = 1.5

    # --- 1. P1 공격 판정 ---
    absolute_hitbox_p1 = player1.get_absolute_hitbox()

    if (absolute_hitbox_p1 and
            player1.has_hit == False and
            player2.is_alive):

        if absolute_hitbox_p1.colliderect(player2.hurtbox_absolute):
            player1.has_hit = True

            # 충돌 위치 (이펙트 생성 위치)
            # 대략 두 사각형의 중간 지점
            hit_pos = (
                (absolute_hitbox_p1.centerx + player2.hurtbox_absolute.centerx) // 2,
                (absolute_hitbox_p1.centery + player2.hurtbox_absolute.centery) // 2
            )

            if player2.current_state == 'Blocking':
                print("P2 Blocked!")
                # [이펙트] 방어 이펙트 생성
                if 'BlockEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'])
                    effect_group.add(effect)

            elif player2.current_state == 'Dizzy':
                print("P2 is Invincible!")

            else:
                # [이펙트] 타격 이펙트 생성
                if 'HitEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'])
                    effect_group.add(effect)

                # 데미지 처리
                current_attack = player1.attacks[player1.current_state]
                if current_attack.is_ko_move:
                    player2.take_damage(player2.max_hp)
                else:
                    damage = current_attack.damage
                    if player1.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player2.take_damage(damage)

    # --- 2. P2 공격 판정 ---
    absolute_hitbox_p2 = player2.get_absolute_hitbox()

    if (absolute_hitbox_p2 and
            player2.has_hit == False and
            player1.is_alive):

        if absolute_hitbox_p2.colliderect(player1.hurtbox_absolute):
            player2.has_hit = True

            hit_pos = (
                (absolute_hitbox_p2.centerx + player1.hurtbox_absolute.centerx) // 2,
                (absolute_hitbox_p2.centery + player1.hurtbox_absolute.centery) // 2
            )

            if player1.current_state == 'Blocking':
                print("P1 Blocked!")
                # [이펙트] 방어 이펙트 생성
                if 'BlockEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'])
                    effect_group.add(effect)

            elif player1.current_state == 'Dizzy':
                print("P1 is Invincible!")

            else:
                # [이펙트] 타격 이펙트 생성
                if 'HitEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'])
                    effect_group.add(effect)

                # 데미지 처리
                current_attack = player2.attacks[player2.current_state]
                if current_attack.is_ko_move:
                    player1.take_damage(player1.max_hp)
                else:
                    damage = current_attack.damage
                    if player2.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player1.take_damage(damage)