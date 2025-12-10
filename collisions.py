# (파일: collisions.py)

import pygame
from visual_effects import VisualEffect


def handle_player_collisions(player1, player2, effect_group, effect_frames, sounds):
    """
    타격 판정, 이펙트 생성(방향 적용), 사운드 재생
    """

    AWAKEN_MULTIPLIER = 1.5

    # ==================================================
    # 1. P1(공격) -> P2(피격)  [방향: 정방향]
    # ==================================================
    absolute_hitbox_p1 = player1.get_absolute_hitbox()

    if (absolute_hitbox_p1 and
            player1.has_hit == False and
            player2.is_alive):

        if absolute_hitbox_p1.colliderect(player2.hurtbox_absolute):
            player1.has_hit = True

            # 1. 펀치 소리
            attack_type = player1.current_state
            if attack_type in sounds:
                sounds[attack_type].play()

            # 2. 이펙트 위치 (교집합 중심)
            intersection = absolute_hitbox_p1.clip(player2.hurtbox_absolute)
            hit_pos = intersection.center

            # 3. 상태별 분기
            if player2.current_state == 'Blocking':
                print("P2 Blocked!")
                if 'BlockEffect' in effect_frames:
                    # P1 공격이므로 flip=False (기본)
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'], flip=False)
                    effect_group.add(effect)

                if 'Block' in sounds: sounds['Block'].play()

            elif player2.current_state == 'Dizzy':
                print("P2 is Invincible!")

            else:
                # 타격 이펙트 (flip=False)
                if 'HitEffect' in effect_frames:
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'], flip=False)
                    effect_group.add(effect)

                # 데미지 처리
                was_alive = player2.is_alive
                current_attack = player1.attacks[player1.current_state]
                if current_attack.is_ko_move:
                    player2.take_damage(player2.max_hp)
                else:
                    damage = current_attack.damage
                    if player1.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player2.take_damage(damage)

                if was_alive and not player2.is_alive:
                    if 'Bell' in sounds: sounds['Bell'].play()

    # ==================================================
    # 2. P2(공격) -> P1(피격) [방향: 반대방향(Flip)]
    # ==================================================
    absolute_hitbox_p2 = player2.get_absolute_hitbox()

    if (absolute_hitbox_p2 and
            player2.has_hit == False and
            player1.is_alive):

        if absolute_hitbox_p2.colliderect(player1.hurtbox_absolute):
            player2.has_hit = True

            # 1. 펀치 소리
            attack_type = player2.current_state
            if attack_type in sounds:
                sounds[attack_type].play()

            # 2. 이펙트 위치
            intersection = absolute_hitbox_p2.clip(player1.hurtbox_absolute)
            hit_pos = intersection.center

            if player1.current_state == 'Blocking':
                print("P1 Blocked!")
                if 'BlockEffect' in effect_frames:
                    # ▼▼▼ [수정] P2 공격이므로 flip=True ▼▼▼
                    effect = VisualEffect(hit_pos, effect_frames['BlockEffect'], flip=True)
                    effect_group.add(effect)

                if 'Block' in sounds: sounds['Block'].play()

            elif player1.current_state == 'Dizzy':
                print("P1 is Invincible!")

            else:
                # 타격 이펙트
                if 'HitEffect' in effect_frames:
                    # ▼▼▼ [수정] P2 공격이므로 flip=True ▼▼▼
                    effect = VisualEffect(hit_pos, effect_frames['HitEffect'], flip=True)
                    effect_group.add(effect)

                # 데미지 처리
                was_alive = player1.is_alive
                current_attack = player2.attacks[player2.current_state]
                if current_attack.is_ko_move:
                    player1.take_damage(player1.max_hp)
                else:
                    damage = current_attack.damage
                    if player2.is_awakened: damage *= AWAKEN_MULTIPLIER
                    player1.take_damage(damage)

                if was_alive and not player1.is_alive:
                    if 'Bell' in sounds: sounds['Bell'].play()